#!/usr/bin/python


DOCUMENTATION = r'''
---
module: axonops_restore

short_description: restore a previous backup

version_added: "1.0.0"

description: restore a backup to your cluster on AxonOps SaaS.

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
            - Cluster where to apply the Backup.
            - It can be read from the environment variable AXONOPS_CLUSTER.
        required: true
        type: str
    auth_token:
        description:
            - api-token for authenticate to AxonOps SaaS.
            - It can be read from the environment variable AXONOPS_TOKEN.
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
  - name: Restore snapshot to a Cassandra cluster
    axonops.configuration.restore_snapshot:
        org: "your_org"
        cluster: "your_cluster_name"
        tables: []
        snapshotId: "snashot_id_to_restore"
        nodes: []
        remote: true
        restoreAllTables: true
        restoreAllNodes: true
'''

RETURN = r'''
url:
    description: The endpoint url.
    type: str
    returned: always

'''

import json
import uuid
import sys
import time

from dateutil import parser
from datetime import timezone, datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.axonops.configuration.plugins.module_utils.axonops import AxonOps
from ansible_collections.axonops.configuration.plugins.module_utils.axonops_utils import make_module_args, \
    dicts_are_different, string_to_bool, string_or_none, bool_to_string

def run_module():
    module_args = make_module_args({
        'tables': {'type': 'list', 'default': []},
        'snapshotId': {'type': 'str', 'required': True},
        'nodes': {'type': 'list', 'default': []},
        'remote': {'type': 'bool', 'default': True},
        'restoreAllTables': {'type': 'bool', 'default': True},
        'restoreAllNodes': {'type': 'bool', 'default': True},
    })

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('restoreAllNodes', False, ('nodes',)),
            ('restoreAllTables', False, ('tables',)),
        ],
    )

    result = {
        'changed': False,
        'message': ""
    }    

    axonops = AxonOps(module.params['org'], auth_token=module.params['auth_token'], base_url=module.params['base_url'],
                      username=module.params['username'], password=module.params['password'],
                      cluster_type=module.params['cluster_type'])

    if axonops.errors:
        module.fail_json(msg=' '.join(axonops.errors), **result)


    payload = {
        "tables": module.params['tables'],
        "snapshotId": module.params['snapshotId'],
        "nodes": module.params['nodes'],
        "remote": module.params['remote'],
        "restoreAllTables": module.params['restoreAllTables'],
        "restoreAllNodes": module.params['restoreAllNodes'],
    }

    restore_snapshot_url = (f"/api/v1/cassandraSnapshotRestore/"
                             f"{module.params['org']}/{axonops.get_cluster_type()}/{module.params['cluster']}")

    restore_dateTime = datetime.now(tz=timezone.utc)

    # if it is in check mode, or it is not changed, exit
    if module.check_mode:
        module.exit_json(**result)
        return

    
    # The underlying do_request call uses open_url and that doesn't actually return any error messages
    # that come up. So if you try and restore a snapshot where the snapshotid doesn't exists you only 
    # get a generic 400 BAD REQUEST error rather than the handled error message "Could not find snapshot ID"
    restore_response, return_error = axonops.do_request(restore_snapshot_url, method="POST", json_data=payload)
    if return_error:
        module.fail_json(msg=return_error, **result)

    # Restore id being retured by axonops is a new feature so may not always be available
    restore_id = None
    if restore_response is not None and "ID" in restore_response:
        restore_id = restore_response["ID"]

    # Need to check for a restoreRequest that has a timestamp after 
    result['changed'] = True
    result['restore_status'] = "Pending"

    # The cassandraSnapshotRestore call doesn't return a specific id that we can query directly so have to 
    # do a fair amount of payload searching to try and find the triggered restore
    # keep querying the endpoint until we either whether the job has finished/failed/been cancelled
    while result['restore_status'] != "Done":
        saas_check, return_error = axonops.do_request(restore_snapshot_url, method="GET")
        if return_error:
            module.fail_json(msg=return_error, **result)

        most_recent_event_time = None
        
        for restore in saas_check:
            if restore['Type'] == "restoreBackup":
                if restore_id == None:
                    if "RestoreRequest" not in restore['Params'][3]:
                        break

                    if (restore['Params'][3]['RestoreRequest']['snapshotId'] == payload['snapshotId'] 
                        and restore['Params'][3]['RestoreRequest']['tables'] == payload['tables']
                        and restore['Params'][3]['RestoreRequest']['nodes'] == payload['nodes']
                        and restore['Params'][3]['RestoreRequest']['restoreAllTables'] == payload['restoreAllTables']
                        and restore['Params'][3]['RestoreRequest']['restoreAllNodes'] == payload['restoreAllNodes']
                    ):
                        item_last_run = parser.parse(restore['LastRun']).replace(tzinfo=timezone.utc)
                        # Make sure only consider records from after the restore was run and grab the most recent one.
                        if item_last_run > restore_dateTime:
                            if not most_recent_event_time:
                                most_recent_event_time = item_last_run
                            if item_last_run >= most_recent_event_time:
                                result['restore_id'] = restore["ID"]
                                result['restore_time'] = restore["LastRun"]
                                result['restore_status'] = restore["Status"]
                                result['restore_last_value'] = restore["LastReturnValue"]
                                result['restore_id_provided'] = False

                                if restore["Status"] == "Failed":
                                    module.fail_json(**result, msg="Restore attempt failed")
                                    return
                                elif restore["IsCancelled"]: 
                                    module.fail_json(**result, msg="Restore attempt was cancelled")
                                    return
                else:
                    if restore["ID"] == restore_id:
                            item_last_run = parser.parse(restore['LastRun']).replace(tzinfo=timezone.utc)
                            # Make sure only consider records from after the restore was run and grab the most recent one.
                            if item_last_run > restore_dateTime:
                                if not most_recent_event_time:
                                    most_recent_event_time = item_last_run
                                if item_last_run >= most_recent_event_time:
                                    result['restore_backup_id'] = restore["ID"]
                                    result['restore_time'] = restore["LastRun"]
                                    result['restore_status'] = restore["Status"]
                                    result['restore_last_value'] = restore["LastReturnValue"]
                                    result['restore_id'] = restore_id
                                    result['restore_id_provided'] = True

                                    if restore["Status"] == "Failed":
                                        module.fail_json(**result, msg="Restore attempt failed")
                                        return
                                    elif restore["IsCancelled"]: 
                                        module.fail_json(**result, msg="Restore attempt was cancelled")
                                        return

        time.sleep(5)

    module.exit_json(**result)
    return

def main():
    run_module()

if __name__ == '__main__':
    main()

