import unittest

from filter_plugins.hetzner_firewall import *


class FirewallTest(unittest.TestCase):

    def test_init(self):
        module = FilterModule()
        filters = module.filters()

        self.assertEqual(filters.get('hetzner_firewall_change_set'), change_set.change_set)
        self.assertEqual(filters.get('hetzner_firewall_form_urlencode'), form_urlencode.form_urlencode)
        self.assertEqual(filters.get('hetzner_firewall_omit'), omit.omit)
