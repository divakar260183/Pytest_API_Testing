import json
import requests

from util.file_reader import read_test_data_file, read_config_file
from util.utilities import get_value_for_key


class AgentLogin:
    def __init__(self):
        self.__token = None
        self.__baseURL = None
        self.__header_get_request = None
        self.__header_post_request = None
        self.__site_id = None
        self.__agent_id = None

    def login(self, environment):
        config_data_json_dict = read_config_file('config.json')
        user_data_json_dict = read_test_data_file('userData.json')
        user_data_json = get_value_for_key(user_data_json_dict['userData'], environment)
        self.__baseURL = get_value_for_key(config_data_json_dict['baseURL'], environment)
        request_url = self.__baseURL + config_data_json_dict['loginAPIPath']
        login_response = requests.get(request_url, user_data_json)
        assert login_response.status_code == 200
        login_response_dict = json.loads(login_response.content)
        self.__token = login_response_dict['jwtToken']
        self.__site_id = login_response_dict['siteId']
        self.__agent_id = login_response_dict['agentId']
        self.__header_get_request = {"Authorization": "Bearer " + self.__token}
        self.__header_post_request = {"Authorization": "Bearer " + self.__token, "Content-Type": "application/json"}

    def get_token(self):
        return self.__token

    def get_base_url(self):
        return self.__baseURL

    def get_site_id(self):
        return self.__site_id

    def get_param(self):
        return {'siteId': self.__site_id}

    def get_agent_id(self):
        return self.__agent_id

    def get_header_get_request(self):
        return self.__header_get_request

    def get_header_post_request(self):
        return self.__header_post_request

    def close(self):
        pass
