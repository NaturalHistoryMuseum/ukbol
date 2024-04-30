from functools import wraps

from flask import Blueprint
from sqlalchemy.orm import aliased

from ukbol.extensions import db
from ukbol.model import Taxon, Specimen
from ukbol.schema import TaxonSchema, SpecimenSchema

blueprint = Blueprint("taxon_api", __name__)

taxon_schema = TaxonSchema()
specimen_schema = SpecimenSchema()


def validate_taxon_id(func):
    @wraps(func)
    def validate(*args, **kwargs):
        taxon = db.get_or_404(Taxon, kwargs.pop("taxon_id"))
        kwargs["taxon"] = taxon
        return func(*args, **kwargs)

    return validate


@blueprint.get("/taxon/roots")
def get_roots():
    return taxon_schema.dump(
        Taxon.query.filter(Taxon.parent_id.is_(None)).order_by(Taxon.name), many=True
    )


@blueprint.get("/taxon/<taxon_id>")
@validate_taxon_id
def get_taxon(taxon: Taxon):
    return taxon_schema.dump(taxon)


@blueprint.get("/taxon/<taxon_id>/children")
@validate_taxon_id
def get_taxon_children(taxon: Taxon):
    return taxon_schema.dump(
        Taxon.query.filter(Taxon.parent_id == taxon.id).order_by(Taxon.name), many=True
    )


@blueprint.get("/taxon/<taxon_id>/parents")
@validate_taxon_id
def get_taxon_parents(taxon: Taxon):
    base_query = Taxon.query.filter(Taxon.id == taxon.id).cte(recursive=True)
    base_alias = aliased(base_query, name="tt")
    join_query = Taxon.query.join(base_alias, Taxon.id == base_alias.c.parent_id)
    recursive_query = base_query.union(join_query)
    return [row[0] for row in db.session.query(recursive_query).all()][1:]


@blueprint.get("/taxon/<taxon_id>/specimens")
@validate_taxon_id
def get_taxon_specimens(taxon: Taxon):
    # todo: should we use the rank too?
    # we find the specimens from the selected taxon using a simple exact name match with
    # the accepted name plus the synonyms (if there are any)
    names = {taxon.name}
    names.update(synonym.name for synonym in taxon.synonyms)
    page = db.paginate(
        Specimen.query.filter(Specimen.name.in_(names)).order_by(
            Specimen.name, Specimen.id
        )
    )
    return {
        "count": page.total,
        "specimens": specimen_schema.dump(page.items, many=True),
    }
