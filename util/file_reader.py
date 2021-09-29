import csv
import json
import os
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
    dummy_json = read_test_data_file('DummyData.json')
    csv_file_path = get_test_data_file_with_csv_extension(csv_file_name)
    if os.path.exists(csv_file_path):
        with csv_file_path.open(mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            counter = -1
            for row in reader:
                if row['FieldType'] == "requestType":
                    counter = counter + 1
                dummy_json = get_value_from_field_value(row, dummy_json, counter)
                dummy_json = get_value_from_key_value(row, dummy_json, counter)
                if row['FieldType'] == 'End_Request':
                    if row['FieldValue'] == 'Add':
                        dummy_json1 = read_test_data_file('DummyData.json')
                        dummy_json['data'].append(dummy_json1['data'][0])
                    else:
                        if row['FieldValue'] == 'End':
                            break
        write_test_data_json(dummy_json, json_file_name)
    else:
        raise FileNotFoundError(csv_file_path, " does not exists in path ", csv_file_path)


def get_value_from_field_value(row, dummy_json, counter):
    field_type_list = ["requestType", "path", "requestBody", "responseCode", "responseSchema"]
    if row['FieldType'] in field_type_list:
        data = row['FieldValue']
        if data == "":
            del dummy_json['data'][counter][row['FieldType']]
        else:
            dummy_json['data'][counter][row['FieldType']] = data
    return dummy_json


def get_value_from_key_value(row, dummy_json, counter):
    field_type_list = ["headers", "param"]
    if row['FieldType'] in field_type_list:
        key_data = row['Key']
        value_data = row['Value']
        if key_data == "" and value_data == "":
            del dummy_json['data'][counter][row['FieldType']]
        else:
            dummy_json['data'][counter][row['FieldType']] = key_data + " " + value_data
    return dummy_json


def write_test_data_json(dummy_json, json_file_name):
    json_file_path = get_test_data_file_with_json_extension(json_file_name)
    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    with open(json_file_path, 'w') as json_file:
        json_file.write(json.dumps(dummy_json, sort_keys=False, indent=4))
