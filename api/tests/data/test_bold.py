import tarfile
from pathlib import Path

import pytest

from ukbol.data.bold import (
    get_tsv_name,
    get,
    extract_taxonomy,
    iter_specimens,
    rebuild_bold_tables,
)
from ukbol.model import Specimen

bold_tar_gz = Path(__file__).parent.parent / "files" / "BOLD_Public.19-Apr-2024.tar.gz"
bad_bold_tar_gz = Path(__file__).parent.parent / "files" / "bad.tar.gz"


class TestGetTSVName:
    def test_ok(self):
        with tarfile.open(bold_tar_gz) as tar:
            assert get_tsv_name(tar) == "BOLD_Public.19-Apr-2024.tsv"

    def test_fail(self):
        with tarfile.open(bad_bold_tar_gz) as tar:
            with pytest.raises(Exception):
                get_tsv_name(tar)


class TestGet:
    def test_value_exists(self):
        assert get({"test": "value"}, "test", lowercase=False) == "value"

    def test_value_exists_lowercase(self):
        assert get({"test": "VaLuE"}, "test", lowercase=True) == "value"

    def test_value_missing(self):
        assert get({}, "test", lowercase=True) is None
        assert get({}, "test", lowercase=False) is None
        assert get({"test": "None"}, "test") is None

    def test_value_lowercase_default(self):
        assert get({"test": "VaLuE"}, "test") == "VaLuE"


class TestExtractTaxonomy:
    def test_empty(self):
        assert extract_taxonomy({}) == {}

    def test_class(self):
        assert extract_taxonomy({"class": "Goat!"}) == {
            "cls": "goat!",
            "name": "goat!",
            "rank": "class",
        }

    def test_order_full(self):
        row = {
            "kingdom": "The Kingdom",
            "phylum": "The Phylum",
            "class": "The Class",
            "order": "The Order",
            "family": "The Family",
            "subfamily": "The Subfamily",
            "genus": "The Genus",
            "species": "The Species",
            "subspecies": "The Subspecies",
            "otherStuff": "beans",
            "hello": "there!",
        }
        assert extract_taxonomy(row) == {
            "kingdom": "the kingdom",
            "phylum": "the phylum",
            "cls": "the class",
            "order": "the order",
            "family": "the family",
            "subfamily": "the subfamily",
            "genus": "the genus",
            "species": "the species",
            "subspecies": "the subspecies",
            "name": "the subspecies",
            "rank": "subspecies",
        }

    def test_order_not_full(self):
        row = {
            "phylum": "The Phylum",
            "class": "The Class",
            "order": "The Order",
            # this is a cheeky one that should be ignored
            "family": "None",
            "genus": "The Genus",
            "otherStuff": "beans",
            "hello": "there!",
        }
        assert extract_taxonomy(row) == {
            "phylum": "the phylum",
            "cls": "the class",
            "order": "the order",
            "genus": "the genus",
            "name": "the genus",
            "rank": "genus",
        }


class TestIterSpecimens:
    def test_iter_empty(self):
        assert list(iter_specimens(iter([]))) == []

    def test_iter(self):
        rows = [
            {
                "specimenid": f"{i}",
                "bin_uri": f"BOLD:{i}",
                "country": "Norway",
                "genus": "The Genus",
                "family": "The Family",
            }
            for i in range(10)
        ]
        specimens = list(iter_specimens(rows))
        assert len(specimens) == 10
        for i in range(10):
            assert isinstance(specimens[i], Specimen)
            assert specimens[i].specimen_id == f"{i}"
            assert specimens[i].bin_uri == f"BOLD:{i}"
            assert specimens[i].country == "norway"
            assert specimens[i].genus == "the genus"
            assert specimens[i].family == "the family"
            assert specimens[i].name == "the genus"
            assert specimens[i].rank == "genus"


class TestRebuildBoldTables:
    def test_basic(self, app):
        rebuild_bold_tables(bold_tar_gz)

        # there are 1000 rows in the sample bold tar.gz
        assert Specimen.query.count() == 1000
        # 9513374 is a value in the sample
        assert Specimen.query.filter(Specimen.specimen_id == "9513374").count() == 1
        # there are 44 mexico country values in the sample
        assert Specimen.query.filter(Specimen.country == "mexico").count() == 44
