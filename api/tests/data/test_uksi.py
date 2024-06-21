import json
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock, patch

from ukbol.data.uksi import rebuild_uksi_tables
from ukbol.model import Taxon, Synonym

nbn_mock_data = Path(__file__).parent.parent / "files" / "mock_nbn_records.json"


@contextmanager
def mock_nbn_records():
    with nbn_mock_data.open() as f:
        mock_records = json.load(f)
    mock_get_from_nbn = MagicMock(return_value=mock_records)
    with patch("ukbol.data.uksi.get_from_nbn", mock_get_from_nbn):
        yield


class TestRebuildUKSITables:
    def test_basic(self, app_no_data):
        with mock_nbn_records():
            rebuild_uksi_tables()

            assert Taxon.query.count() == 16
            assert Synonym.query.count() == 4

            biota = Taxon.get("NHMSYS0021048735")
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

            fungi = Taxon.get("NHMSYS0020535450")
            assert fungi.name == "fungi"
            assert fungi.authorship == "R.T. Moore"
            assert fungi.rank == "kingdom"
            assert len(fungi.children) == 2
            ascomycota, zygomycota = sorted(fungi.children, key=lambda t: t.name)
            assert ascomycota.name == "ascomycota"
            assert zygomycota.name == "zygomycota"

            abrothallus_cetrariae = Taxon.get("BMSSYS0000000001")
            assert abrothallus_cetrariae.parent == Taxon.get("NHMSYS0001472727")
            assert sorted(abrothallus_cetrariae.synonyms, key=lambda s: s.id) == [
                Synonym.get("BMSSYS0000042050"),
                Synonym.get("NHMSYS0000361124"),
            ]
            assert Synonym.get("BMSSYS0000042050").authorship == "I. Kotte"
            assert Synonym.get("NHMSYS0000361124").authorship is None
            assert Synonym.get("BMSSYS0000000016").rank == "variety"

    def test_with_old_data(self, app_no_data):
        with mock_nbn_records():
            # add a load of data
            rebuild_uksi_tables()
            first_taxon_count = Taxon.query.count()
            first_synonym_count = Synonym.query.count()

            # then add the data again, this should delete what was added a moment ago
            # and then add it again
            rebuild_uksi_tables()
            second_taxon_count = Taxon.query.count()
            second_synonym_count = Synonym.query.count()
            assert first_taxon_count == second_taxon_count
            assert first_synonym_count == second_synonym_count
