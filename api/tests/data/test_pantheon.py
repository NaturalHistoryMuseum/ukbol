from pathlib import Path

from ukbol.data.pantheon import rebuild_pantheon_tables
from ukbol.model import PantheonSpecies

pantheon_csv = Path(__file__).parent.parent / "files" / "pantheon.csv"


class TestRebuildPantheonTables:
    def test_basic(self, app_no_data):
        rebuild_pantheon_tables(pantheon_csv)

        # there are 11779 rows in the database now
        assert PantheonSpecies.query.count() == 11779
        # check a random assemblage
        assert (
            PantheonSpecies.query.filter(
                PantheonSpecies.specific_assemblage_type == "W211"
            ).count()
            == 40
        )

    def test_with_old_data(self, app_no_data):
        # add a load of data
        rebuild_pantheon_tables(pantheon_csv)
        first_count = PantheonSpecies.query.count()

        # then add the data again, this should delete what was added a moment ago and
        # then add it again
        rebuild_pantheon_tables(pantheon_csv)
        second_count = PantheonSpecies.query.count()
        assert first_count == second_count
