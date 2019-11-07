import unittest

from filter_plugins.template_defaults import *


class TemplateDefaultsTest(unittest.TestCase):

    def test_template_defaults(self):
        templates = [{'name': 'foo'}]
        expected_templates = [{'whitelist_hos': False, 'is_default': False, 'name': 'foo', 'rules': {}}]

        actual_templates = template_defaults(templates)

        self.assertEqual(actual_templates, expected_templates)

    def test_rule_defaults(self):
        templates = [{'name': 'foo', 'rules': {'input': [{'name': 'bar'}]}}]
        expected_templates = [{'is_default': False,
                               'name': 'foo',
                               'rules': {'input': [{'dst_ip': None,
                                                    'dst_port': None,
                                                    'ip_version': 'ipv4',
                                                    'name': 'bar',
                                                    'packet_length': None,
                                                    'protocol': None,
                                                    'src_ip': None,
                                                    'src_port': None,
                                                    'tcp_flags': None}]},
                               'whitelist_hos': False}]

        actual_templates = template_defaults(templates)

        self.assertEqual(actual_templates, expected_templates)
