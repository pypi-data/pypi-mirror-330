import pytest
from ncompasslib.immutable import Immutable, mutate

def test_initial_attribute_setting():
    """Test that attributes can be set initially"""
    obj = Immutable()
    obj.test_attr = "value"
    assert obj.test_attr == "value"

def test_attribute_immutability():
    """Test that attributes cannot be changed after initial setting"""
    obj = Immutable()
    obj.test_attr = "value"
    
    with pytest.raises(RuntimeError):
        obj.test_attr = "new_value"
        
def test_multiple_attributes():
    """Test handling multiple attributes"""
    obj = Immutable()
    obj.attr1 = "value1"
    obj.attr2 = "value2"
    
    assert obj.attr1 == "value1"
    assert obj.attr2 == "value2"
    
    with pytest.raises(RuntimeError):
        obj.attr1 = "new_value"
        
def test_mutate_decorator():
    """Test the mutate decorator allows temporary mutation"""
    class TestClass(Immutable):
        def __init__(self):
            self.value = 0
            
        @mutate
        def increment(self):
            self.value += 1
            
    obj = TestClass()
    initial_value = obj.value
    obj.increment()
    
    assert obj.value == initial_value + 1
    
    # Verify immutability is restored
    with pytest.raises(RuntimeError):
        obj.value = 10
        
def test_mutate_decorator_with_exception():
    """Test that mutate decorator restores immutability even if function raises"""
    class TestClass(Immutable):
        def __init__(self):
            self.value = 0
            
        @mutate
        def raise_error(self):
            self.value += 1
            raise ValueError("Test error")
            
    obj = TestClass()
    
    with pytest.raises(ValueError):
        obj.raise_error()
        
    # Verify immutability is restored
    with pytest.raises(RuntimeError):
        obj.value = 10 

def test_immutable_inheritance():
    """Test that immutability works through inheritance chains"""
    class BaseClass(Immutable):
        def __init__(self):
            self.base_attr = "base"
    
    class ChildClass(BaseClass):
        def __init__(self):
            super().__init__()
            self.child_attr = "child"
    
    obj = ChildClass()
    assert obj.base_attr == "base"
    assert obj.child_attr == "child"
    
    # Test immutability of inherited attributes
    with pytest.raises(RuntimeError):
        obj.base_attr = "new_base"
    
    with pytest.raises(RuntimeError):
        obj.child_attr = "new_child"

def test_complex_data_structures():
    """Test immutability with complex data structures"""
    obj = Immutable()
    obj.list_attr = [1, 2, 3]
    obj.dict_attr = {"key": "value"}
    
    # Contents of mutable objects can still be changed
    obj.list_attr.append(4)
    obj.dict_attr["new_key"] = "new_value"
    
    assert 4 in obj.list_attr
    assert "new_key" in obj.dict_attr
    
    # But the attributes themselves can't be reassigned
    with pytest.raises(RuntimeError):
        obj.list_attr = [5, 6, 7]
    
    with pytest.raises(RuntimeError):
        obj.dict_attr = {"other": "data"}

def test_property_descriptors():
    """Test immutability with property descriptors"""
    class PropertyClass(Immutable):
        def __init__(self):
            self._value = 10
            
        @property
        def value(self):
            return self._value
            
        @value.setter
        def value(self, new_value):
            self._value = new_value
    
    obj = PropertyClass()
    
    # Direct attribute access should be immutable
    with pytest.raises(RuntimeError):
        obj._value = 20
    
    # Property setter should still be blocked by immutability
    with pytest.raises(RuntimeError):
        obj.value = 20

def test_mutate_method_chaining():
    """Test mutate decorator supports method chaining"""
    class ChainClass(Immutable):
        def __init__(self):
            self.value = 0
            
        @mutate
        def increment(self, amount=1):
            self.value += amount
            return self
            
        @mutate
        def double(self):
            self.value *= 2
            return self
    
    obj = ChainClass()
    
    # Test method chaining
    result = obj.increment().double().increment(5)
    
    assert obj.value == 7  # (0+1)*2+5
    assert result is obj  # Should return self for chaining 

def test_multi_level_inheritance():
    """Test that immutability works through multiple levels of inheritance"""
    class GrandparentClass(Immutable):
        def __init__(self):
            self.grandparent_attr = "grandparent"
    
    class ParentClass(GrandparentClass):
        def __init__(self):
            super().__init__()
            self.parent_attr = "parent"
    
    class ChildClass(ParentClass):
        def __init__(self):
            super().__init__()
            self.child_attr = "child"
    
    obj = ChildClass()
    
    # Verify attributes were set properly through the inheritance chain
    assert obj.grandparent_attr == "grandparent"
    assert obj.parent_attr == "parent"
    assert obj.child_attr == "child"
    
    # Test immutability is preserved through all inheritance levels
    with pytest.raises(RuntimeError):
        obj.grandparent_attr = "new_grandparent"
    
    with pytest.raises(RuntimeError):
        obj.parent_attr = "new_parent"
    
    with pytest.raises(RuntimeError):
        obj.child_attr = "new_child"
    
    # Verify direct attribute access in each class is also immutable
    with pytest.raises(RuntimeError):
        obj.grandparent_attr = "modified" 