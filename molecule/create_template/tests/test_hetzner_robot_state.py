import os
import requests
import unittest

from requests.auth import HTTPBasicAuth


class DefaultTest(unittest.TestCase):
    hetzner_robot_base_url = os.getenv(
        'HETZNER_ROBOT_BASE_URL', 'http://localhost:3000'
    )
    auth = HTTPBasicAuth('robot', 'secret')

    def test_firewall_template_created(self):
        response = requests.get(self.hetzner_robot_base_url +
                                "/firewall/template", auth=self.auth)
        self.maxDiff = None
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[1], {
            'firewall_template': {
                'id': 2,
                'name': 'Created Template',
                'whitelist_hos': 'true',
                'is_default': 'false',
                'rules': {
                    'input': [{
                        'action': 'accept',
                        'ip_version': 'ipv4',
                        'name': 'Allow all'}]
                }}})

    def test_firewall_amount_unchanged(self):
        response = requests.get(self.hetzner_robot_base_url +
                                "/firewall", auth=self.auth)
        self.assertEqual(len(response.json()), 0)
