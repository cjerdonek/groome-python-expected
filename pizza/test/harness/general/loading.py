# encoding: utf-8

"""
Exposes a load_tests implementation for configuring tests.

This module exposes a function config_load_tests() that lets one pass
configuration data to unittest.TestCase classes without relying on
global variables.  The configuration data can be accessed from within
TestCase objects as `self.test_config`.

Usage:

Simply include the following (or something equivalent):

    from pizza.test.harness.general import config_load_tests

    load_tests = config_load_tests  # trigger the load_tests protocol.

You can also use config_load_tests() in addition to an existing load_tests()
implementation.  For example:

    def load_tests(loader, tests, pattern):
        # Do stuff: make and/or modify your tests, etc.
        return config_load_tests(loader, tests, pattern)

"""

from unittest import TestCase, TestSuite

def _test_gen(tests):
    """
    Return a generator over all TestCase instances recursively in tests.

    Sample usage--

    for test in _test_gen(tests):
        print test

    The point is that TestSuite.__iter__() only provides direct access to
    child tests and not to grandchild tests, etc. which this function
    provides.  Also see--

      http://docs.python.org/library/unittest.html#unittest.TestSuite.__iter__

    Arguments:

      tests: a TestCase instance, TestSuite instance, or iterable of
        TestCase and TestSuite instances.

    """
    if isinstance(tests, TestCase):
        yield tests
        return
    # Otherwise, we have an iterable or a TestSuite instance.
    for test in tests:
        for test2 in _test_gen(test):
            yield test2

def config_load_tests(loader, tests, pattern):
    """
    A load_tests protocol implementation that sets the test_config attribute.

    Returns a unittest.TestSuite instance.

    See the docstring of this module for more information.

    """
    for test in _test_gen(tests):
        test.test_config = loader.test_config

    return TestSuite(tests)
