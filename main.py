
"""
Example of authenticating with SPN + Secret
Can be expanded to retrieve values from Key Vault or other sources
If using Current User Credentials, ensure you have logged in using 'az login' or 'az login --use-device-code --allow-no-subscriptions' and have the required permissions to the Fabric Workspace

Pre-requisites:
pip install -r requirements.txt

"""

import os

# Setting parameters
environment = "" 
repository_directory = os.path.join(os.path.dirname(__file__), "workspace") # Path to the workspace directory

from azure.identity import ClientSecretCredential, DefaultAzureCredential
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items

# Authentication to Azure
if os.getenv("GITHUB_ACTIONS") == "true": # Check if running in GitHub Actions to Use Service Principal Authentication otherwise use DefaultAzureCredential
    print("Running from GitHub Actions - Using Service Principal Authentication")
    workspace_id = os.getenv("FABRIC_WORKSPACE_ID") 
    client_id = os.getenv("AZURE_CLIENT_ID") # Secret defined in GitHub - Service Principal ID
    client_secret = os.getenv("AZURE_CLIENT_SECRET") # Secret defined in GitHub - Service Principal Secret
    tenant_id = os.getenv("AZURE_TENANT_ID") # Secret defined in GitHub - Tenant ID
    if not all([client_id, client_secret, tenant_id]):
        raise ValueError("Missing Azure credentials")

    token_credential = ClientSecretCredential(
        client_id=client_id, client_secret=client_secret, tenant_id=tenant_id
    )
    item_type_in_scope = ["Notebook", "Environment"]
else:
    print("Running from Local - Using Current User Credentials")
    token_credential = DefaultAzureCredential() 
    workspace_id = input("Enter your Workspace ID: ") # Fabric Workspace ID
    item_type_in_scope = ["Notebook", "Environment", "DataPipeline"]

# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    repository_directory=repository_directory,
    item_type_in_scope=item_type_in_scope,
)

# Publish all items defined in item_type_in_scope
publish_all_items(target_workspace)

# Unpublish all items defined in item_type_in_scope not found in repository
unpublish_all_orphan_items(target_workspace)
