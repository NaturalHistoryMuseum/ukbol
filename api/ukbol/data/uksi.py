import csv
import zipfile
from io import TextIOWrapper
from itertools import batched
from pathlib import Path
from typing import Iterable

import networkx as nx

from ukbol.data.utils import get
from ukbol.extensions import db
from ukbol.model import Taxon, Synonym
from ukbol.utils import log


def rebuild_uksi_tables(uksi_dwca: Path):
    """
    Given the Path to a UKSI taxonomy DwC-A file, clear out the taxon and synonym
    tables, and then repopulate them with data derived from the DwC-A.

    :param uksi_dwca: the Path to a DwC-A file of the UKSI taxonomy
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
    with zipfile.ZipFile(uksi_dwca) as dwca:
        with dwca.open("taxa.csv") as f:
            taxa_csv = TextIOWrapper(f, encoding="utf-8", newline="")
            reader: Iterable[dict] = csv.DictReader(taxa_csv, dialect=csv.excel)
            for row in reader:
                taxon_id = row["taxonID"]
                # lowercase both the name and the rank to make matching easier
                name = row["scientificName"].lower()
                rank = row["taxonRank"].lower()
                authorship = get(row, "scientificNameAuthorship")

                if row["taxonomicStatus"] == "synonym":
                    synonyms.append(
                        Synonym(
                            id=taxon_id,
                            name=name,
                            authorship=authorship,
                            rank=rank,
                            taxon_id=row["acceptedNameUsageID"],
                        )
                    )
                else:
                    parent_id = row.get("parentNameUsageID", None)
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
