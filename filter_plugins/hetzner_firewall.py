from ansible_filter import change_set
from ansible_filter import form_urlencode
from ansible_filter import omit


class FilterModule(object):

    def filters(self):
        return {
            'hetzner_firewall_change_set': change_set.change_set,
            'hetzner_firewall_form_urlencode': form_urlencode.form_urlencode,
            'hetzner_firewall_omit': omit.omit
        }
