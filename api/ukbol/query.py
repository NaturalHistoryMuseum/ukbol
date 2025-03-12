from typing import Iterator

from ukbol.extensions import db
from ukbol.model import Specimen, Taxon


def iter_specimens_in_associated_bins(taxon: Taxon) -> Iterator[Specimen]:
    """
    Given a taxon, get a distinct list of the BIN URIs for the specimens with the same
    name as the taxon, then lookup all the specimens in those BINs and yield them in BIN
    URI order.

    What this essentially does it find all the specimens in the BINs this taxon appears
    in regardless of whether they have the same exact name as this taxon.

    :param taxon: a Taxon object
    :return: yields Specimen objects
    """
    # gather up all the names this taxon has
    names = {taxon.name}
    names.update(synonym.name for synonym in taxon.synonyms)

    # find the BINs associated with the found names (ignore None BIN URIs)
    distinct_bins = set(
        db.session.scalars(
            db.select(Specimen.bin_uri)
            .distinct()
            .filter(Specimen.identification.in_(names))
            .filter(Specimen.bin_uri.isnot(None))
        )
    )

    # order the results by the BIN URI (one of the primary callers of this function uses
    # groupby to process the specimens yielded from this function and doing the ordering
    # here is more efficient!)
    select = (
        db.select(Specimen)
        .filter(Specimen.bin_uri.in_(distinct_bins))
        .order_by(Specimen.bin_uri)
    )
    yield from db.session.scalars(select)
