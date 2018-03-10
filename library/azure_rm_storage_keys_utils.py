#!/usr/bin/python
from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: azure_rm_storage_keys
short_description: Retrieve Azure Storage Account Keys
version_added: "2.4"
description:
    - "Retrive keys for a Storage Account"

options:
    resource_group:
        description:
            - This is the name of the resource group for which you want to retrieve Keys
        required: true
    name:
        description:
            - Name of the Storage Account instance.
        required: true

extends_documentation_fragment:
    - azure

author:
    - Amanvir Mundra (@amanvirmundra)
'''

EXAMPLES = '''
- name: Get Storage account keys
      azure_rm_storage_keys_utils:
        resource_group: resource_group
        name: account_name
'''

RETURN = '''
key1:
    description: Key1 for azure storage account
    returned: always
    type: str
key2:
    description: Key2 for azure storage account
    returned: always
    type: str
'''

from ansible.module_utils.azure_rm_common import AzureRMModuleBase
try:
    from msrestazure.azure_exceptions import CloudError
except ImportError:
    # This is handled in azure_rm_common
    pass

class AzureRMStorageAccountKeys(AzureRMModuleBase):
    def __init__(self):
        
        self.module_arg_spec = dict(
            resource_group=dict(type='str', aliases=['resource_group_name'], required=True),
            name=dict(type='str', required=True)
        )
        self.resource_name = None
        self.name = None

        super(AzureRMStorageAccountKeys, self).__init__(self.module_arg_spec, supports_tags=True)
    

    def exec_module(self, **kwargs):
        """Main module execution method"""
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            setattr(self, key, kwargs[key])

        try:
            account_keys = self.storage_client.storage_accounts.list_keys(self.resource_group, self.name)
        except CloudError:
            pass
        storage_keys = {v.key_name: v.value for v in account_keys.keys}

        self.result['key1'] = storage_keys['key1']
        self.result['key2'] = storage_keys['key2']
        
        return self.results


def main():
    AzureRMStorageAccountKeys()

if __name__ == '__main__':
    main()