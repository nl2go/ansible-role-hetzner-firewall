import unittest

from filter_plugins.form_urlencode import *


class FormUrlencodeTest(unittest.TestCase):

    def test_urlencode_bool_true(self):
        obj = True

        encoded_str = form_urlencode(obj)

        self.assertEqual(encoded_str, 'true&')

    def test_urlencode_bool_false(self):
        obj = False

        encoded_str = form_urlencode(obj)

        self.assertEqual(encoded_str, 'false&')

    def test_urlencode_obj(self):
        obj = {
            "id": 123,
            "name": "rule 1"
        }
        expected_encoded_str = 'id=123&name=rule%201&'

        encoded_str = form_urlencode(obj)

        self.assertEqual(encoded_str, expected_encoded_str)

    def test_urlencode_list(self):
        obj = ["foo", "bar"]
        expected_encoded_str = '0=foo&1=bar&'

        encoded_str = form_urlencode(obj)

        self.assertEqual(encoded_str, expected_encoded_str)

    def test_urlencode_nested_obj(self):
        obj = {
            "id": 123,
            "whitelist_hos": "true",
            "is_default": "false",
            "rules": {
                "input": [{
                    "ip_version": "ipv4",
                    "src_port": None,
                    "name": "rule 1",
                    "src_ip": "1.1.1.1",
                    "dst_port": "80",
                    "action": "accept"
                }]
            }
        }
        expected_encoded_str = 'id=123&whitelist_hos=true&is_default=false&rules[input][0][ip_version]=ipv4&rules[input][0][src_port]=null&rules[input][0][name]=rule%201&rules[input][0][src_ip]=1.1.1.1&rules[input][0][dst_port]=80&rules[input][0][action]=accept&'

        encoded_str = form_urlencode(obj)

        self.assertEqual(encoded_str, expected_encoded_str)
