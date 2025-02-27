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
            super().__init__()
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
            super().__init__()
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