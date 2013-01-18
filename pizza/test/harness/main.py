"""
Exposes the function that the run_test command-line option should call.

"""

import unittest
import pizza.test.harness.general.loading as loading

class TestConfig(object):

    def __init__(self, temp_dir):
        """
        Arguments:

          temp_dir: the sandbox directory that test cases can use for writing
            temporary files to the file system.

        """
        self.temp_dir = temp_dir


def run_tests():
    # TODO: pass the correct directory.
    config = TestConfig(temp_dir="TODO")
    loader = loading.TestLoader()
    loader.test_config = config
    unittest.main(module="pizza.test.pizza.test_pizza", argv=["prog"],
                  testLoader=loader)
