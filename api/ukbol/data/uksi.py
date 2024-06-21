from itertools import batched
from typing import Iterable

import networkx as nx
import requests

from ukbol.data.utils import get
from ukbol.extensions import db
from ukbol.model import Taxon, Synonym
from ukbol.utils import log


def get_from_nbn() -> Iterable[dict]:
    """
    Retrieves all taxon data from NBN using their species search endpoint and yields the
    individual records as a continuous stream of dicts.

    :return: yields dicts
    """
    url = "https://species-ws.nbnatlas.org/search"
    params = {
        # this seems to work, but no idea how stable this is
        "fq": "idxtype:TAXON",
        # their API seems to cope well with us trawling it for all its data and 200
        # seems to be an ok chunk size
        "pageSize": 200,
        # fyi: this isn't a page number, it's a pure row number offset
        "start": 0,
    }

    count = 0
    log("Downloading taxonomy data from NBN API...")
    while True:
        r = requests.get(url, params=params)
        data = r.json()
        results = data["searchResults"]["results"]
        if not results:
            break
        else:
            count += len(results)
            yield from results
            params["start"] += len(results)
        # log some progress info every 10,000 records
        if count % 10000 == 0:
            log(f"{count}/{data['searchResults']['totalRecords']}")
    log(f"Downloaded {count} records from NBN API...")


def rebuild_uksi_tables():
    """
    Clear out the taxon and synonym tables, and then repopulate them with data derived
    from the NBN API.
    """
    log("Removing existing data...")
    Synonym.query.delete()
    Taxon.query.delete()
    db.session.commit()

    # we're going to build a directed graph from the taxonomy data so that we can add
    # the rows into the database in the right order, thus ensuring all the foreign keys
    # get inserted ok and in the right order (i.e. the referenced row is entered before
    # the referer)
    graph = nx.DiGraph()
    # collect synonyms in here as we go
    synonyms = []

    log("Creating taxonomy graph...")
    for record in get_from_nbn():
        # we only want uksi records
        if get(record, "infoSourceName", lowercase=True) != "uksi":
            continue

        taxon_id = record["guid"]
        # lowercase both the name and the rank to make matching easier
        name = record["scientificName"].lower()
        rank = record["rank"].lower()
        authorship = record["scientificNameAuthorship"]

        if record["taxonomicStatus"] == "synonym":
            synonyms.append(
                Synonym(
                    id=taxon_id,
                    name=name,
                    authorship=authorship,
                    rank=rank,
                    taxon_id=record["acceptedConceptID"],
                )
            )
        else:
            parent_id = record["parentGuid"]
            if not parent_id:
                parent_id = None
            taxon = Taxon(
                id=taxon_id,
                name=name,
                authorship=authorship,
                rank=rank,
                parent_id=parent_id,
            )
            graph.add_node(taxon.id, taxon=taxon)
            if taxon.parent_id:
                # add a link from the parent to this taxon
                graph.add_edge(taxon.parent_id, taxon.id)

    # remove synonyms we don't have the reference taxon for
    synonyms = [syn for syn in synonyms if syn.taxon_id in graph]

    log(f"Graph creation complete")
    log(f"Details: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
    log(f"Also found {len(synonyms)} synonyms")

    batch_size = 1000
    log("Writing taxa to database...")
    for batch in batched(nx.topological_sort(graph), batch_size):
        db.session.add_all((graph.nodes[node]["taxon"] for node in batch))
        db.session.commit()

    log("Writing synonyms to database...")
    for batch in batched(synonyms, batch_size):
        db.session.add_all(batch)
        db.session.commit()

    log(f"Added {Taxon.query.count()} taxa and {Synonym.query.count()} synonyms")
    log("UKSI derived tables rebuilt")
