import requests


def test_api_request(login, request_url, test_data, request_header, request_param):
    response = None
    if test_data['requestType'] == 'GET':
        response = requests.get(request_url, headers=request_header)
    else:
        if test_data['requestType'] == 'POST':
            response = requests.post(request_url, json=test_data['requestBody'], headers=request_header)
        else:
            if test_data['requestType'] == 'DELETE':
                response = requests.delete(request_url, headers=request_header)
    print("response.code :", response.status_code)
