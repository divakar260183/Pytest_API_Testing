import os
import urllib

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from util.file_reader import get_test_data_file_with_csv_extension


def download_test_data_file(file_name):

    personal_token = 'rkrs5td4ziemjibdsdbsqye43fgmnbttml7lm44lgafmsstugzoa'
    organization_url = 'https://dev.azure.com/Comm100'

    # create a connection to the org
    credentials = BasicAuthentication('', personal_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    # Get a client (the "core" client provides access to projects, teams, etc)
    core_client = connection.clients.get_core_client()

    # Get the first page of projects
    get_projects_response = core_client.get_projects()
    index = 0
    found = False
    while get_projects_response is not None:
        for project in get_projects_response.value:
            print("[" + str(index) + "] " + project.name)
            index += 1
            if project.name == "APIAutomation":
                # call to access wiki page
                file_path = get_test_data_file_with_csv_extension(file_name)
                if os.path.exists(file_path):
                    # code for removing the file
                    os.remove(file_path)
                # create a file at the source path
                dls = "https://dev.azure.com/Comm100/f025d0a2-6ccc-416a-a40f-da05bf20f24f/_apis/git/repositories/770f79cc-31cd-450e-8765-4d813bc280ad/Items?path=/.attachments/InputData-444a6ab6-4522-42b0-82a2-f7d4e67bcd91.csv&download=false&resolveLfs=true&%24format=octetStream&api-version=5.0-preview.1&sanitize=true&versionDescriptor.version=wikiMaster"
                urllib.request.urlretrieve(dls, file_path)
                found = True
                break
        if found is False and get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
            # Get the next page of projects
            get_projects_response = core_client.get_projects(
                continuation_token=get_projects_response.continuation_token)
        else:
            # All projects have been retrieved
            get_projects_response = None

