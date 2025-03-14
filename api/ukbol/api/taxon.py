import csv
import io
from collections import Counter
from dataclasses import dataclass
from functools import wraps
from itertools import batched, groupby
from typing import Iterator

from flask import Blueprint, Response, request, stream_with_context
from sqlalchemy.orm import aliased

from ukbol.bins import get_associated_specimens_select, iter_associated_specimens
from ukbol.extensions import db
from ukbol.model import Taxon
from ukbol.schema import (
    SpecimenSchema,
    TaxonBinSchema,
    TaxonSchema,
    TaxonSuggestionSchema,
)
from ukbol.utils import clamp

blueprint = Blueprint("taxon_api", __name__)

# create the schemas we're going to use to build JSON responses
taxon_schema = TaxonSchema()
specimen_schema = SpecimenSchema()
suggestion_schema = TaxonSuggestionSchema()
taxon_bin_schema = TaxonBinSchema()


def validate_taxon_id(func):
    """
    Decorator that validates the taxon_id parameter by attempting to load the Taxon
    object associated with it. If a Taxon with the ID can't be found, a 404 is raised.
    If the Taxon can be found, the "taxon_id" is replaced in the kwargs with a "taxon"
    key which has the loaded Taxon object as its value. This is then passed to the
    wrapped function.

    :param func: the function to wrap
    :return: the wrapped function
    """

    @wraps(func)
    def validate(*args, **kwargs):
        taxon = db.get_or_404(Taxon, kwargs.pop("taxon_id"))
        kwargs["taxon"] = taxon
        return func(*args, **kwargs)

    return validate


@blueprint.get("/taxon/roots")
def get_roots():
    """
    Returns a list of the root Taxon objects in the taxonomy, these are ones that have
    no parent. At present which taxa this encapsulates is controlled by the uksi data
    loader which specifically trims the parents to just the 4 kingdoms we want:
    Animalia, Chromista, Fungi, and Plantae.

    :return: a list of Taxon serialised objects
    """
    return taxon_schema.dump(
        db.session.scalars(db.select(Taxon).filter(Taxon.parent_id.is_(None))).all(),
        many=True,
    )


@blueprint.get("/taxon/ranks")
def get_ranks():
    """
    Returns a list of the available taxon ranks in the taxonomy.

    :return: a list of ranks
    """
    return db.session.scalars(db.select(Taxon.rank).distinct()).all()


@blueprint.get("/taxon/suggest")
def get_suggestions():
    """
    Given a query parameter, returns a list of suggested names from the taxonomy that
    match the query. Names are matched just using a full wildcard query so the matching
    isn't particularly sophisticated. A size parameter is available to limit the number
    of results (min 1, max 20). Use ignore_ranks to exclude taxa with ranks in the given
    comma-separated list of ranks from the results.

    :return: a list of suggested taxa
    """
    query = request.args.get("query", "", type=str)
    size = clamp(request.args.get("size", 10, type=int), 1, 20)

    select = db.select(Taxon)
    if query:
        select = select.filter(Taxon.name.ilike(f"%{query}%"))

    result = db.session.scalars(select.order_by(Taxon.name).limit(size))

    return suggestion_schema.dump(result.all(), many=True)


@blueprint.get("/taxon/<taxon_id>")
@validate_taxon_id
def get_taxon(taxon: Taxon):
    """
    Given a taxon_id as part of the path, returns the Taxon associated with that ID,
    serialised as JSON. If the taxon doesn't exist, a 404 is raised.

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a Taxon object, serialised as a JSON
    """
    return taxon_schema.dump(taxon)


@blueprint.get("/taxon/<taxon_id>/children")
@validate_taxon_id
def get_taxon_children(taxon: Taxon):
    """
    Given a taxon_id as part of the path, returns the children taxa of that taxon,
    serialised as JSON. If the taxon doesn't exist, a 404 is raised. All direct children
    are returned. The Taxon returned are order by name ascending.

    Use ignore_ranks to exclude taxa with ranks in the given comma-separated list of
    ranks from the results.

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a list of child Taxon objects, serialised as a JSON
    """
    select = db.select(Taxon).filter_by(parent_id=taxon.id)
    result = db.session.scalars(select.order_by(Taxon.name))
    return taxon_schema.dump(result.all(), many=True)


