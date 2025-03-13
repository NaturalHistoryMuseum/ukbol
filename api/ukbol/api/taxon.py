import csv
import io
from collections import Counter
from dataclasses import dataclass
from functools import wraps
from itertools import groupby

from flask import Blueprint, Response, make_response, request
from sqlalchemy import Select
from sqlalchemy.orm import aliased

from ukbol.extensions import db
from ukbol.model import Specimen, Taxon
from ukbol.query import iter_specimens_in_associated_bins
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


def add_ignore_ranks_filter(select: Select) -> Select:
    """
    Adds a clause to the given select query to ignore taxon ranks. The ranks to ignore
    are extracted from the request's query parameters. If no ranks are specified, no
    additional clause is added and all ranks are allowed in the query.

    The query parameter which is used to specify the ranks to ignore is called
    "ignore_ranks" and should contain a comma separated list of ranks.

    :param select: the select query to use
    :return: the select query with the added clause if necessary
    """
    ignore_ranks = request.args.get("ignore_ranks", "", type=str)
    if not ignore_ranks:
        return select

    to_ignore = [rank.strip() for rank in ignore_ranks.split(",")]
    return select.filter(Taxon.rank.not_in(to_ignore))


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

    select = add_ignore_ranks_filter(select)
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
    select = add_ignore_ranks_filter(select)
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


@blueprint.get("/taxon/<taxon_id>/specimens")
@validate_taxon_id
def get_taxon_specimens(taxon: Taxon):
    """
    Given a taxon_id as part of the path, matches BOLD specimens with the same taxon
    name and returns the details about them in a paginated fashion. The BOLD specimens
    are matched in the local database using a direct lowercase string match currently.
    All synonyms of the taxon are also used during matching.

    Paging can be achieved using the "page" and "per_page" parameters. The results are
    ordered by name and ID ascending.

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a list of Specimen objects, serialised as a JSON
    """
    # todo: should we use the rank too?
    # we find the specimens from the selected taxon using a simple exact name match with
    # the accepted name plus the synonyms (if there are any)
    names = {taxon.name}
    names.update(synonym.name for synonym in taxon.synonyms)
    select = (
        db.select(Specimen)
        .filter(Specimen.identification.in_(names))
        .order_by(Specimen.identification, Specimen.id)
    )

    page = db.paginate(select)
    return {
        "count": page.total,
        "specimens": specimen_schema.dump(page.items, many=True),
    }


@dataclass
class TaxonBin:
    bin: str
    count: int
    uk_count: int
    names: list[tuple[str, int]]


@blueprint.get("/taxon/<taxon_id>/bins")
@validate_taxon_id
def get_taxon_bins(taxon: Taxon):
    """
    Given a taxon_id as part of the path, matches BOLD specimens with the same taxon
    name, groups them by their assigned BIN and then returns a list of all bins in
    descending count order with details about counts etc.

    The BOLD specimens are matched in the local database using a direct lowercase string
    match currently. All synonyms of the taxon are also used during matching.

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a list of JSON objects representing a single BIN
    """
    bins = []
    for bin_uri, specimens in groupby(
        iter_specimens_in_associated_bins(taxon), lambda s: s.bin_uri
    ):
        count = 0
        uk_count = 0
        names = Counter()
        for specimen in specimens:
            count += 1
            if specimen.country_iso == "GB":
                uk_count += 1
            names[specimen.identification] += 1

        bins.append(TaxonBin(bin_uri, count, uk_count, names.most_common()))

    # return sorted by specimen count
    return taxon_bin_schema.dump(
        sorted(bins, key=lambda taxon_bin: taxon_bin.count, reverse=True), many=True
    )


@blueprint.get("/taxon/<taxon_id>/download/specimens")
@validate_taxon_id
def download_specimens(taxon: Taxon) -> Response:
    """
    Download the taxon bin data as a CSV. This is done synchronously because the number
    of specimens is likely not to be that large but if this becomes a burden it should
    be changed to something asynchronous (and we'd need to page the get_taxon_bins route
    as well really).

    :param taxon: the Taxon object, retrieved via the validate_taxon_id decorator
    :return: a CSV file response
    """
    data = io.StringIO()
    headers = [column.name for column in Specimen.__table__.columns]
    writer = csv.DictWriter(data, headers)
    writer.writeheader()
    writer.writerows(
        specimen_schema.dump(iter_specimens_in_associated_bins(taxon), many=True)
    )
    output = make_response(data.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=specimens.csv"
    output.headers["Content-type"] = "text/csv"
    return output
