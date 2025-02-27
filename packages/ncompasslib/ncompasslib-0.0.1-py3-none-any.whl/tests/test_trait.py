import pytest
from ncompasslib.trait import Trait

def test_trait_inheritance():
    """Test that Trait properly inherits from Immutable"""
    
    class TestTrait(Trait):
        def __init__(self):
            super().__init__()
            self.test_attr = "value"
            
    obj = TestTrait()
    
    # Test immutability
    with pytest.raises(RuntimeError):
        obj.test_attr = "new_value"
