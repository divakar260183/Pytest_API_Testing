import json

import requests

request_url = ""
module_name = "shifts"


def get_shifts_data(login, request_data):
    global request_url
    request_url = login.get_base_url() + request_data['path']
    get_shift_response = requests.get(url=request_url, headers=login.get_header_get_request())
    assert get_shift_response.status_code == 200, "Get Shifts Response is incorrect"
    return json.loads(get_shift_response.content)


def test_delete_shift(login, request_data):
    global request_url
    shifts_data_dict = get_shifts_data(login, request_data)
    for shift in shifts_data_dict['shifts']:
        if shift['name'] == request_data['requestBody']['name']:
            shift_delete_response = requests.delete(url=request_url + "/" + shift['id'],
                                                    headers=login.get_header_get_request())
            assert shift_delete_response.status_code == 204, "Shift Delete Response Code is incorrect"


def test_create_shift(login, request_data):
    shift_config_request_url = login.get_base_url() + request_data['configPath']
    shift_config_response = requests.get(shift_config_request_url, params=login.get_param(),
                                         headers=login.get_header_get_request())
    assert shift_config_response.status_code == 200, "Shift Config Response Code is not correct"
    shift_config_response_json_dict = json.loads(shift_config_response.content)
    if not shift_config_response_json_dict['isEnabled']:
        shift_config_response = requests.post(shift_config_request_url + ':enable',
                                              params=login.get_param(),
                                              headers=login.get_header_post_request())
        assert shift_config_response.status_code == 200
        shift_config_response_json_dict = json.loads(shift_config_response.content)
        assert shift_config_response_json_dict['isEnabled'] is True, "Shifts Feature is not enabled"
    agent_away_statuses_request_url = login.get_base_url() + request_data['agentAwayStatusesPath']
    agent_away_statuses_response = requests.get(agent_away_statuses_request_url, params=login.get_param(),
                                                headers=login.get_header_get_request())
    agent_away_statuses_dict = json.loads(agent_away_statuses_response.content)

    request_data['requestBody']['agentIds'][0] = login.get_agent_id()
    for x in range(len(request_data['requestBody']['shiftWorkingHours'])):
        request_data['requestBody']['shiftWorkingHours'][x]['agentAwayStatusId'] = agent_away_statuses_dict[0]['id']
    shift_creation_response = requests.post(request_url, json=request_data['requestBody'],
                                            headers=login.get_header_post_request(),
                                            params=login.get_param())
    assert shift_creation_response.status_code == 201, "Shift Creation Response Status Code is incorrect"
    shift_creation_response_dict = json.loads(shift_creation_response.content)
    shifts_data_dict = get_shifts_data(login, request_data)
    request_data['requestBody']['agentIds'][0] = login.get_agent_id()
    for shift in shifts_data_dict['shifts']:
        if shift['name'] == request_data['requestBody']['name'] and shift_creation_response_dict['id'] == shift['id']:
            assert shift['agentIds'] == request_data['requestBody']['agentIds'], "Agent Id is not matching"
            assert shift['timeZone'] == request_data['requestBody']['timeZone'], "Time Zone is not matching"