@blueprint.get("/taxon/<taxon_id>/parents")
@validate_taxon_id
def get_taxon_parents(taxon: Taxon):
    """
    Given a taxon_id as part of the path, returns the parent's taxa IDs of that taxon,
    serialised as a list of strings (i.e. JSON). If the taxon doesn't exist, a 404 is
    raised. All IDs from the given taxon up to the top of the tree are returned. The IDs
    are returned in order traversing up the tree (i.e the first ID in the list is the
    immediate parent of the given taxon (such as the genus if the given taxon is a
    species), the last is the great-*-grandparent (such as the domain). The ID of the
    provided taxon is not included in the list. If the taxon doesn't have any parents,
    an empty list is returned.

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a list of parent Taxon IDs, serialised as a JSON
    """
    base_query = Taxon.query.filter(Taxon.id == taxon.id).cte(recursive=True)
    base_alias = aliased(base_query)
    join_query = Taxon.query.join(base_alias, Taxon.id == base_alias.c.parent_id)
    recursive_query = base_query.union(join_query)
    return [row[0] for row in db.session.query(recursive_query).all()][1:]


@blueprint.get("/taxon/<taxon_id>/associated_specimens")
@validate_taxon_id
def get_taxon_associated_specimens(taxon: Taxon):
    """
    Given a taxon_id as part of the path, finds the BINs the taxon appears in and then
    finds the specimens in those BINs and returns them.

    Paging can be achieved using the "page" and "per_page" parameters. The results are
    ordered by name and ID ascending.

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a list of Specimen objects, serialised as a JSON
    """
    select = get_associated_specimens_select(taxon).order_by(Taxon.name, Taxon.id)
    page = db.paginate(select)
    return {
        "count": page.total,
        "specimens": specimen_schema.dump(page.items, many=True),
    }


@dataclass
class BINSummary:
    bin: str
    count: int
    uk_count: int
    names: list[tuple[str, int]]


@blueprint.get("/taxon/<taxon_id>/bin_summaries")
@validate_taxon_id
def get_taxon_bins(taxon: Taxon):
    """
    Given a taxon_id as part of the path, matches BOLD specimens with the same taxon
    name, groups them by their assigned BIN and then returns a list of all BINs in
    descending count order with summary details about counts etc.

    The BOLD specimens are matched in the local database using a direct lowercase string
    match currently. All synonyms of the taxon are also used during matching.

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a list of JSON objects summarising a single BIN
    """
    bins = []
    for bin_uri, specimens in groupby(
        iter_associated_specimens(taxon), lambda s: s.bin_uri
    ):
        count = 0
        uk_count = 0
        names = Counter()
        for specimen in specimens:
            count += 1
            if specimen.country_iso == "GB":
                uk_count += 1
            names[specimen.identification] += 1

        bins.append(BINSummary(bin_uri, count, uk_count, names.most_common()))

    # return sorted by specimen count
    return taxon_bin_schema.dump(
        sorted(bins, key=lambda taxon_bin: taxon_bin.count, reverse=True), many=True
    )


@blueprint.get("/taxon/<taxon_id>/download/specimens")
@validate_taxon_id
def download_specimens(taxon: Taxon) -> Response:
    """
    Download the taxon bin data as a CSV file. This is done synchronously because the
    number of specimens is likely not to be that large but if this becomes a burden it
    should be changed to something asynchronous. The data is streamed in chunks to avoid
    building up lots of rows in memory.

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a streamed CSV response
    """

    def iter_rows() -> Iterator[str]:
        for batch in batched(iter_associated_specimens(taxon), 1000):
            rows = specimen_schema.dump(batch, many=True)
            data = io.StringIO()
            writer = csv.DictWriter(data, rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
            yield data.getvalue()

    # use the taxon name in the filename
    filename = f"{taxon.name.replace(' ', '_')}_specimens.csv"
    headers = {
        "Content-type": "text/csv",
        "Content-Disposition": f"attachment; filename={filename}",
    }
    # stream the rows so that we don't have to buffer the whole lot in memory first. The
    # generator needs the request context for the database
    return Response(stream_with_context(iter_rows()), headers=headers)
