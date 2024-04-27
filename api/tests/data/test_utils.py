from ukbol.data.utils import get


class TestGet:
    def test_value_exists(self):
        assert get({"test": "value"}, "test", lowercase=False) == "value"
        assert get({"test": "None"}, "test", filter_str_nones=False) == "None"

    def test_value_exists_lowercase(self):
        assert get({"test": "VaLuE"}, "test", lowercase=True) == "value"

    def test_value_missing(self):
        assert get({}, "test", lowercase=True) is None
        assert get({}, "test", lowercase=False) is None
        assert get({"test": "None"}, "test", filter_str_nones=True) is None

    def test_value_lowercase_default(self):
        assert get({"test": "VaLuE"}, "test") == "VaLuE"
