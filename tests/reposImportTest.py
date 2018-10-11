# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import ScenarioTest
from azure_devtools.scenario_tests import AllowLargeResponse

from .utilities.helper import get_random_name

class ReposImportTests(ScenarioTest):
    @AllowLargeResponse(size_kb=3072)
    def test_repos_import_create(self):
        self.cmd('az dev configure --defaults instance=https://AzureDevOpsCliTest.visualstudio.com token=vj3ep2pg3fo6vxsklkwvkiy23dkbyynmfpg4vb66xniwr23zylla')
        self.cmd('az dev login --token vj3ep2pg3fo6vxsklkwvkiy23dkbyynmfpg4vb66xniwr23zylla')
        #Generate random repo name
        random_repo_name = get_random_name(8) 
        
        try:
            #Create a repo with random name
            create_repo_command = 'az repos repo create --detect off --name ' + random_repo_name +' --project ImportRepoTest --output json'
            repo_create_output = self.cmd(create_repo_command).get_output_in_json()
            created_repo_id = repo_create_output["id"]
            assert len(created_repo_id) > 0
            
            #Import repo
            import_repo_command = 'az repos import create --git-source-url https://dev.azure.com/AzureDevOpsCliTest/ImportRepoTest/_git/snakes-and-ladders --repository ' + created_repo_id + ' --project ImportRepoTest --detect Off --output json'
            import_repo_output = self.cmd(import_repo_command).get_output_in_json()
            import_repo_status = import_repo_output["status"]
            assert import_repo_status == 'completed'

        finally:
            #TestCleanup - Delete the temporary repo we created for the test
            list_repo_command = 'az repos repo list --project ImportRepoTest --output json --detect off'
            list_repo_output_before_delete = self.cmd(list_repo_command).get_output_in_json()
            delete_repo_command = 'az repos repo delete --detect off --id ' + created_repo_id + ' --project ImportRepoTest -y --output json'
            self.cmd(delete_repo_command)
            
            #Verify Deletion
            list_repo_output_after_delete = self.cmd(list_repo_command).get_output_in_json()
            assert len(list_repo_output_before_delete) == len(list_repo_output_after_delete) + 1
