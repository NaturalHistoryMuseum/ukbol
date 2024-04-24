import csv
import zipfile
from collections import defaultdict
from io import TextIOWrapper
from itertools import batched
from pathlib import Path
from typing import Iterable

import networkx as nx

from ukbol.extensions import db
from ukbol.model import Taxon, Synonym
from ukbol.utils import log


def rebuild_uksi_tables(uksi_dwca: Path):
    Synonym.query.delete()
    Taxon.query.delete()
    db.session.commit()

    graph = nx.Graph()
    synonyms = defaultdict(list)
    roots = []

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

                if row["taxonomicStatus"] == "synonym":
                    synonym_for_taxon_id = row["acceptedNameUsageID"]
                    synonyms[synonym_for_taxon_id].append(
                        Synonym(
                            id=taxon_id,
                            name=name,
                            rank=rank,
                            taxon_id=synonym_for_taxon_id,
                        )
                    )
                else:
                    parent_id = row.get("parentNameUsageID", None)
                    if not parent_id:
                        parent_id = None
                    taxon = Taxon(
                        id=taxon_id,
                        name=name,
                        rank=rank,
                        parent_id=parent_id,
                    )
                    graph.add_node(taxon.id, taxon=taxon)
                    if taxon.parent_id:
                        graph.add_edge(taxon.id, taxon.parent_id)
                    else:
                        roots.append(taxon)

    log(f"Graph creation complete")
    log(f"Details: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
    log(f"Also found {len(synonyms)} taxa with synonyms")
    log("Writing to database...")

    # add the taxon and synonym objects to the database in batches of 1000
    for batch in batched(iter_model_objects(graph, synonyms, roots), 1000):
        db.session.add_all(batch)
        db.session.commit()

    log(f"Added {Taxon.query.count()} taxa and {Synonym.query.count()} synonyms")
    log("UKSI derived tables rebuilt")


def iter_model_objects(
    graph: nx.Graph,
    synonyms: dict[str, list[Synonym]],
    roots: list[Taxon],
) -> Iterable[Taxon | Synonym]:
    for layer in nx.bfs_layers(graph, sources=[root.id for root in roots]):
        taxa = [graph.nodes[node]["taxon"] for node in layer]
        yield from taxa
        yield from (synonym for taxon in taxa for synonym in synonyms[taxon.id])
