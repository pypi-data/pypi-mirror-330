import pytest
import threading
import time
from at_common_workflow.core.context import Context

def test_context_operations():
    context = Context()
    
    # Test setting and getting values
    context.set("key1", "value1")
    assert context.get("key1") == "value1"
    
    # Test nested values
    context.set("nested", {"a": {"b": "value"}})
    assert context.get("nested.a.b") == "value"
    
    # Test missing keys
    with pytest.raises(KeyError):
        context.get("non_existent")
    
    assert context.get("non_existent", default="default") == "default"

def test_attribute_access():
    context = Context()
    
    # Test attribute setting and getting
    context.user_name = "John"
    assert context.user_name == "John"
    assert context.get("user_name") == "John"
    
    # Test attribute access with default
    assert context.get("non_existent_attr", "default") == "default"
    
    # Test attribute error
    with pytest.raises(KeyError):
        _ = context.non_existent_attr

def test_contains_operator():
    context = Context()
    context.set("a.b.c", "value")
    
    assert "a" in context
    assert "a.b" in context
    assert "a.b.c" in context
    assert "a.b.d" not in context
    assert "x" not in context

def test_repr_functionality():
    context = Context()
    context.name = "test"
    context.nested = {"key": "value"}
    
    repr_str = repr(context)
    assert repr_str.startswith("Context(")
    assert repr_str.endswith(")")
    assert "name" in repr_str
    assert "test" in repr_str
    assert "nested" in repr_str

def test_type_handling():
    context = Context()
    
    # Test various types
    test_values = {
        "int": 42,
        "float": 3.14,
        "bool": True,
        "list": [1, 2, 3],
        "dict": {"a": 1},
        "none": None,
        "complex": {"list": [{"nested": "value"}]}
    }
    
    for key, value in test_values.items():
        context.set(key, value)
        assert context.get(key) == value

def test_edge_cases():
    context = Context()
    
    # Test empty string key
    with pytest.raises(KeyError):
        context.get("")
    
    # Test None key
    with pytest.raises(AttributeError):
        context.get(None)
    
    # Test key with multiple dots
    context.set("a..b", "value")
    assert context.get("a..b") == "value"
    
    # Test key ending with dot
    context.set("end.", "value")
    assert context.get("end.") == "value"

def test_thread_safety():
    context = Context()
    iterations = 1000
    threads = 10
    errors = []

    def worker():
        try:
            for i in range(iterations):
                key = f"key{i}"
                context.set(key, i)
                assert context.get(key) == i
                time.sleep(0.0001)  # Force thread switching
        except Exception as e:
            errors.append(e)

    # Create and start threads
    threads_list = [threading.Thread(target=worker) for _ in range(threads)]
    for t in threads_list:
        t.start()
    
    # Wait for all threads to complete
    for t in threads_list:
        t.join()
    
    assert not errors, f"Thread safety test failed with errors: {errors}"