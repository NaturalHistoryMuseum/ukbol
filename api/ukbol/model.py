from typing import Any, List, Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ukbol.extensions import db


# imported from uksi
class Taxon(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    authorship: Mapped[str | None] = mapped_column()
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
    name: Mapped[str] = mapped_column()
    authorship: Mapped[str | None] = mapped_column()
    rank: Mapped[str] = mapped_column()
    taxon_id: Mapped[str] = mapped_column(ForeignKey(Taxon.id), index=True)

    # relationships
    taxon: Mapped["Taxon"] = relationship(back_populates="synonyms")

    @classmethod
    def get(cls, ident: Any) -> Self | None:
        return db.session.get(cls, ident)


# imported from BOLD
class Specimen(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    processid: Mapped[str | None] = mapped_column()
    sampleid: Mapped[str | None] = mapped_column()
    fieldid: Mapped[str | None] = mapped_column()
    museumid: Mapped[str | None] = mapped_column()
    record_id: Mapped[str | None] = mapped_column()
    specimenid: Mapped[str | None] = mapped_column()
    processid_minted_date: Mapped[str | None] = mapped_column()
    bin_uri: Mapped[str | None] = mapped_column(index=True)
    bin_created_date: Mapped[str | None] = mapped_column()
    collection_code: Mapped[str | None] = mapped_column()
    inst: Mapped[str | None] = mapped_column()
    taxid: Mapped[str | None] = mapped_column()
    kingdom: Mapped[str | None] = mapped_column()
    phylum: Mapped[str | None] = mapped_column()
    cls: Mapped[str | None] = mapped_column()
    order: Mapped[str | None] = mapped_column()
    family: Mapped[str | None] = mapped_column()
    subfamily: Mapped[str | None] = mapped_column()
    tribe: Mapped[str | None] = mapped_column()
    genus: Mapped[str | None] = mapped_column()
    species: Mapped[str | None] = mapped_column()
    subspecies: Mapped[str | None] = mapped_column()
    species_reference: Mapped[str | None] = mapped_column()
    identification: Mapped[str | None] = mapped_column(index=True)
    identification_method: Mapped[str | None] = mapped_column()
    identification_rank: Mapped[str | None] = mapped_column(index=True)
    identified_by: Mapped[str | None] = mapped_column()
    identifier_email: Mapped[str | None] = mapped_column()
    taxonomy_notes: Mapped[str | None] = mapped_column()
    sex: Mapped[str | None] = mapped_column()
    reproduction: Mapped[str | None] = mapped_column()
    life_stage: Mapped[str | None] = mapped_column()
    short_note: Mapped[str | None] = mapped_column()
    notes: Mapped[str | None] = mapped_column()
    voucher_type: Mapped[str | None] = mapped_column()
    tissue_type: Mapped[str | None] = mapped_column()
    specimen_linkout: Mapped[str | None] = mapped_column()
    associated_specimens: Mapped[str | None] = mapped_column()
    associated_taxa: Mapped[str | None] = mapped_column()
    collectors: Mapped[str | None] = mapped_column()
    collection_date_start: Mapped[str | None] = mapped_column()
    collection_date_end: Mapped[str | None] = mapped_column()
    collection_event_id: Mapped[str | None] = mapped_column()
    collection_time: Mapped[str | None] = mapped_column()
    collection_notes: Mapped[str | None] = mapped_column()
    geoid: Mapped[str | None] = mapped_column()
    country_ocean: Mapped[str | None] = mapped_column()
    country_iso: Mapped[str | None] = mapped_column(index=True)
    province_state: Mapped[str | None] = mapped_column()
    region: Mapped[str | None] = mapped_column()
    sector: Mapped[str | None] = mapped_column()
    site: Mapped[str | None] = mapped_column()
    site_code: Mapped[str | None] = mapped_column()
    coord: Mapped[str | None] = mapped_column()
    coord_accuracy: Mapped[str | None] = mapped_column()
    coord_source: Mapped[str | None] = mapped_column()
    elev: Mapped[str | None] = mapped_column()
    elev_accuracy: Mapped[str | None] = mapped_column()
    depth: Mapped[str | None] = mapped_column()
    depth_accuracy: Mapped[str | None] = mapped_column()
    habitat: Mapped[str | None] = mapped_column()
    sampling_protocol: Mapped[str | None] = mapped_column()
    nuc: Mapped[str | None] = mapped_column()
    nuc_basecount: Mapped[str | None] = mapped_column()
    insdc_acs: Mapped[str | None] = mapped_column()
    funding_src: Mapped[str | None] = mapped_column()
    marker_code: Mapped[str | None] = mapped_column()
    primers_forward: Mapped[str | None] = mapped_column()
    primers_reverse: Mapped[str | None] = mapped_column()
    sequence_run_site: Mapped[str | None] = mapped_column()
    sequence_upload_date: Mapped[str | None] = mapped_column()
    bold_recordset_code_arr: Mapped[str | None] = mapped_column()
    ecoregion: Mapped[str | None] = mapped_column()
    biome: Mapped[str | None] = mapped_column()
    realm: Mapped[str | None] = mapped_column()
    sovereign_inst: Mapped[str | None] = mapped_column()

    @classmethod
    def get(cls, ident: Any) -> Self | None:
        return db.session.get(cls, ident)
