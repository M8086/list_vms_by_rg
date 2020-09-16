# Get a list of all Virtual Machines for each Resource Group in a subscription
import os
import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_exceptions import CloudError

# You will want to supply the values in this function as environment variables
def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id

credentials, subscription_id = get_credentials()
client = ResourceManagementClient(credentials, subscription_id)
compute = ComputeManagementClient(credentials, subscription_id)


# Gather a list of VMs from each resource group and print them
def list_vms(resource_group):
    try:
        print(f'Getting VMs for: {resource_group}')
        vms = compute.virtual_machines.list(resource_group)
        while True:
            print(f'- {vms.next().name}')
    except StopIteration:
        print(f'\n\nFound all VMs for Resource Group: {resource_group}')

# Helper function to get all resource groups in the subscription
def get_vms_by_rg():
    try:
        rg = client.resource_groups.list()
        while True:
            list_vms(rg.next().name)
    except StopIteration:
        print("\n\nGathered all resource groups and VMs")

if __name__ == "__main__":
    get_vms_by_rg()
