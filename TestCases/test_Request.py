import requests


def test_api_request(login, request_url, request_type, request_header, request_param, request_body,
                     response_code, response_schema):
    response = None
    if request_type == 'GET':
        response = requests.get(request_url, headers=request_header)
    else:
        if request_type == 'POST':
            response = requests.post(request_url, json=request_body, headers=request_header)
        else:
            if request_type == 'DELETE':
                response = requests.delete(request_url, headers=request_header)
    assert response.status_code == response_code, "Response Code is not correct"
