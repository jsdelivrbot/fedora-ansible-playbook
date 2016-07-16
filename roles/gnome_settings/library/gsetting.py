#!/usr/bin/python

from gi.repository import Gio
from ansible.module_utils.basic import *


def _set_boolean(schema, key, value):
    gsettings = Gio.Settings.new(schema)
    return gsettings.set_boolean(key, value)


def _set_int(schema, key, value):
    gsettings = Gio.Settings.new(schema)
    return gsettings.set_int(key, value)


def _set_array(schema, key, value):
    gsettings = Gio.Settings.new(schema)
    return gsettings.set_strv(key, value)


def _set_string(schema, key, value):
    gsettings = Gio.Settings.new(schema)
    return gsettings.set_string(key, value)


def _set_value(schema, key, value, type):
    set_type = {
        'int': _set_int,
        'boolean': _set_boolean,
        'array': _set_array,
        'string': _set_string,
    }
    func = set_type.get(type)

    return func(schema, key, value)


def _get_value(schema, key, type):
    gsettings = Gio.Settings.new(schema)
    return gsettings.get_value(key)


def main():
    module = AnsibleModule(
        argument_spec={
            'schema': {'required': True},
            'key': {'required': True},
            'value': {'required': True},
            'type': {'choices': ['string', 'boolean', 'int', 'array'], 'default': 'string'},
        },
        supports_check_mode=True,
    )
    schema = module.params['schema']
    key = module.params['key']
    value = module.params['value']
    type = module.params['type']

    if type == 'boolean':
        value = module.boolean(value)

    try:
        old_value = _get_value(schema, key, type)
        changed = old_value != value

        if changed and not module.check_mode:
            _set_value(schema, key, value, type)
    except:
        pass

    module.exit_json(changed=changed, schema=schema, key=key, value=value, type=type)


main()
