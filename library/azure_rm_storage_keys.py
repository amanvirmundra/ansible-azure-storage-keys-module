#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: azure_rm_storage_keys

short_description: This is my sample module

version_added: "2.4"

description:
    - "This is my longer description explaining my sample module"

options:
    resourcegroup_name:
        description:
            - This is the name of the resource group for which you want to retrieve Keys
        required: true

extends_documentation_fragment:
    - azure

author:
    - Amanvir Mundra (@amanvirmundra)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.storage import StorageManagementClient


def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        name=dict(type='str', required=True),
        resource_group=dict(type='str', required=True),
        client_id=dict(type='str', required=True),
        secret=dict(type='str', required=True),
        tenant=dict(type='str', required=True),
        subscription_id=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        Key1='',
        Key2=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    resource_group = module.params['resource_group']
    name = module.params['name']

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
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

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['Key1'] = storage_keys['key1']
    result['Key2'] = storage_keys['key2']

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()