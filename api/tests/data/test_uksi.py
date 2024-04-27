from pathlib import Path

from ukbol.data.uksi import rebuild_uksi_tables
from ukbol.model import Taxon, Synonym

uksi_dwca = Path(__file__).parent.parent / "files" / "uksi_dwca.zip"


class TestRebuildUKSITables:
    def test_basic(self, app):
        rebuild_uksi_tables(uksi_dwca)

        assert Taxon.query.count() == 16
        assert Synonym.query.count() == 4

        biota = Taxon.query.get("NHMSYS0021048735")
        assert biota.name == "biota"
        assert biota.rank == "unranked"
        assert biota.authorship is None
        assert biota.parent_id is None
        assert len(biota.children) == 1

        eukaryota = biota.children[0]
        assert eukaryota.id == "NBNSYS0100003095"
        assert eukaryota.name == "eukaryota"
        assert eukaryota.authorship == "(Chatton, 1925) Whittaker & Margulis, 1978"
        assert eukaryota.rank == "domain"

        fungi = Taxon.query.get("NHMSYS0020535450")
        assert fungi.name == "fungi"
        assert fungi.authorship == "R.T. Moore"
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
        assert Synonym.query.get("BMSSYS0000042050").authorship == "I. Kotte"
        assert Synonym.query.get("NHMSYS0000361124").authorship is None
        assert Synonym.query.get("BMSSYS0000000016").rank == "variety"

    def test_with_old_data(self, app):
        # add a load of data
        rebuild_uksi_tables(uksi_dwca)
        first_taxon_count = Taxon.query.count()
        first_synonym_count = Synonym.query.count()

        # then add the data again, this should delete what was added a moment ago and
        # then add it again
        rebuild_uksi_tables(uksi_dwca)
        second_taxon_count = Taxon.query.count()
        second_synonym_count = Synonym.query.count()
        assert first_taxon_count == second_taxon_count
        assert first_synonym_count == second_synonym_count
