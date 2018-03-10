#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

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
        Key1='',
        Key2=''
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
    storage_keys = {v.key_name: v.value for v in account_keys.keys}

    result['Key1'] = storage_keys['key1']
    result['Key2'] = storage_keys['key2']

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()