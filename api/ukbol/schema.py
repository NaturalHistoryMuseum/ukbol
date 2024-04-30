from marshmallow import fields

from ukbol.extensions import ma
from ukbol.model import Taxon, Synonym, Specimen


class SynonymSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Synonym

    id = ma.auto_field()
    name = ma.auto_field()
    authorship = ma.auto_field()
    rank = ma.auto_field()
    taxon = ma.auto_field()


class TaxonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Taxon
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    authorship = ma.auto_field()
    rank = ma.auto_field()
    parent = ma.auto_field()
    children = ma.auto_field()
    synonyms = fields.Nested(SynonymSchema(), many=True)


class SpecimenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Specimen

    id = ma.auto_field()
    specimen_id = ma.auto_field()
    name = ma.auto_field()
    rank = ma.auto_field()
    bin_uri = ma.auto_field()
    country = ma.auto_field()
    kingdom = ma.auto_field()
    phylum = ma.auto_field()
    cls = ma.auto_field()
    order = ma.auto_field()
    family = ma.auto_field()
    subfamily = ma.auto_field()
    genus = ma.auto_field()
    species = ma.auto_field()
    subspecies = ma.auto_field()
