import unittest

from filter_plugins.change_set import *


class ChangeSetTest(unittest.TestCase):

    default_change_set = {
        'create': [],
        'update': [],
        'delete': [],
        'noop': []
    }

    def test_set_action_create(self):
        local = [{'foo': 'bar', 'name': 'obj1'}]
        origin = []
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'create': [{'foo': 'bar', 'name': 'obj1'}],
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_create_if_state_present(self):
        local = [{'foo': 'bar', 'name': 'obj1', 'state': 'present'}]
        origin = []
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'create': [{'foo': 'bar', 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_state_absent_no_origin(self):
        local = [{'foo': 'bar', 'name': 'obj1', 'state': 'absent'}]
        origin = []
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({

            'noop': [{'foo': 'bar', 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_delete_if_state_absent(self):
        local = [{'foo': 'bar', 'name': 'obj1', 'state': 'absent'}]
        origin = [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'delete': [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_update(self):
        local = [{'foo': 'baz', 'name': 'obj1'}]
        origin = [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'update': [{'foo': 'baz', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_bool_str(self):
        local = [{'foo': 'true', 'name': 'obj1'}]
        origin = [{'foo': True, 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'true', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_field_empty_dict_or_list(self):
        local = [{'empty': [], 'foo': 'true', 'name': 'obj1'}]
        origin = [{'empty': {}, 'foo': True, 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'empty': [], 'foo': 'true', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop(self):
        local = [{'foo': 'bar', 'name': 'obj1'}]
        origin = [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'bar', 'id': 1, 'name': 'obj1'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_state_present(self):
        local = [{'foo': 'bar', 'name': 'obj2', 'state': 'present'}]
        origin = [{'foo': 'bar', 'id': 1, 'name': 'obj2'}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'bar', 'id': 1, 'name': 'obj2'}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)

    def test_set_action_noop_if_origin_nested_object_has_additional_properties(self):
        local = [{'foo': 'bar', 'name': 'obj2', 'items': [{'foo': 'bar'}]}]
        origin = [{'foo': 'bar', 'name': 'obj2', 'items': [{'foo': 'bar', 'foz':'baz'}]}]
        expected_change_set = copy.deepcopy(self.default_change_set)
        expected_change_set.update({
            'noop': [{'foo': 'bar', 'name': 'obj2', 'items': [{'foo': 'bar'}]}]
        })

        actual_change_set = change_set(local, origin)

        self.assertEqual(actual_change_set, expected_change_set)
