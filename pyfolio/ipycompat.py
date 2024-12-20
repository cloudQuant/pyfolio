import IPython
from nbformat import read

# Get the major version of IPython
IPY_MAJOR = IPython.version_info[0]

# Raise an error if the IPython version is too old
if IPY_MAJOR < 3:
    raise ImportError("IPython version %d is not supported." % IPY_MAJOR)

# Always use nbformat for reading notebooks
def read_notebook(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return read(f, as_version=4)



__all__ = ['read']
