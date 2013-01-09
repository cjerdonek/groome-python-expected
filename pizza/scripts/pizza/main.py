"""
Provides the function for the main setup.py console_script.

"""

from __future__ import absolute_import

import sys

from pizza import pizza
import pizza.test.harness.main as harness
from pizza.scripts.pizza import argparsing

def run_tests():
    harness.run_tests()

def main_inner(sys_argv=None):
    """Run the program and return the status code."""
    if sys_argv is None:
        sys_argv = sys.argv
    ns = argparsing.parse_args(sys_argv)

    if ns.run_tests:
        run_tests()
    else:
        values = ns.args
        result = pizza.run(values)
        print(result)

    # TODO: return the right status code as appropriate.
    return 0

def main(sys_argv=None, from_source=False, **kwargs):
    """
    Arguments:

      from_source: whether this function is being called from a source
        checkout (e.g. by running `python test_molt.py` or
        `python -m molt.scripts.molt`).

    """
    status = main_inner(sys_argv)
    sys.exit(status)
