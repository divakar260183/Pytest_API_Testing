import json
from pathlib import Path

TEST_DATA_BASE_PATH = Path.cwd().joinpath('testData')
CONFIG_DATA_BASE_PATH = Path.cwd().joinpath('config')


def read_test_data_file(file_name):
    path = get_test_data_file_with_json_extension(file_name)
    with path.open(mode='r') as f:
        return json.load(f)


def get_test_data_file_with_json_extension(file_name):
    if '.json' in file_name:
        path = TEST_DATA_BASE_PATH.joinpath(file_name)
    else:
        path = TEST_DATA_BASE_PATH.joinpath(f'{file_name}.json')
    return path


def read_config_file(file_name):
    path = get_config_file_with_json_extension(file_name)
    with path.open(mode='r') as f:
        return json.load(f)


def get_config_file_with_json_extension(file_name):
    if '.json' in file_name:
        path = CONFIG_DATA_BASE_PATH.joinpath(file_name)
    else:
        path = CONFIG_DATA_BASE_PATH.joinpath(f'{file_name}.json')
    return path
