import json
import os

import yaml


class Symbol:
    WORKDIR = '$$workdir'
    IMPORT = '$$import'


def read(filepath: str):
    handler = None
    if filepath.endswith('.yaml'):
        handler = yaml.safe_load
    elif filepath.endswith('.json'):
        handler = json.load

    with open(filepath, 'r+') as f:
        config = handler(f)

    workdir = os.path.dirname(filepath)
    if Symbol.IMPORT in config:
        if not isinstance(config[Symbol.IMPORT], list):
            config[Symbol.IMPORT] = [config[Symbol.IMPORT]]
        for index in range(len(config[Symbol.IMPORT])):
            config[Symbol.IMPORT][index] = os.path.join(workdir, config[Symbol.IMPORT][index])

    return config


def merge(config_base, config_add: dict):
    if config_base is None:
        return config_add

    for key in config_add:
        if key in config_base:
            if isinstance(config_base[key], dict) and isinstance(config_add[key], dict):
                merge(config_base[key], config_add[key])
            else:
                config_base[key] = config_add[key]
        else:
            config_base[key] = config_add[key]

    return config_base


def parse(filepath: str, path_circle=None):
    filepath = os.path.abspath(filepath)

    path_circle = path_circle or set()
    path_circle.add(filepath)

    config = read(filepath)

    if Symbol.IMPORT in config:
        import_config = None
        for import_filepath in config[Symbol.IMPORT]:
            if import_filepath in path_circle:
                raise ValueError(f'Circular import detected: {import_filepath}')
            current_config = parse(import_filepath, path_circle)
            import_config = merge(import_config, current_config)

        config = merge(import_config, config)
        del config[Symbol.IMPORT]

    path_circle.remove(filepath)
    return config
