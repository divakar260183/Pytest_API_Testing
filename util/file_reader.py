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
                if row['FieldType'] == "Request Type":
                    request_type = row['FieldValue']
                    counter = counter + 1
                    dummy_json['data'][counter]['requestType'] = request_type
                else:
                    if row['FieldType'] == "API Path":
                        api_path = row['FieldValue']
                        dummy_json['data'][counter]['path'] = api_path
                    else:
                        if row['FieldType'] == "Headers":
                            header_key = row['Key']
                            header_value = row['Value']
                            if header_key == "" and header_value == "":
                                del dummy_json['data'][counter]['headers']
                            else:
                                dummy_json['data'][counter]['headers'] = header_key + " " + header_value
                        else:
                            if row['FieldType'] == "Response Code":
                                response_code = row['FieldValue']
                                dummy_json['data'][counter]['responseCode'] = response_code
                            else:
                                if row['FieldType'] == "Param":
                                    param_key = row['Key']
                                    param_value = row['Value']
                                    if param_key == "" and param_value == "":
                                        del dummy_json['data'][counter]['param']
                                    else:
                                        dummy_json['data'][counter]['param'] = param_key + " " + param_value
                                else:
                                    if row['FieldType'] == "Request Body":
                                        req_body = row['FieldValue']
                                        if req_body == "":
                                            del dummy_json['data'][counter]['requestBody']
                                        else:
                                            dummy_json['data'][counter]['requestBody'] = req_body
                                    else:
                                        if row['FieldType'] == "Response Schema":
                                            resp_schema = row['FieldValue']
                                            if resp_schema == "":
                                                del dummy_json['data'][counter]['responseSchema']
                                            else:
                                                dummy_json['data'][counter]['responseSchema'] = resp_schema
                                        else:
                                            if row['FieldType'] == 'End_Request':
                                                if row['FieldValue'] == 'Add':
                                                    dummy_json1 = read_test_data_file('DummyData.json')
                                                    dummy_json['data'].append(dummy_json1['data'][0])
                                                else:
                                                    if row['FieldValue'] == 'End':
                                                        break
        json_file_path = get_test_data_file_with_json_extension(json_file_name)
        mode = 'a' if os.path.exists(json_file_path) else 'w'
        with open(json_file_path, mode) as json_file:
            json_file.write(json.dumps(dummy_json, sort_keys=False, indent=4))
    else:
        raise FileNotFoundError(csv_file_path, " does not exists in path ", csv_file_path)