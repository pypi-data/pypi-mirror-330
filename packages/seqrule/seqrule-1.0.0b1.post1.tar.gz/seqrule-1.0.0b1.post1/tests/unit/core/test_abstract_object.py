"""
Tests for the AbstractObject class.

These tests verify that the AbstractObject class behaves as expected,
particularly when accessing properties using different methods.
"""

from seqrule import AbstractObject


class TestAbstractObject:
    """Test suite for the AbstractObject class."""

    def test_initialization(self):
        """Test initialization with properties."""
        obj = AbstractObject(value=42, name="test")

        assert obj.properties["value"] == 42
        assert obj.properties["name"] == "test"

    def test_dictionary_access(self):
        """Test accessing properties using dictionary-style access."""
        obj = AbstractObject(value=42, name="test")

        assert obj["value"] == 42
        assert obj["name"] == "test"

    def test_nested_dictionary_access(self):
        """Test accessing nested dictionary properties."""
        obj = AbstractObject(metadata={"type": "important", "tags": ["tag1", "tag2"]})

        assert obj["metadata"]["type"] == "important"
        assert obj["metadata"]["tags"] == ["tag1", "tag2"]

    def test_missing_property(self):
        """Test accessing a property that doesn't exist."""
        obj = AbstractObject(value=42)

        assert obj["name"] is None

    def test_equality(self):
        """Test equality comparison between AbstractObjects."""
        obj1 = AbstractObject(value=42, name="test")
        obj2 = AbstractObject(value=42, name="test")
        obj3 = AbstractObject(value=43, name="test")

        assert obj1 == obj2
        assert obj1 != obj3

    def test_repr(self):
        """Test string representation."""
        obj = AbstractObject(value=42, name="test")
        repr_str = repr(obj)

        assert "AbstractObject" in repr_str
        assert "value" in repr_str
        assert "42" in repr_str
        assert "name" in repr_str
        assert "test" in repr_str

    def test_deeply_nested_properties(self):
        """Test accessing deeply nested properties."""
        obj = AbstractObject(nested={"level1": {"level2": {"level3": "deep value"}}})

        assert obj["nested"]["level1"]["level2"]["level3"] == "deep value"

    def test_dict_access_proxy(self):
        """Test that dictionary values are wrapped in a proxy for attribute access."""
        obj = AbstractObject(metadata={"type": "important", "priority": 1})

        # Using dictionary access returns a proxy object
        metadata = obj["metadata"]
        assert metadata["type"] == "important"
        assert metadata["priority"] == 1

    def test_hash(self):
        """Test that AbstractObject instances can be hashed."""
        obj1 = AbstractObject(value=42, name="test")
        obj2 = AbstractObject(value=42, name="test")
        obj3 = AbstractObject(value=43, name="test")

        # Equal objects should have the same hash
        assert hash(obj1) == hash(obj2)
        # Different objects should have different hashes
        assert hash(obj1) != hash(obj3)

        # Test that objects can be used as dictionary keys
        d = {obj1: "value1"}
        assert (
            d[obj2] == "value1"
        )  # obj2 is equal to obj1, so should retrieve the same value

    def test_hash_with_complex_properties(self):
        """Test hashing objects with complex properties like lists, dicts, and sets."""
        # Object with a list property
        obj_with_list = AbstractObject(tags=["tag1", "tag2"])

        # Object with a dict property
        obj_with_dict = AbstractObject(metadata={"type": "important", "priority": 1})

        # Object with a set property
        obj_with_set = AbstractObject(categories={"cat1", "cat2"})

        # Object with nested complex properties
        obj_with_nested = AbstractObject(
            complex={
                "list": [1, 2, 3],
                "dict": {"a": 1, "b": 2},
                "set": {"x", "y", "z"},
            }
        )

        # Test that all objects can be hashed
        hash_values = [
            hash(obj_with_list),
            hash(obj_with_dict),
            hash(obj_with_set),
            hash(obj_with_nested),
        ]

        # All hash values should be integers
        assert all(isinstance(h, int) for h in hash_values)

        # Equal objects should have the same hash
        obj_with_list_copy = AbstractObject(tags=["tag1", "tag2"])
        assert hash(obj_with_list) == hash(obj_with_list_copy)

    def test_hash_with_unhashable_types(self):
        """Test hashing objects with properties that are normally unhashable."""
        # Create objects with normally unhashable types
        obj_with_dict = AbstractObject(dict_prop={"key": "value"})
        obj_with_list = AbstractObject(list_prop=[1, 2, 3])
        obj_with_set = AbstractObject(set_prop={"a", "b", "c"})

        # These should all be hashable now
        hash(obj_with_dict)
        hash(obj_with_list)
        hash(obj_with_set)

        # Test with nested unhashable types
        obj_with_nested = AbstractObject(
            nested={
                "dict": {"a": 1},
                "list": [1, 2, 3],
                "set": {"x", "y"},
                "mixed": {"list_in_dict": [4, 5, 6], "set_in_dict": {"p", "q"}},
            }
        )

        # Should be hashable
        hash(obj_with_nested)

        # Test with a more complex case: a list containing dictionaries
        obj_with_list_of_dicts = AbstractObject(
            complex_list=[{"name": "item1", "value": 1}, {"name": "item2", "value": 2}]
        )

        # Should be hashable
        hash(obj_with_list_of_dicts)

    def test_dict_access_proxy_methods(self):
        """Test the methods of DictAccessProxy."""
        obj = AbstractObject(
            metadata={"type": "important", "priority": 1, "nested": {"key": "value"}}
        )

        # Get the proxy object
        metadata = obj["metadata"]

        # Test the get method
        assert metadata.get("type") == "important"
        assert metadata.get("nonexistent") is None
        assert metadata.get("nonexistent", "default") == "default"

        # Test that get returns a proxy for nested dicts
        nested = metadata.get("nested")
        assert nested["key"] == "value"

        # Test the __contains__ method
        assert "type" in metadata
        assert "nonexistent" not in metadata

    def test_dict_access_proxy_get_with_none_value(self):
        """Test the get method of DictAccessProxy with None values."""
        obj = AbstractObject(data={"null_value": None, "nested": {"null_nested": None}})

        # Get the proxy object
        data = obj["data"]

        # Test get with None value
        assert data.get("null_value") is None

        # Test get with default when key exists but value is None
        assert data.get("null_value", "default") is None

        # Test nested get with None value
        nested = data.get("nested")
        assert nested.get("null_nested") is None

        # Test get with non-dict value
        assert data.get("nonexistent", 123) == 123

    def test_hash_with_non_abstract_object(self):
        """Test the __hash__ method with non-AbstractObject comparison."""
        obj = AbstractObject(value=42, name="test")

        # Test equality with non-AbstractObject
        assert obj != "not an object"

        # This should not raise an exception
        result = obj.__hash__()
        assert isinstance(result, int)

        # Create a dictionary with the object as a key
        d = {obj: "value"}
        assert obj in d

    def test_dict_access_proxy_get_with_dict_value(self):
        """Test the get method of DictAccessProxy specifically with dictionary values."""
        obj = AbstractObject(
            data={"dict_value": {"key": "value"}, "regular_value": "string"}
        )

        # Get the proxy object
        data = obj["data"]

        # Test get with dict value - should return a proxy
        dict_value = data.get("dict_value")
        assert dict_value["key"] == "value"

        # Test get with non-dict value
        regular_value = data.get("regular_value")
        assert regular_value == "string"

        # Test get with default when key doesn't exist
        default_dict = data.get("nonexistent", {"default": "dict"})
        assert default_dict["default"] == "dict"

    def test_dict_access_proxy_get_method_coverage(self):
        """Test specifically targeting the get method in DictAccessProxy for coverage."""
        # Create an object with an empty dictionary
        obj = AbstractObject(empty_data={})

        # Get the proxy object
        data = obj["empty_data"]

        # Test get with a key that doesn't exist and a non-dict default
        result = data.get("nonexistent_key", "default_value")
        assert result == "default_value"

        # Test get with a key that doesn't exist and a dict default
        dict_result = data.get("another_key", {"nested": "value"})
        assert isinstance(dict_result, object)  # Should be a proxy
        assert dict_result["nested"] == "value"

        # Create a more complex object to test the get method
        complex_obj = AbstractObject(
            data={
                "key1": "value1",
                "key2": {"nested_key": "nested_value"},
                "key3": None,
            }
        )

        # Get the proxy object
        complex_data = complex_obj["data"]

        # Test all branches of the get method
        assert complex_data.get("key1") == "value1"  # Regular value
        assert complex_data.get("key2")["nested_key"] == "nested_value"  # Dict value
        assert complex_data.get("key3") is None  # None value
        assert (
            complex_data.get("key4", "default") == "default"
        )  # Missing key with default

        # Direct access to the get method implementation
        from seqrule.core import DictAccessProxy

        proxy = DictAccessProxy({"test": "value"})
        assert proxy.get("test") == "value"
        assert proxy.get("missing", "default") == "default"
