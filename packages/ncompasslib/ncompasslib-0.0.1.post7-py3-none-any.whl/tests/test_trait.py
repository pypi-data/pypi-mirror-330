import pytest
from abc import abstractmethod
from ncompasslib.trait import Trait

def test_trait_immutability():
    """Test that Trait properly inherits immutability from Immutable"""
    
    class TestTrait(Trait):
        def __init__(self):
            super().__init__()
            self.test_attr = "value"
            self.number_attr = 42
            
    obj = TestTrait()
    
    # Test immutability with different attribute types
    with pytest.raises(RuntimeError):
        obj.test_attr = "new_value"
    
    with pytest.raises(RuntimeError):
        obj.number_attr = 100
        
    # Note: The current Immutable implementation allows adding new attributes
    # after initialization. This is documenting current behavior.
    obj.new_attr = "this works with current implementation"
    assert obj.new_attr == "this works with current implementation"
    
    # But changing the new attribute should be prevented
    with pytest.raises(RuntimeError):
        obj.new_attr = "this should fail"


def test_trait_mutable_containers():
    """Test behavior of mutable containers within immutable objects"""
    
    class TestTrait(Trait):
        def __init__(self):
            super().__init__()
            self.list_attr = [1, 2, 3]
            self.dict_attr = {"key": "value"}
            
    obj = TestTrait()
    
    # Cannot reassign containers
    with pytest.raises(RuntimeError):
        obj.list_attr = [4, 5, 6]
        
    with pytest.raises(RuntimeError):
        obj.dict_attr = {"new": "dict"}
    
    # Note: The following operations might be allowed depending on how Immutable is implemented
    # Documenting current behavior rather than expected behavior
    # These operations modify the container's contents, not the attribute reference itself
    obj.list_attr.append(4)
    assert 4 in obj.list_attr
    
    obj.dict_attr["new_key"] = "new_value"
    assert "new_key" in obj.dict_attr


def test_trait_abstract_behavior():
    """Test that Trait works correctly as an abstract base class"""
    
    class AbstractTrait(Trait):
        @abstractmethod
        def abstract_method(self):
            pass
    
    # Should not be able to instantiate a class with abstract methods
    with pytest.raises(TypeError):
        AbstractTrait()
    
    # Concrete implementation should work
    class ConcreteTrait(AbstractTrait):
        def abstract_method(self):
            return "implemented"
    
    obj = ConcreteTrait()
    assert obj.abstract_method() == "implemented"


def test_trait_inheritance_chain():
    """Test that Trait works in multi-level inheritance chains"""
    
    class BaseTrait(Trait):
        def __init__(self):
            super().__init__()
            self.base_attr = "base"
    
    class DerivedTrait(BaseTrait):
        def __init__(self):
            super().__init__()
            self.derived_attr = "derived"
    
    class FurtherDerivedTrait(DerivedTrait):
        def __init__(self):
            super().__init__()
            self.further_attr = "further"
    
    obj = FurtherDerivedTrait()
    
    # Test attribute access through inheritance chain
    assert obj.base_attr == "base"
    assert obj.derived_attr == "derived"
    assert obj.further_attr == "further"
    
    # Test immutability is preserved through inheritance
    with pytest.raises(RuntimeError):
        obj.base_attr = "new_base"


def test_trait_with_parameters():
    """Test Trait subclasses that accept initialization parameters"""
    
    class ParameterizedTrait(Trait):
        def __init__(self, param1=None, param2=None):
            # Call super().__init__() without parameters - it should work now
            super().__init__()
            self.param1 = param1
            self.param2 = param2
    
    obj1 = ParameterizedTrait("value1")
    obj2 = ParameterizedTrait("value1", "value2")
    
    assert obj1.param1 == "value1"
    assert obj1.param2 is None
    assert obj2.param1 == "value1"
    assert obj2.param2 == "value2"


def test_trait_class_vs_instance_attributes():
    """Test behavior of class attributes vs instance attributes in Traits"""
    
    class TraitWithClassAttrs(Trait):
        class_attr = "class_value"
        
        def __init__(self):
            super().__init__()
            self.instance_attr = "instance_value"
    
    obj1 = TraitWithClassAttrs()
    obj2 = TraitWithClassAttrs()
    
    # Test class attribute access
    assert obj1.class_attr == "class_value"
    assert obj2.class_attr == "class_value"
    assert TraitWithClassAttrs.class_attr == "class_value"
    
    # Class attributes can be modified at class level
    TraitWithClassAttrs.class_attr = "new_class_value"
    assert obj1.class_attr == "new_class_value"
    assert obj2.class_attr == "new_class_value"
    
    # Note: Class attributes accessed through instance typically aren't
    # protected by the same immutability mechanisms as instance attributes
    # Documenting current behavior
    obj1.class_attr = "instance_override"
    assert obj1.class_attr == "instance_override"
    # Class attribute remains unchanged
    assert TraitWithClassAttrs.class_attr == "new_class_value"
    assert obj2.class_attr == "new_class_value"
