#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: azure_rm_storageaccount_keys

version_added: "2.6"

short_description: Retrieve Azure Storage Account Keys.

description:
    - Retrive keys for a Storage Account.

options:
    resource_group:
        description:
            - This is the name of the resource group for which you want to retrieve Keys
        required: true
        default: null
    name:
        description:
            - Name of the Storage Account instance.
        required: true
        default: null
        aliases:
            - resource_group_name
    client_id:
        description:
            - Client Id of Azure Service Principal
        required: true
        default: null
    secret:
        description:
            - App secret of Azure Service Principal
        required: true
        default: null
    tenant:
        description:
            - Tenant Id of Azure Service Principal
        required: true
        default: null
    subscription_id:
        description:
            - Azure Subscription Id
        required: true
        default: null

extends_documentation_fragment:
    - azure

author:
    - Amanvir Mundra (@amanvirmundra)

'''

EXAMPLES = '''
- name: Get Storage account keys
  azure_rm_storageaccount_keys:
    resource_group: resource_group
    name: name
'''

RETURN = '''
keys:
    description: Dictionary of Keys associated with the Storage Account
    returned: always
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.storage import StorageManagementClient

def run_module():
    
    module_args = dict(
        name=dict(type='str', required=True),
        resource_group=dict(type='str', required=True),
        client_id=dict(type='str', required=True),
        secret=dict(type='str', required=True),
        tenant=dict(type='str', required=True),
        subscription_id=dict(type='str', required=True)
    )
    
    result = dict(
        changed=False,
        keys=None
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    resource_group = module.params['resource_group']
    name = module.params['name']

    if module.check_mode:
        return result

    credentials = ServicePrincipalCredentials(
        client_id = module.params['client_id'],
        secret = module.params['secret'],
        tenant = module.params['tenant']
    )
    subscription_id = module.params['subscription_id']
    client = StorageManagementClient(credentials, subscription_id)
    account_keys = client.storage_accounts.list_keys(resource_group, name)
    keys = dict()
    for key in account_keys.keys:
        keys[key.key_name] = key.value

    result['keys'] = keys

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()