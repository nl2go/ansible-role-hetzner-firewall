#!/usr/bin/python

import copy

STATE_KEY = 'state'
STATE_PRESENT = 'present'
STATE_ABSENT = 'absent'

ACTION_KEY = 'action'
ACTION_CREATE = 'create'
ACTION_UPDATE = 'update'
ACTION_NOOP = 'noop'
ACTION_DELETE = 'delete'

OBJ_KEY = 'value'


def array_to_dict(obj_array, attr='name'):
    obj_dict = {}

    for obj in obj_array:
        key = obj.get(attr)
        obj_dict[key] = obj

    return obj_dict


def dict_to_array(obj_dict):
    obj_array = []

    for obj_key, obj_value in obj_dict.iteritems():
        obj_array.append(obj_value)

    return obj_array


def get_action(local_obj, origin_obj, state):
    if not origin_obj:
        if state == STATE_PRESENT:
            return ACTION_CREATE
        else:
            return ACTION_NOOP
    elif is_equal_intersection(local_obj, origin_obj):
        if state == STATE_PRESENT:
            return ACTION_NOOP
        else:
            return ACTION_DELETE
    else:
        if state == STATE_PRESENT:
            return ACTION_UPDATE
        else:
            return ACTION_DELETE


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def is_equal_intersection(local_obj, origin_obj):
    for key, value in local_obj.items():
        origin_value = origin_obj.get(key)
        if isinstance(origin_value, bool):
            value = str2bool(value)
        elif isinstance(value, bool):
            origin_value = str2bool(origin_value)

        if is_empty_dict_or_list(origin_value) and is_empty_dict_or_list(value):
            continue
        elif origin_value != value:
            return False

    return True


def is_empty_dict_or_list(value):
    return isinstance(value, dict) or isinstance(value, list)


def remove_state(obj):
    return obj.pop(STATE_KEY, STATE_PRESENT)


def update_obj(obj, origin_obj):
    if origin_obj:
        updated_obj = copy.deepcopy(origin_obj)
        updated_obj.update(obj)
    else:
        updated_obj = obj

    return updated_obj


def change_set(local, origin, attr='name'):
    if not local:
        return []

    local_dict = array_to_dict(local, attr)

    if not isinstance(origin, list):
        origin_dict = {}
    else:
        origin_dict = array_to_dict(origin, attr)

    change_set_dict = {
        ACTION_CREATE: [],
        ACTION_UPDATE: [],
        ACTION_DELETE: [],
        ACTION_NOOP: []
    }

    for obj_key, local_obj in local_dict.items():
        origin_obj = origin_dict.get(obj_key)
        obj = copy.deepcopy(local_obj)
        state = remove_state(obj)
        action = get_action(obj, origin_obj, state)

        obj = update_obj(obj, origin_obj)

        change_set_dict[action].append(obj)

    return change_set_dict


class FilterModule(object):

    def filters(self):
        return {
            'hetzner_firewall_change_set': change_set
        }
