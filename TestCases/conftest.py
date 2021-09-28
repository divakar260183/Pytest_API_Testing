import pytest

from login_func import AgentLogin
from util.file_reader import read_test_data_file, read_input_file
from util.utilities import get_value_for_key


def pytest_addoption(parser):
    parser.addoption('--environment', action="store", default="decoupling")


@pytest.fixture(scope='session')
def login(request):
    login = AgentLogin()
    environment = request.config.getoption("--environment")
    login.login(environment)
    yield login
    login.close()


@pytest.fixture(scope="class")
def test_data():
    testdata = read_test_data_file('testData.json')
    yield testdata


@pytest.fixture(scope="function")
def request_data(test_data):
    test_args = test_data
    yield test_args


def pytest_generate_tests(metafunc):
    if 'test_data' not in metafunc.fixturenames:
        return
    read_input_file("InputData.csv", "Test_Data.json")
    testdata = read_test_data_file('testData.json')
    data = get_value_for_key(testdata.get('data', None), metafunc.module.module_name)
    metafunc.parametrize('test_data', data)
