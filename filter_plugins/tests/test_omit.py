import unittest

from filter_plugins.omit import *


class OmitTest(unittest.TestCase):

    def test_template_defaults(self):
        obj = [{'foo': 'a', 'bar': 'b'}]
        expected_obj = [{'foo': 'a'}]

        actual_obj = omit(obj, ['bar'])

        self.assertEqual(actual_obj, expected_obj)
