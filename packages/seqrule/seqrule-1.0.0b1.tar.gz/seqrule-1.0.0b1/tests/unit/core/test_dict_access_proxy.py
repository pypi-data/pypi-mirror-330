"""
Tests for the DictAccessProxy class.

These tests verify that the DictAccessProxy class behaves as expected,
particularly when accessing dictionary values using different methods.
"""

from seqrule.core import DictAccessProxy


class TestDictAccessProxy:
    """Test suite for the DictAccessProxy class."""

    def test_initialization(self):
        """Test initialization with a dictionary."""
        data = {"key": "value"}
        proxy = DictAccessProxy(data)

        assert proxy._data == data

    def test_getitem(self):
        """Test accessing values using dictionary-style access."""
        proxy = DictAccessProxy({"key": "value", "nested": {"inner": "nested_value"}})

        assert proxy["key"] == "value"
        assert isinstance(proxy["nested"], DictAccessProxy)
        assert proxy["nested"]["inner"] == "nested_value"
        assert proxy["nonexistent"] is None

    def test_get_method(self):
        """Test the get method."""
        proxy = DictAccessProxy(
            {"key": "value", "nested": {"inner": "nested_value"}, "null_value": None}
        )

        # Test with existing keys
        assert proxy.get("key") == "value"
        assert proxy.get("key", "default") == "value"

        # Test with nested dictionary
        nested = proxy.get("nested")
        assert isinstance(nested, DictAccessProxy)
        assert nested["inner"] == "nested_value"

        # Test with None value
        assert proxy.get("null_value") is None
        assert proxy.get("null_value", "default") is None

        # Test with non-existent key
        assert proxy.get("nonexistent") is None
        assert proxy.get("nonexistent", "default") == "default"

        # Test with non-existent key and dict default
        dict_default = proxy.get("another_nonexistent", {"default": "dict"})
        assert isinstance(dict_default, DictAccessProxy)
        assert dict_default["default"] == "dict"

    def test_contains(self):
        """Test the __contains__ method."""
        proxy = DictAccessProxy({"key": "value", "null_key": None})

        assert "key" in proxy
        assert "null_key" in proxy
        assert "nonexistent" not in proxy
