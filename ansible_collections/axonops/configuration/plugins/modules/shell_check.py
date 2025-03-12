#!/usr/bin/python


DOCUMENTATION = r'''
---
module: axonops_shell_check

short_description: Set the shell checks.

version_added: "1.0.0"

description: Set the Shell Checks for your cluster on AxonOps SaaS.

options:
    base_url:
        description:
            - This represent the base url.
            - Specify this parameter if you are running on-premise.
            - Ignore if you are Running AxonOps SaaS.
        required: false
        type: str
    org:
        description:
            - This is the organisation name in AxonOps Saas.
            - It can be read from the environment variable AXONOPS_ORG.
        required: true
        type: str
    cluster:
        description:
            - Cluster where to apply the Adaptive Repair.
            - It can be read from the environment variable AXONOPS_CLUSTER.
        required: true
        type: str
    auth_token:
        description:
            - api-token for authenticate to AxonOps SaaS.
            - It can be read from the environment variable AXONOPS_TOKEN.
        required: false
        type: str
    api_token:
        description:
            - api-token to authenticate with AxonOps Server
        required: false
        type: str
    username:
        description:
            - Username for authenticate.
            - It can be read from the environment variable AXONOPS_USERNAME.
        required: false
        type: str
    password:
        description:
            - password for authenticate.
            - It can be read from the environment variable AXONOPS_PASSWORD.
        required: false
        type: str
    cluster_type:
        description:
            - The typo of cluster, cassandra, DSE, etc.
            - Default is cassandra
            - It can be read from the environment variable AXONOPS_CLUSTER_TYPE.
        required: false
        type: str
'''

EXAMPLES = r'''
# Activate Adaptive Repair on cluster `my_cluster` of `my_company`
  - name: Activate Adaptive Repair on my_cluster
    axonops_adaptive_repair:
      auth_token: "{{ secret }}"
      org: my_company
      cluster: my_cluster
      present: true
# Make sure single_instance has no Adaptive Repair present
  - name: Make sure single_instance has no Adaptive Repair present
    axonops_adaptive_repair:
      auth_token: "{{ secret }}"
      org: my_company
      cluster: single_instance
      present: false

'''

RETURN = r'''
url:
    description: The endpoint url.
    type: str
    returned: always

'''

import uuid
from copy import copy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.axonops.configuration.plugins.module_utils.axonops import AxonOps
from ansible_collections.axonops.configuration.plugins.module_utils.axonops_utils import make_module_args, \
    dicts_are_different


def run_module():
    module_args = make_module_args({
        'present': {'type': 'bool', 'required': False, 'default': True},
        'name': {'type': 'str', 'required': True},
        'interval': {'type': 'str', 'required': True},
        'timeout': {'type': 'str', 'required': True},
        'shell': {'type': 'str', 'required': False, 'default': '/bin/bash'},
        'script': {'type': 'str', 'required': True},
    })

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {
        'changed': False,
    }

    axonops = AxonOps(module.params['org'], auth_token=module.params['auth_token'], base_url=module.params['base_url'],
                      username=module.params['username'], password=module.params['password'],
                      cluster_type=module.params['cluster_type'], api_token=module.params['api_token'])

    if axonops.errors:
        module.fail_json(msg=' '.join(axonops.errors), **result)

    healthchecks_url = (f"/api/v1/healthchecks/"
                        f"{module.params['org']}/{axonops.get_cluster_type()}/{module.params['cluster']}")

    saas_settings, return_error = axonops.do_request(healthchecks_url)
    if return_error:
        module.fail_json(msg=return_error, **result)

    # all the shell checks for that environment
    current_checks_in_saas = saas_settings['shellchecks']
    shell_checks_to_send_to_saas = []
    existing_check = None
    if current_checks_in_saas:
        for check in current_checks_in_saas:
            if check['name'] == module.params['name']:
                existing_check = check
            else:
                shell_checks_to_send_to_saas.append(check)

    if module.params['present']:
        new_check = {
            'id': existing_check['id'] if existing_check else str(uuid.uuid4()),
            'present': module.params['present'],
            'interval': module.params['interval'],
            'name': module.params['name'],
            'script': module.params['script'],
            'shell': module.params['shell'],
            'timeout': module.params['timeout'],
        }
    else:
        new_check = {
            'present': False
        }

    if existing_check:
        existing_check_filtered = {
            'id': existing_check['id'],
            'present': True,
            'interval': existing_check['interval'],
            'name': existing_check['name'],
            'script': existing_check['script'],
            'shell': existing_check['shell'],
            'timeout': existing_check['timeout'],
        }
    else:
        existing_check_filtered = {
            'present': False
        }

    changed = dicts_are_different(existing_check_filtered, new_check)
    result['changed'] = changed
    result['diff'] = {'before': existing_check_filtered, 'after': copy(new_check)}

    if module.check_mode or not changed:
        module.exit_json(**result)
        return

    new_check['readonly'] = False

    new_check['integrations'] = {
        'OverrideError': False,
        'OverrideInfo': False,
        'OverrideWarning': False,
        'Routing': None,
        'Type': ''
    }

    if new_check['present']:
        shell_checks_to_send_to_saas.append(new_check)

    payload = {
        'httpchecks': saas_settings['httpchecks'],
        'tcpchecks': saas_settings['tcpchecks'],
        'shellchecks': shell_checks_to_send_to_saas,
    }

    _, return_error = axonops.do_request(
        rel_url=healthchecks_url,
        method='PUT',
        json_data=payload,
    )

    if return_error:
        module.fail_json(msg=return_error, **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
