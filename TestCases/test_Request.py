import json

import requests
from genson import SchemaBuilder
from jsonschema import validate


def validate_schema(actual_data, expected_data):
    builder = SchemaBuilder()
    builder.add_object(expected_data)
    schema = builder.to_schema()
    if isinstance(actual_data, list):
        for data in actual_data:
            validate(instance=data, schema=schema)
    else:
        validate(instance=expected_data, schema=schema)


def test_api_request(request_url, request_type, request_header, request_param, request_body,
                     response_code, response_schema, is_login_required):
    response = None
    if is_login_required:
        if request_type == 'GET':
            response = requests.get(request_url, headers=request_header)
        elif request_type == 'POST':
            response = requests.post(request_url, json=request_body, headers=request_header,
                                     params=request_param)
        elif request_type == 'DELETE':
            response = requests.delete(request_url, headers=request_header)
    else:
        if request_type == 'GET':
            response = requests.get(request_url)
        elif request_type == 'POST':
            response = requests.post(request_url, json=request_body)
        elif request_type == 'DELETE':
            response = requests.delete(request_url)
    print("content :", response.content)
    print("response schema :", response_schema)
    assert response.status_code == response_code, "Response Code is not correct"
    validate_schema(json.loads(response.content), response_schema)
