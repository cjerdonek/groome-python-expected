# encoding: utf-8

"""
Utility functions for setup.py.

"""

import os

ENCODING_DEFAULT = 'utf-8'

def read(path, encoding=None):
    """
    Read and return the contents of a text file as a unicode string.

    """
    if encoding is None:
        encoding = ENCODING_DEFAULT

    # This implementation was chosen to be compatible across Python 2/3.
    with open(path, 'rb') as f:
        b = f.read()

    return b.decode(encoding)

# In setup.py, scraping the version number from the package is preferable to
# importing the package because setup.py should not have to be able to
# run the package in order to do its distribution-related tasks.  Also,
# importing might not always be possible anyways, for example if the package
# is written in Python 2 but setup.py is being run from Python 3.  See this
# e-mail exchange for a brief discussion, for example:
# http://mail.python.org/pipermail/python-porting/2012-May/000298.html
def scrape_version(package_dir):
    """
    Return the version string for a package without importing the package.

    For this function to work, the package's __init__.py file must contain
    a line of the following form:

        __version__ = '0.1.2-alpha'

    """
    init_path = os.path.join(package_dir, '__init__.py')
    text = read(init_path)

    needle = '__version__ ='
    try:
        line = next(line for line in text.splitlines() if line.startswith(needle))
    except StopIteration:
        raise Exception("version string not found in: %s" % init_path)

    expr = line[len(needle):]
    # Using eval() is more robust than using a regular expression.
    # For example, this method can handle single and double quotes,
    # end-of-line comments, and more complex version string expressions.
    version = eval(expr)

    return version
