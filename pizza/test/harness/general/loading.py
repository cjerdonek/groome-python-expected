# encoding: utf-8

"""
Exposes a config_load_test() function and TestLoader subclass.

"""

import unittest

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
    if isinstance(tests, unittest.TestCase):
        yield tests
        return
    # Otherwise, we have an iterable or a TestSuite instance.
    for test in tests:
        for test2 in _test_gen(test):
            yield test2

def config_load_tests(loader, tests, pattern):
    """
    A unittest load_tests protocol implementation and helper.

    This function adds a test_config attribute to every test case with value
    loader.test_config and returns a unittest.TestSuite instance.

    This function lets one pass configuration data to TestCase classes without
    relying on global variables.  The configuration data can be accessed
    from within TestCase objects as `self.test_config`.

    To use this API, the unittest.TestLoader object that you pass to your
    unittest.TestProgram class must have a test_config attribute set to the
    object with which you would like to store configuration data.

    Usage
    -----

    First store configuration data in your test loader:

        loader = TestLoader()  # can be unittest.TestLoader
        loader.test_config = config_data
        unittest.main(testLoader=loader)

    Then from within the test modules that need it:

        from pizza.test.harness.general import config_load_tests

        load_tests = config_load_tests  # trigger the load_tests protocol.

    You can also use config_load_tests() in addition to an existing
    load_tests() implementation.  For example:

        def load_tests(loader, tests, pattern):
            # Do stuff: make and/or modify your tests, etc.
            return config_load_tests(loader, tests, pattern)

    """
    for test in _test_gen(tests):
        test.test_config = loader.test_config

    return unittest.TestSuite(tests)

class TestLoader(unittest.TestLoader):

    """
    This TestLoader differs from unittest's default TestLoader by providing
    additional diagnostic information when an AttributeError occurs while
    loading a module.

    Because of Python issue 7559 ( http://bugs.python.org/issue7559# ),
    the unittest module masks ImportErrors and the name of the offending
    module.  This TestLoader reports the name of the offending module
    along with a reminder that the AttributeError may be masking an
    ImportError.

    """

    def loadTestsFromNames(self, names, module=None):
        """
        Return a suite of all unit tests and doctests in the package.

        """
        suites = []

        for name in names:
            try:
                suite = self.loadTestsFromName(name, module)
            except AttributeError as err:
                msg = """AttributeError while loading unit tests from:
%s

Due to a bug in Python's unittest module, the AttributeError may be masking
an ImportError in the module being processed.
-->%s""" % (repr(name), str(err))
                # TODO [template]: add to the existing exception instead of
                # raising a new one.
                raise Exception(msg)
            suites.append(suite)

        return self.suiteClass(suites)
