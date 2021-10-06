import json
import requests
module_name = "channels"


def get_channel_accounts(request_url, request_header):
    channel_accounts_response = requests.get(url=request_url, headers=request_header)
    assert channel_accounts_response.status_code == 200, "Get Channel Accounts Response Code is not correct"
    return json.loads(channel_accounts_response.content)


def test_delete_channel_account(request_url, request_header, request_body):
    channel_accounts_response_dict = get_channel_accounts(request_url, request_header)
    for account in channel_accounts_response_dict:
        if account['appId'] == request_body['appId'] \
                and account['originalAccountId'] == request_body['originalAccountId'] and \
                account['name'] == request_body['name']:
            channel_accounts_delete_response = requests.delete(url=request_url + "/" + account['id'],
                                                               headers=request_header)
            assert channel_accounts_delete_response.status_code == 204, "Shift Delete Response Code is incorrect"


# def test_create_channel_account(login, request_data):
#     request_body = request_data['requestBody']
#     channel_account_creation_response = requests.post(request_url, json=request_body,
#                                                       headers=login.get_header_post_request())
#     assert channel_account_creation_response.status_code == 201, "Channel Account Creation Response Code is not Correct"
#     channel_account_creation_response_dict = json.loads(channel_account_creation_response.content)
#     channel_accounts_response_dict = get_channel_accounts(login, request_data)
#     for account in channel_accounts_response_dict:
#         if account['appId'] == request_data['requestBody']['appId'] \
#                 and account['originalAccountId'] == request_data['requestBody']['originalAccountId'] \
#                 and account['id'] == channel_account_creation_response_dict['id']:
#             assert account['name'] == request_data['requestBody']['name'], \
#                 "Account Name of New Created Channel Account does not match"
