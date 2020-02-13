import unittest

from filter_plugins.template_defaults import *


class TemplateDefaultsTest(unittest.TestCase):

    def test_init(self):
        module = FilterModule()
        filters = module.filters()

        self.assertEqual(filters.get('hetzner_firewall_template_defaults'), template_defaults)

    def test_template_defaults(self):
        templates = [{'name': 'foo'}]
        expected_templates = [{'whitelist_hos': False, 'is_default': False, 'name': 'foo', 'rules': {}}]

        actual_templates = template_defaults(templates)

        self.assertEqual(actual_templates, expected_templates)

    def test_rule_defaults(self):
        templates = [{'name': 'foo', 'rules': {'input': [{'name': 'bar'}]}}]
        expected_templates = [{'is_default': False,
                               'name': 'foo',
                               'rules': {'input': [{
                                                    'ip_version': 'ipv4',
                                                    'name': 'bar'
                                                    }]},
                               'whitelist_hos': False}]

        actual_templates = template_defaults(templates)

        self.assertEqual(actual_templates, expected_templates)
