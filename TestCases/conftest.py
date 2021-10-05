import json

import pytest

from login_func import AgentLogin
from util.file_reader import read_input_file, read_test_data_file, read_config_file
from util.utilities import get_value_for_key


def pytest_addoption(parser):
    parser.addoption('--environment', action="store", default="decoupling")


@pytest.fixture
def test_data(request):
    yield request.param


def pytest_generate_tests(metafunc):
    if 'test_data' not in metafunc.fixturenames:
        return
    read_input_file("InputData.csv", "Test_Data.json")
    input_data = read_test_data_file('Test_Data.json')
    data = input_data.get('data', None)
    metafunc.parametrize('test_data', data, indirect=True)


@pytest.fixture(scope='session')
def login(request):
    login = AgentLogin()
    environment = request.config.getoption("--environment")
    login.login(environment)
    yield login
    login.close()


@pytest.fixture
def request_url(request, test_data):
    config_data_json_dict = read_config_file('config.json')
    environment = request.config.getoption("--environment")
    base_url = get_value_for_key(config_data_json_dict['baseURL'], environment)
    url = base_url + test_data['path']
    return url


@pytest.fixture
def request_header(login, test_data):
    header_array = test_data['headers'].split(" ")
    if test_data['requestType'] == 'POST':
        header = {header_array[0]: header_array[1] + " " + login.get_token(),
                  header_array[3]: header_array[4]}
    else:
        header = {header_array[0]: header_array[1] + " " + login.get_token()}
    return header


@pytest.fixture
def request_param(login, test_data):
    param = None
    if 'param' in test_data:
        param_array = test_data['param'].split(" ")
        if param_array[0] == 'siteId':
            param = {'siteId': login.get_site_id()}
    return param


@pytest.fixture
def request_type(test_data):
    return test_data['requestType']


@pytest.fixture
def request_body(test_data):
    body = None
    if 'requestBody' in test_data:
        body = json.loads(test_data['requestBody'])
    return body


@pytest.fixture
def response_code(test_data):
    return int(test_data['responseCode'])


@pytest.fixture
def response_schema(test_data):
    response_schema = None
    if 'responseSchema' in test_data:
        response_schema = json.loads(test_data['responseSchema'])
    return response_schema


@pytest.fixture
def is_login_required(test_data):
    if 'isLoginRequired' in test_data:
        return bool(test_data['isLoginRequired'])


@pytest.fixture
def test_name(test_data):
    return test_data['TestName']


@pytest.fixture
def test_id(test_data):
    return test_data['TestId']
