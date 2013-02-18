"""
Tests of pizza.pizza.

"""

import unittest
import pizza.test.harness.general.loading as loading

# TODO [template]: use this only where it makes sense.
load_tests = loading.config_load_tests

class MainTestCase(unittest.TestCase):

    def test(self):
        self.assertEqual(self.test_config.temp_dir, "TODO")
        self.assertEqual(1, 1)
