"""
Provides the function for the main setup.py console_script.

"""

from __future__ import absolute_import

import sys

from pizza import pizza


# TODO: create an inner function that returns the exit status code.
# TODO: accept ingredients via the command-line.
def main(sys_argv=None, from_source=False, **kwargs):
    """
    Arguments:

      from_source: whether this function is being called from a source
        checkout (e.g. by running `python test_molt.py` or
        `python -m molt.scripts.molt`).

    """
    if sys_argv is None:
        sys_argv = sys.argv
    result = pizza.run("ingredients")
    print(result)
    sys.exit(0)
