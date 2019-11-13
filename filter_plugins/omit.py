#!/usr/bin/python


def omit(obj, attributes):
    if isinstance(obj, dict):
        return omit_dict(obj, attributes)
    elif isinstance(obj, list):
        return omit_list(obj, attributes)

    raise TypeError('Given object is whether a dictionary nor a list.')


def omit_dict(obj_dict, attributes):
    result_obj = {}
    for key, value in obj_dict.items():
        if key not in attributes:
            result_obj[key] = value
    return result_obj


def omit_list(obj_list, attributes):
    result_list = []
    for obj in obj_list:
        result_list.append(omit_dict(obj, attributes))
    return result_list


class FilterModule(object):

    def filters(self):
        return {
            'hetzner_firewall_omit': omit
        }
