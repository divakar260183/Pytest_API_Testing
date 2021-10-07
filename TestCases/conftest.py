import json

import pytest

from login_func import AgentLogin
from util.file_reader import read_input_file, read_test_data_file, read_config_file
from util.utilities import get_value_for_key


def pytest_addoption(parser):
    parser.addoption('--environment', action="store", default="decoupling")


@pytest.fixture
def request_data(request):
    yield request.param


def pytest_generate_tests(metafunc):
    if 'request_data' not in metafunc.fixturenames:
        return
    read_input_file("InputData.csv", "Test_Data.json")
    input_data = read_test_data_file('Test_Data.json')
    data = input_data.get('data', None)
    metafunc.parametrize('request_data', data, indirect=True)


@pytest.fixture(scope='session')
def login(request):
    login = AgentLogin()
    environment = request.config.getoption("--environment")
    login.login(environment)
    yield login
    login.close()


@pytest.fixture
def request_url(request, request_data):
    config_data_json_dict = read_config_file('config.json')
    environment = request.config.getoption("--environment")
    base_url = get_value_for_key(config_data_json_dict['baseURL'], environment)
    url = base_url + request_data['path']
    return url


@pytest.fixture
def request_header(login, request_data):
    header_array = request_data['headers'].split(" ")
    if header_array.__len__() == 5:
        header = {header_array[0]: header_array[1] + " " + login.get_token(),
                  header_array[3]: header_array[4]}
    elif header_array.__len__() == 3:
        header = {header_array[0]: header_array[1] + " " + login.get_token()}
    else:
        header = None
    return header


@pytest.fixture
def request_param(login, request_data):
    param = None
    if 'param' in request_data:
        param_array = request_data['param'].split(" ")
        if param_array[0] == 'siteId':
            param = {'siteId': login.get_site_id()}
    return param


@pytest.fixture
def request_type(request_data):
    return request_data['requestType']


@pytest.fixture
def request_body(request_data):
    body = None
    if 'requestBody' in request_data:
        body = json.loads(request_data['requestBody'])
    return body


@pytest.fixture
def response_code(request_data):
    return int(request_data['responseCode'])


@pytest.fixture
def response_schema(request_data):
    response_schema = None
    if 'responseSchema' in request_data:
        response_schema = json.loads(request_data['responseSchema'])
    return response_schema


@pytest.fixture
def is_login_required(request_data):
    if 'isLoginRequired' in request_data:
        return bool(request_data['isLoginRequired'])


@pytest.fixture
def scenario_name(request_data):
    return request_data['ScenarioName']


@pytest.fixture
def scenario_id(request_data):
    return request_data['ScenarioId']
