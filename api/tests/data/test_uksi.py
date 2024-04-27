from pathlib import Path

from ukbol.data.uksi import rebuild_uksi_tables
from ukbol.model import Taxon, Synonym

uksi_dwca = Path(__file__).parent.parent / "files" / "uksi_dwca.zip"


def test_rebuild_uksi_tables(app):
    rebuild_uksi_tables(uksi_dwca)

    assert Taxon.query.count() == 16
    assert Synonym.query.count() == 4

    biota = Taxon.query.get("NHMSYS0021048735")
    assert biota.name == "biota"
    assert biota.rank == "unranked"
    assert biota.parent_id is None
    assert len(biota.children) == 1

    eukaryota = biota.children[0]
    assert eukaryota.id == "NBNSYS0100003095"
    assert eukaryota.name == "eukaryota"
    assert eukaryota.rank == "domain"

    fungi = Taxon.query.get("NHMSYS0020535450")
    assert fungi.name == "fungi"
    assert fungi.rank == "kingdom"
    assert len(fungi.children) == 2
    ascomycota, zygomycota = sorted(fungi.children, key=lambda t: t.name)
    assert ascomycota.name == "ascomycota"
    assert zygomycota.name == "zygomycota"

    abrothallus_cetrariae = Taxon.query.get("BMSSYS0000000001")
    assert abrothallus_cetrariae.parent == Taxon.query.get("NHMSYS0001472727")
    assert sorted(abrothallus_cetrariae.synonyms, key=lambda s: s.id) == [
        Synonym.query.get("BMSSYS0000042050"),
        Synonym.query.get("NHMSYS0000361124"),
    ]
    assert Synonym.query.get("BMSSYS0000000016").rank == "variety"
