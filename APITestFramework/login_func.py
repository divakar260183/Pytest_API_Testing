import json
import requests

from APITestFramework.util.file_reader import read_config_file
from APITestFramework.util.utilities import get_value_for_key


class AgentLogin:
    def __init__(self):
        self.__token = None
        self.__site_id = None
        self.__agent_id = None

    def login(self, environment):
        config_data_json_dict = read_config_file('environments.json')
        user_data_json_dict = read_config_file('agents.json')
        user_data_json = get_value_for_key(user_data_json_dict['userData'], environment)
        base_url = get_value_for_key(config_data_json_dict['baseURL'], environment)
        request_url = base_url + config_data_json_dict['loginAPIPath']
        login_response = requests.get(request_url, user_data_json)
        assert login_response.status_code == 200
        login_response_dict = json.loads(login_response.content)
        self.__token = login_response_dict['jwtToken']
        self.__site_id = login_response_dict['siteId']
        self.__agent_id = login_response_dict['agentId']

    def get_token(self):
        return self.__token

    def get_site_id(self):
        return self.__site_id

    def get_agent_id(self):
        return self.__agent_id

    def close(self):
        pass
