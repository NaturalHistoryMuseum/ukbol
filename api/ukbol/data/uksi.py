from collections import deque
from itertools import batched
from typing import Iterable

import networkx as nx
import requests

from ukbol.data.utils import get, update_status
from ukbol.extensions import db
from ukbol.model import Synonym, Taxon
from ukbol.utils import log

USER_AGENT = "UKBoL taxonomy updater"
# the names we want to be the root taxa
ROOT_NAMES = ["animalia", "chromista", "fungi", "plantae"]
# some ranks we just want to ignore and not add to the database
UNACCEPTABLE_RANKS = ["unranked", "unknown", "functional group"]


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
        r = requests.get(url, params=params, headers={"user-agent": USER_AGENT})
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


def iter_taxa(graph: nx.DiGraph, *root_ids) -> Iterable[Taxon]:
    """
    Given a directed taxonomy graph, yield the roots and all the taxa below them in a
    breadth first fashion so that they can be inserted into the database successfully
    without creating any dependency issues.

    Some taxa will be skipped based a few different rules to try and filter out some of
    the mess in the UKSI taxonomy on NBN.

    :param graph: the taxonomy graph
    :param root_ids: the taxon IDs to use as the roots
    :return: yields Taxon objects
    """
    # create a queue with the root IDs to start with
    id_queue = deque(root_ids)
    while id_queue:
        taxon_id = id_queue.popleft()
        taxon = graph.nodes[taxon_id]["taxon"]
        # grab the parent taxon
        parent_id = next(graph.predecessors(taxon_id))
        parent = graph.nodes[parent_id]["taxon"]

        # ignore some ranks that we really don't want
        if taxon.rank in UNACCEPTABLE_RANKS:
            continue
        # if this is a species, and it's not under a genus, ignore it
        if taxon.rank == "species" and parent.rank != "genus":
            continue

        # if the taxon ID is a root ID, set the parent to None
        if taxon_id in root_ids:
            taxon.parent_id = None

        yield taxon

        # don't add the children of species level taxa
        if taxon.rank == "species":
            continue

        # add the children to the queue
        id_queue.extend(graph.successors(taxon_id))


def rebuild_uksi_tables():
    """
    Clear out the taxon and synonym tables, and then repopulate them with data derived
    from the NBN API.
    """
    # we're going to build a directed graph from the taxonomy data so that we can add
    # the rows into the database in the right order, thus ensuring all the foreign keys
    # get inserted ok and in the right order (i.e. the referenced row is entered before
    # the referer)
    graph = nx.DiGraph()
    # collect synonyms in here as we go
    synonyms = []
    # we only want the taxonomy at and below specific taxa, so when we spot them while
    # crawling NBN, we'll add them to the root_ids list below
    root_ids = []

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
            if name in ROOT_NAMES:
                root_ids.append(taxon.id)

    # add edges linking children to parents
    for taxon_id, data in graph.nodes(data=True):
        taxon = data["taxon"]
        if taxon.parent_id:
            if taxon.parent_id in graph:
                # add a link from the parent to this taxon
                graph.add_edge(taxon.parent_id, taxon_id)
            else:
                # the taxon has a link to a parent we don't know, do not create an edge
                # and remove the parent ID reference from the taxon to avoid breaking
                # the database's foreign key constraints on the parent ID. There are two
                # scenarios where this might happen (at least that I can think of):
                # firstly, the taxon parent isn't in the UKSI part of the NBN taxonomy,
                # I haven't seen this happen, but I guess it's possible? Secondly, the
                # taxon links to a parent ID that doesn't exist, which I have seen
                # happen and is why this code exists in the first place.
                taxon.parent_id = None

    log("Graph creation complete")
    log(f"Details: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
    log(f"Also found {len(synonyms)} synonyms")

    log("Removing existing data...")
    Synonym.query.delete()
    Taxon.query.delete()
    db.session.commit()

    batch_size = 1000
    log("Writing taxa to database...")
    # keep track of the taxon IDs we've actually entered into the database for later
    added_ids = set()
    for batch in batched(iter_taxa(graph, *root_ids), batch_size):
        added_ids.update(taxon.id for taxon in batch)
        db.session.add_all(batch)
        db.session.commit()

    log("Writing synonyms to database...")
    for batch in batched(synonyms, batch_size):
        # only add synonyms which have a taxon in the database to relate to
        db.session.add_all(
            synonym for synonym in batch if synonym.taxon_id in added_ids
        )
        db.session.commit()

    taxon_count = Taxon.query.count()
    synonym_count = Synonym.query.count()
    update_status("uksi-taxa", taxon_count)
    update_status("uksi-synonym", synonym_count)
    log(f"Added {taxon_count} taxa and {synonym_count} synonyms")
    log("UKSI derived tables rebuilt")
