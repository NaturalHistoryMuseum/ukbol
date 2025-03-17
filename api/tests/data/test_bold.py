import tarfile
from pathlib import Path

import pytest

from ukbol.data.bold import get_tsv_name, rebuild_bold_tables
from ukbol.model import Specimen

bold_tar_gz = Path(__file__).parent.parent / "files" / "BOLD_Public.24-JAN-2025.tar.gz"
bad_bold_tar_gz = Path(__file__).parent.parent / "files" / "bad.tar.gz"


class TestGetTSVName:
    def test_ok(self):
        with tarfile.open(bold_tar_gz) as tar:
            assert (
                get_tsv_name(tar)
                == "BOLD_Public.24-JAN-2025/BOLD_Public.24-Jan-2025.tsv"
            )

    def test_fail(self):
        with tarfile.open(bad_bold_tar_gz) as tar:
            with pytest.raises(Exception):
                get_tsv_name(tar)


class TestRebuildBoldTables:
    def test_basic(self, app_no_data):
        rebuild_bold_tables(bold_tar_gz)

        # there are 1000 rows in the sample bold tar.gz
        assert Specimen.query.count() == 999
        # 9513374 is a value in the sample
        assert Specimen.query.filter(Specimen.specimenid == "1575613").count() == 1
        # there are 168 mexico country values in the sample
        assert Specimen.query.filter(Specimen.country_iso == "MX").count() == 168

    def test_with_old_data(self, app_no_data):
        # add a load of data
        rebuild_bold_tables(bold_tar_gz)
        first_count = Specimen.query.count()

        # then add the data again, this should delete what was added a moment ago and
        # then add it again
        rebuild_bold_tables(bold_tar_gz)
        second_count = Specimen.query.count()
        assert first_count == second_count
