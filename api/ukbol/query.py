from typing import Iterator

from sqlalchemy import Select

from ukbol.extensions import db
from ukbol.model import Specimen, Taxon


def get_containing_bins(taxon: Taxon) -> set[str]:
    """
    Given a taxa, find all the BINs its name appears in and return them as a set.

    :param taxon: the taxon to look up
    :return: a set of BIN URIs
    """
    # gather up all the names this taxon has
    names = {taxon.name}
    names.update(synonym.name for synonym in taxon.synonyms)

    # find the BINs associated with the found names (ignore None BIN URIs)
    return set(
        db.session.scalars(
            db.select(Specimen.bin_uri)
            .distinct()
            # todo: should we also match on rank?
            .filter(Specimen.identification.in_(names))
            .filter(Specimen.bin_uri.isnot(None))
        )
    )


def get_associated_specimens_select(taxon: Taxon) -> Select:
    """
    Given a taxon, return a select which will find all specimens in the BINs associated
    with that taxon. This is achieved by first finding the BINs using the
    get_containing_bins function above and then returning a select based on those BINs.

    :param taxon: the Taxon object
    :return: a select statement to find associated specimens
    """
    distinct_bins = get_containing_bins(taxon)
    return db.select(Specimen).filter(Specimen.bin_uri.in_(distinct_bins))


def iter_associated_specimens(taxon: Taxon) -> Iterator[Specimen]:
    """
    Given a taxon, yield the specimens which are found in the BINs the taxon appears in.
    The BINs are found using the get_containing_bins function above. The specimens are
    returned in BIN URI order, in part because a known calling function needs this for
    a subsequent groupby.

    :param taxon: a Taxon object
    :return: yields Specimen objects
    """
    select = get_associated_specimens_select(taxon).order_by(Specimen.bin_uri)
    yield from db.session.scalars(select)
