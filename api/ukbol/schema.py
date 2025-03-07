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


class TaxonSuggestionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Taxon
        include_fk = False

    id = ma.auto_field()
    name = ma.auto_field()
    rank = ma.auto_field()


class SpecimenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Specimen

    id = ma.auto_field()
    processid = ma.auto_field()
    sampleid = ma.auto_field()
    fieldid = ma.auto_field()
    museumid = ma.auto_field()
    record_id = ma.auto_field()
    specimenid = ma.auto_field()
    processid_minted_date = ma.auto_field()
    bin_uri = ma.auto_field()
    bin_created_date = ma.auto_field()
    collection_code = ma.auto_field()
    inst = ma.auto_field()
    taxid = ma.auto_field()
    kingdom = ma.auto_field()
    phylum = ma.auto_field()
    cls = ma.auto_field(data_key="class")
    order = ma.auto_field()
    family = ma.auto_field()
    subfamily = ma.auto_field()
    tribe = ma.auto_field()
    genus = ma.auto_field()
    species = ma.auto_field()
    subspecies = ma.auto_field()
    species_reference = ma.auto_field()
    # capitalise the identification when outputting as we lowercase it on ingest
    identification = ma.Function(lambda specimen: specimen.identification.capitalize())
    identification_method = ma.auto_field()
    identification_rank = ma.auto_field()
    identified_by = ma.auto_field()
    identifier_email = ma.auto_field()
    taxonomy_notes = ma.auto_field()
    sex = ma.auto_field()
    reproduction = ma.auto_field()
    life_stage = ma.auto_field()
    short_note = ma.auto_field()
    notes = ma.auto_field()
    voucher_type = ma.auto_field()
    tissue_type = ma.auto_field()
    specimen_linkout = ma.auto_field()
    associated_specimens = ma.auto_field()
    associated_taxa = ma.auto_field()
    collectors = ma.auto_field()
    collection_date_start = ma.auto_field()
    collection_date_end = ma.auto_field()
    collection_event_id = ma.auto_field()
    collection_time = ma.auto_field()
    collection_notes = ma.auto_field()
    geoid = ma.auto_field()
    country_ocean = ma.auto_field(data_key="country/ocean")
    country_iso = ma.auto_field()
    province_state = ma.auto_field(data_key="province/state")
    region = ma.auto_field()
    sector = ma.auto_field()
    site = ma.auto_field()
    site_code = ma.auto_field()
    coord = ma.auto_field()
    coord_accuracy = ma.auto_field()
    coord_source = ma.auto_field()
    elev = ma.auto_field()
    elev_accuracy = ma.auto_field()
    depth = ma.auto_field()
    depth_accuracy = ma.auto_field()
    habitat = ma.auto_field()
    sampling_protocol = ma.auto_field()
    nuc = ma.auto_field()
    nuc_basecount = ma.auto_field()
    insdc_acs = ma.auto_field()
    funding_src = ma.auto_field()
    marker_code = ma.auto_field()
    primers_forward = ma.auto_field()
    primers_reverse = ma.auto_field()
    sequence_run_site = ma.auto_field()
    sequence_upload_date = ma.auto_field()
    bold_recordset_code_arr = ma.auto_field()
    ecoregion = ma.auto_field()
    biome = ma.auto_field()
    realm = ma.auto_field()
    sovereign_inst = ma.auto_field()


class TaxonBinSchema(ma.Schema):
    bin = fields.Str()
    count = fields.Integer()
    uk_count = fields.Integer()
    names = fields.List(fields.Tuple((fields.Str(), fields.Integer())))
