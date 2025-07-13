import pytest
from utils.Registry import Registry


@pytest.fixture
def registry():
    return Registry[str]()


def test_register_items(registry):
    assert len(registry.items) == 0
    registry.register('first_item', 'A')
    assert len(registry.items) == 1 and registry.items['first_item'] == 'A'


def test_prevent_override(registry):
    assert len(registry.items) == 0
    registry.register('first_item', 'A')
    assert len(registry.items) == 1 and registry.items['first_item'] == 'A'
    with pytest.raises(ValueError):
        registry.register('first_item', 'B')
    registry.register('first_item', 'B', override=True)
    assert len(registry.items) == 1 and registry.items['first_item'] == 'B'
    
def test_register_multi_items(registry):
    assert len(registry.items) == 0
    registry.register('first_item', 'A')
    assert len(registry.items) == 1 and registry.items['first_item'] == "A"
    registry.register("second_item", "B")
    assert len(registry.items) == 2 and registry.items["second_item"] == "B" and registry.items["first_item"] == "A"
    
def test_unregister(registry):

    registry.register("first_item", "A")
    registry.register("second_item", "B")
    assert len(registry.items) == 2 and registry.items["second_item"] == "B" and registry.items["first_item"] == "A"
    registry.unregister("first_item")
    with pytest.raises(KeyError):
        registry.items["first_item"]
    
def test_unregister_non_existent(registry):
    registry.register("first_item", "A")
    with pytest.raises(KeyError):
        registry.unregister("second_item")
        
@pytest.mark.parametrize(
    "key, registered_items, expected",
    [
        ("foo", {"foo": "bar", "baz": "qux"}, True),         # key vorhanden
        ("baz", {"foo": "bar", "baz": "qux"}, True),         # anderer vorhandener key
        ("missing", {"foo": "bar", "baz": "qux"}, False),    # nicht vorhanden
        ("", {"": "leer"}, True),                            # leerer key
        ("test", {}, False),                                 # leere Registry
    ]
)
def test_has(registry,key, registered_items, expected):
 
    for k, v in registered_items.items():
        registry.register(k, v)
    assert registry.has(key) == expected
    
@pytest.mark.parametrize(
    "key, registered_items, default_value, expected",
    [
        ("foo", {"foo": "bar", "baz": "qux"}, "default", "bar"),      # vorhanden
        ("baz", {"foo": "bar", "baz": "qux"}, "default", "qux"),      # anderer vorhandener key
        ("missing", {"foo": "bar", "baz": "qux"}, "default", "default"),  # fehlt
        ("", {"": "leer", "x": "y"}, "fallback", "leer"),             # leerer key vorhanden
        ("z", {}, "fallback", "fallback"),                            # leere Registry
    ]
)
def test_get(registry,key, registered_items, default_value, expected):
    
    for k, v in registered_items.items():
        registry.register(k, v)
    assert registry.get(key, default_value) == expected
    
def test_all(registry):
    registry.register("One","one")
    registry.register("Two","two")
    registry.register("Three","three")
    expected = {
        "One": "one",
        "Two": "two",
        "Three": "three"
    }
    assert registry.all() == expected
    
def test_clear(registry):
    registry.register("One","one")
    registry.register("Two","two")
    registry.register("Three","three")
    expected = {
        "One": "one",
        "Two": "two",
        "Three": "three"
    }
    assert registry.all() == expected
    registry.clear()
    assert len(registry) == 0 
    for k in expected:
        assert k not in registry.items
    

@pytest.mark.parametrize(
    "registered_items, expected_length",
    [
        ({}, 0),  # leer
        ({"a": "A"}, 1),  # ein Eintrag
        ({"a": "A", "b": "B"}, 2),  # zwei Einträge
        ({"x": "X", "y": "Y", "z": "Z"}, 3),  # drei Einträge
    ]
)
def test_len(registry,registered_items, expected_length):

    for k, v in registered_items.items():
        registry.register(k, v)
    assert len(registry) == expected_length

@pytest.mark.parametrize(
    "registered_items, expected",
    [
        ({}, "<>"),  # leer
        ({"a": "A"}, "<'a': 'A'>"),  # ein Eintrag
        ({"x": "X", "y": "Y", "z": "Z"},"<'x': 'X', 'y': 'Y', 'z': 'Z'>")
        
    ]
)
def test_str(registry, registered_items,expected):
    for k, v in registered_items.items():
        registry.register(k, v)
    assert str(registry) == expected