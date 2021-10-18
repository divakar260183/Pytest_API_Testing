import csv
import json
import os
from pathlib import Path

TEST_DATA_BASE_PATH = Path.cwd().joinpath('TestCases')
CONFIG_DATA_BASE_PATH = Path.cwd().joinpath('APITestFramework/environment')


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


def get_test_data_file_with_csv_extension(file_name):
    if '.csv' in file_name:
        path = TEST_DATA_BASE_PATH.joinpath(file_name)
    else:
        path = TEST_DATA_BASE_PATH.joinpath(f'{file_name}.csv')
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


# Read CSV File
def read_input_file(csv_file_name, json_file_name):
    csv_file_path = get_test_data_file_with_csv_extension(csv_file_name)
    if os.path.exists(csv_file_path):
        with csv_file_path.open(mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            data = []
            for row in reader:
                data_row = {}
                for columns in reader.fieldnames:
                    if row[columns]:
                        data_row[columns] = row[columns]
                data.append(data_row)
            json_dump = {"data": data}
        write_test_data_json(json_dump, json_file_name)
    else:
        raise FileNotFoundError(csv_file_path, " does not exists in path ", csv_file_path)


def write_test_data_json(data, json_file_name):
    json_file_path = get_test_data_file_with_json_extension(json_file_name)
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    with open(json_file_path, 'w') as json_file:
        json_file.write(json.dumps(data, sort_keys=False, indent=4))
