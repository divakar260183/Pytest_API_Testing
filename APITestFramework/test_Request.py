import json
import requests

from APITestFramework.util.utilities import match_data


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
    assert response.status_code == response_code, "Response Code is not correct"
    assert(match_data(response_schema, json.loads(response.content))), "Expected data is not matched in actual data"

