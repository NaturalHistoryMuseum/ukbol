from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

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


# imported from uksi
class Synonym(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    authorship: Mapped[str | None] = mapped_column()
    rank: Mapped[str] = mapped_column()
    taxon_id: Mapped[str] = mapped_column(ForeignKey(Taxon.id), index=True)

    # relationships
    taxon: Mapped["Taxon"] = relationship(back_populates="synonyms")


# imported from BOLD
class Specimen(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    specimen_id: Mapped[str | None] = mapped_column()
    name: Mapped[str | None] = mapped_column()
    rank: Mapped[str | None] = mapped_column()
    bin_uri: Mapped[str | None] = mapped_column(index=True)
    country: Mapped[str | None] = mapped_column(index=True)
    # todo: do we actually need all of these?
    kingdom: Mapped[str | None] = mapped_column()
    phylum: Mapped[str | None] = mapped_column()
    cls: Mapped[str | None] = mapped_column()
    order: Mapped[str | None] = mapped_column()
    family: Mapped[str | None] = mapped_column()
    subfamily: Mapped[str | None] = mapped_column()
    genus: Mapped[str | None] = mapped_column()
    species: Mapped[str | None] = mapped_column()
    subspecies: Mapped[str | None] = mapped_column()
