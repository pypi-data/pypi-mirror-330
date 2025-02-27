import pytest
import pkg_resources

def test_package_version():
    """Test that the package version is correct"""
    version = pkg_resources.get_distribution('ncompasslib').version
    assert version == "0.0.1.post1"
    
def test_required_packages():
    """Test that required packages are available"""
    dist = pkg_resources.get_distribution('ncompasslib')
    requires = [str(r) for r in dist.requires()]
