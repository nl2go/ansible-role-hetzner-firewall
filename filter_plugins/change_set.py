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
    elif is_equal_obj(local_obj, origin_obj):
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


def is_equal_obj(local_obj, origin_obj):
    if is_all_empty(local_obj, origin_obj):
        return True

    if is_any_bool(local_obj, origin_obj):
        return is_equal_bool(local_obj, origin_obj)

    if is_all_dict(local_obj, origin_obj):
        for key, local_value in local_obj.items():
            origin_value = origin_obj.get(key)
            if not is_equal_obj(local_value, origin_value):
                return False
    elif is_list(local_obj) and is_list(origin_obj):
        for i in range(len(local_obj)):
            local_value = local_obj[i]
            origin_value = origin_obj[i]
            if not is_equal_obj(local_value, origin_value):
                return False
    elif local_obj != origin_obj:
        return False

    return True


def is_equal_bool(left, right):
    if not isinstance(left, bool):
        left = str2bool(left)
    if not isinstance(right, bool):
        right = str2bool(right)
    return left is right


def is_any_bool(left, right):
    return isinstance(left, bool) or isinstance(right, bool)


def is_all_empty(left, right):
    return is_empty(left) and is_empty(right)


def is_all_dict(left, right):
    return is_dict(left) and is_dict(right)


def is_all_list(left, right):
    return is_list(left) and is_list(right)


def is_dict(obj):
    return isinstance(obj, dict)


def is_list(obj):
    return isinstance(obj, list)


def is_empty(value):
    if value:
        return False
    return True


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
    result_dict = {
        ACTION_CREATE: [],
        ACTION_UPDATE: [],
        ACTION_DELETE: [],
        ACTION_NOOP: []
    }

    if not local:
        return result_dict

    if is_dict(local):
        if not isinstance(origin, dict):
            origin = {}
        change_set_item(result_dict, local, origin)
        return result_dict

    if is_list(local):
        local_dict = array_to_dict(local, attr)

        if not isinstance(origin, list):
            origin_dict = {}
        else:
            origin_dict = array_to_dict(origin, attr)

        change_set_items(result_dict, local_dict, origin_dict)
        return result_dict

    raise TypeError('Can not build change set for given objects: ' + str(local) + ", " + str(origin))



def change_set_item(result_dict, local_obj, origin_obj):
    obj = copy.deepcopy(local_obj)
    state = remove_state(obj)
    action = get_action(obj, origin_obj, state)

    obj = update_obj(obj, origin_obj)
    result_dict[action].append(obj)


def change_set_items(result_dict, local_dict, origin_dict):
    for obj_key, local_obj in local_dict.items():
        origin_obj = origin_dict.get(obj_key)
        change_set_item(result_dict, local_obj, origin_obj)


class FilterModule(object):

    def filters(self):
        return {
            'hetzner_firewall_change_set': change_set
        }
