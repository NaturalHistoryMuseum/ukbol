from datetime import datetime
from typing import Any, List, Self

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ukbol.extensions import db


# imported from uksi
class Taxon(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    authorship: Mapped[str | None]
    rank: Mapped[str] = mapped_column(index=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("taxon.id"), index=True)

    # relationships
    parent: Mapped["Taxon"] = relationship(back_populates="children", remote_side=[id])
    children: Mapped[List["Taxon"]] = relationship(back_populates="parent")
    synonyms: Mapped[List["Synonym"]] = relationship(back_populates="taxon")

    @classmethod
    def get(cls, ident: Any) -> Self | None:
        return db.session.get(cls, ident)


# imported from uksi
class Synonym(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    authorship: Mapped[str | None]
    rank: Mapped[str]
    taxon_id: Mapped[str] = mapped_column(ForeignKey(Taxon.id), index=True)

    # relationships
    taxon: Mapped["Taxon"] = relationship(back_populates="synonyms")

    @classmethod
    def get(cls, ident: Any) -> Self | None:
        return db.session.get(cls, ident)


# imported from BOLD
class Specimen(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    processid: Mapped[str | None]
    sampleid: Mapped[str | None]
    fieldid: Mapped[str | None]
    museumid: Mapped[str | None]
    record_id: Mapped[str | None]
    specimenid: Mapped[str | None]
    processid_minted_date: Mapped[str | None]
    bin_uri: Mapped[str | None] = mapped_column(index=True)
    bin_created_date: Mapped[str | None]
    collection_code: Mapped[str | None]
    inst: Mapped[str | None]
    taxid: Mapped[str | None]
    kingdom: Mapped[str | None]
    phylum: Mapped[str | None]
    cls: Mapped[str | None]
    order: Mapped[str | None]
    family: Mapped[str | None]
    subfamily: Mapped[str | None]
    tribe: Mapped[str | None]
    genus: Mapped[str | None]
    species: Mapped[str | None]
    subspecies: Mapped[str | None]
    species_reference: Mapped[str | None]
    identification: Mapped[str | None] = mapped_column(index=True)
    identification_method: Mapped[str | None]
    identification_rank: Mapped[str | None] = mapped_column(index=True)
    identified_by: Mapped[str | None]
    identifier_email: Mapped[str | None]
    taxonomy_notes: Mapped[str | None]
    sex: Mapped[str | None]
    reproduction: Mapped[str | None]
    life_stage: Mapped[str | None]
    short_note: Mapped[str | None]
    notes: Mapped[str | None]
    voucher_type: Mapped[str | None]
    tissue_type: Mapped[str | None]
    specimen_linkout: Mapped[str | None]
    associated_specimens: Mapped[str | None]
    associated_taxa: Mapped[str | None]
    collectors: Mapped[str | None]
    collection_date_start: Mapped[str | None]
    collection_date_end: Mapped[str | None]
    collection_event_id: Mapped[str | None]
    collection_time: Mapped[str | None]
    collection_notes: Mapped[str | None]
    geoid: Mapped[str | None]
    country_ocean: Mapped[str | None]
    country_iso: Mapped[str | None] = mapped_column(index=True)
    province_state: Mapped[str | None]
    region: Mapped[str | None]
    sector: Mapped[str | None]
    site: Mapped[str | None]
    site_code: Mapped[str | None]
    coord: Mapped[str | None]
    coord_accuracy: Mapped[str | None]
    coord_source: Mapped[str | None]
    elev: Mapped[str | None]
    elev_accuracy: Mapped[str | None]
    depth: Mapped[str | None]
    depth_accuracy: Mapped[str | None]
    habitat: Mapped[str | None]
    sampling_protocol: Mapped[str | None]
    nuc: Mapped[str | None]
    nuc_basecount: Mapped[str | None]
    insdc_acs: Mapped[str | None]
    funding_src: Mapped[str | None]
    marker_code: Mapped[str | None]
    primers_forward: Mapped[str | None]
    primers_reverse: Mapped[str | None]
    sequence_run_site: Mapped[str | None]
    sequence_upload_date: Mapped[str | None]
    bold_recordset_code_arr: Mapped[str | None]
    ecoregion: Mapped[str | None]
    biome: Mapped[str | None]
    realm: Mapped[str | None]
    sovereign_inst: Mapped[str | None]

    @classmethod
    def get(cls, ident: Any) -> Self | None:
        return db.session.get(cls, ident)


# imported from PANTHEON
class PantheonSpecies(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    species: Mapped[str | None] = mapped_column(index=True)
    family: Mapped[str | None]
    order: Mapped[str | None]
    sqs: Mapped[str | None]
    conservation_status: Mapped[str | None]
    larval_feeding_guild: Mapped[str | None]
    adult_feeding_guild: Mapped[str | None]
    broad_biotope: Mapped[str | None]
    habitat: Mapped[str | None]
    resources: Mapped[str | None]
    specific_assemblage_type: Mapped[str | None] = mapped_column(index=True)
    habitat_score: Mapped[str | None]
    associations: Mapped[str | None]
    common_name: Mapped[str | None]
    notes: Mapped[str | None]


# information about when the data was imported from each source
class DataSourceStatus(db.Model):
    name: Mapped[str] = mapped_column(primary_key=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    version: Mapped[str | None]
    total: Mapped[int]

    @classmethod
    def get(cls, name: str) -> Self | None:
        return db.session.get(cls, name)
