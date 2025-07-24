"""Test basic imports to debug CI issues"""

def test_basic_imports():
    """Test that basic imports work"""
    import pyfolio
    assert hasattr(pyfolio, '__version__')
    
def test_utils_import():
    """Test that utils can be imported"""
    from pyfolio import utils
    assert hasattr(utils, 'HAS_IPYTHON')
    
def test_ipython_optional():
    """Test that IPython import is optional"""
    import pyfolio.utils as utils
    # Whether or not IPython is available, import should work
    assert hasattr(utils, 'display')
    assert hasattr(utils, 'HTML')