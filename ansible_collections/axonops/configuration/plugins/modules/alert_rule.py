#!/usr/bin/python3

DOCUMENTATION = r'''
---
module: axonops_alert_rule

short_description: Configure an alerting rule for AxonOps

version_added: '1.0.0'

description: Configure an alerting rule for AxonOps

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
TODO

'''

EXAMPLES = r'''
TODO
'''

RETURN = r'''
TODO
'''

import re
import uuid

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.axonops.configuration.plugins.module_utils.axonops import AxonOps
from ansible_collections.axonops.configuration.plugins.module_utils.axonops_utils import make_module_args, find_by_field, dicts_are_different


def get_value_by_name(checked_filters, filter_name):
    """
    search in a Value / Name dictionary
    """
    if checked_filters:
        for checked_filter in checked_filters:
            if checked_filter['Name'] == filter_name:
                return checked_filter['Value']
    return None

def normalize_numbers(d):
    """
    Recursively normalizes numbers and lists in a dictionary:
    - Converts all integers and floats to floats to ensure consistent comparison.
    - Sorts lists for consistent comparison, unless they contain dictionaries.
    """
    if isinstance(d, dict):
        return {k: normalize_numbers(v) for k, v in d.items()}
    elif isinstance(d, list):
        # Only sort the list if it contains non-dictionary elements
        if all(isinstance(i, (int, float, str)) for i in d):
            return sorted(normalize_numbers(i) for i in d)
        else:
            return [normalize_numbers(i) for i in d]  # Do not sort if dictionaries are present
    elif isinstance(d, (int, float)):
        return float(d)  # Convert all numbers to floats
    elif isinstance(d, str):
        return d.strip()  # Handle strings by stripping whitespace
    return d


# def normalize_numbers(d):
#     """
#     Recursively normalizes numbers and lists in a dictionary:
#     - Converts all integers and floats to floats to ensure consistent comparison.
#     - Sorts lists for consistent comparison.
#     """
#     if isinstance(d, dict):
#         return {k: normalize_numbers(v) for k, v in d.items()}
#     elif isinstance(d, list):
#         return sorted(normalize_numbers(i) for i in d)
#     elif isinstance(d, (int, float)):
#         return float(d)  # Convert all numbers to floats
#     elif isinstance(d, str):
#         return d.strip()  # Handle strings by stripping whitespace
#     return d

# Function to get the ID by name
def get_integration_id_by_name(data, target_name):
    definitions = data.get("Definitions", [])

    for definition in definitions:
        params = definition.get("Params", {})
        name = params.get("name")
        if name == target_name:
            return definition.get("ID")

    return None


def run_module():
    module_args = make_module_args({
        'name': {'type': 'str', 'default': ''},
        'description': {'type': 'str', 'default': ''},
        'dashboard': {'type': 'str', 'required': True},
        'chart': {'type': 'str', 'required': True},
        'metric': {'type': 'str', 'default': ''},
        'operator': {'type': 'str', 'choices': ['=', '>=', '>', '<=', '<', '!=']},
        'warning_value': {'type': 'float'},
        'critical_value': {'type': 'float'},
        'duration': {'type': 'str'},
        'url_filter': {'type': 'str', 'default': ''},
        'scope': {'type': 'list', 'default': []},
        'dc': {'type': 'list', 'default': []},
        'rack': {'type': 'list', 'default': []},
        'host_id': {'type': 'list', 'default': []},
        'group_by': {'type': 'list', 'default': [], 'choices': ['dc', 'host_id', 'rack', 'scope', []]},
        'routing': {'type': 'dict', 'default': {}},
        'present': {'type': 'bool', 'default': True},
        'percentile': {'type': 'list', 'default': [], 'choices': ['','75thPercentile','95thPercentile','98thPercentile','99thPercentile','999thPercentile']},
        'consistency': {'type': 'list', 'default': [], 'choices': ['','ALL','ANY','ONE','TWO','THREE','SERIAL','QUORUM','EACH_QUORUM','LOCAL_ONE','LOCAL_QUORUM','LOCAL_SERIAL']},
        'keyspace': {'type': 'list', 'default': []},
        'scope': {'type': 'list', 'default': []}
    })

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('present', True, ('operator', 'warning_value', 'critical_value', 'duration'))
        ]
    )
    result = {
        'changed': False,
    }

    consistency =  module.params["consistency"]
    percentile =  module.params["percentile"]
    group_by = module.params["group_by"]
    org = module.params['org']
    cluster_type = module.params['cluster_type']
    cluster = module.params['cluster']
    alert_name = module.params['name'] or module.params['chart']
    url_filter = module.params['url_filter'] or 'time=30'

    axonops = AxonOps(module.params['org'], auth_token=module.params['auth_token'], base_url=module.params['base_url'],
                      username=module.params['username'], password=module.params['password'],
                      cluster_type=module.params['cluster_type'])

    if axonops.errors:
        module.fail_json(msg=' '.join(axonops.errors), **result)

    alerts_url = f"/api/v1/alert-rules/{org}/{axonops.get_cluster_type()}/{cluster}"

    # Get existing alerts and dashboard templates
    existing_alerts, error = axonops.do_request(alerts_url)
    error_message = "Error occured accessing alert URL: " + alerts_url + str(error)
    if error is not None:
        module.fail_json(msg=error_message)
        return

    dash_templates, error = axonops.do_request(
        f"/api/v1/dashboardtemplate/{org}/{axonops.get_cluster_type()}/{cluster}")
    error_message = "Error occured fetching AxonOps dashboard template: " + f"/api/v1/dashboardtemplate/{org}/{axonops.get_cluster_type()}/{cluster}" + str(error)
    if error is not None:
        module.fail_json(msg=error_message)
        return

    # Find the referenced dashboard by name
    new_dash = find_by_field(dash_templates.get('dashboards'), 'name', module.params['dashboard'])
    if not new_dash:
        module.fail_json(msg=f"Could not find dashboard '{module.params['dashboard']}' in AxonOps")
        return

    # Find the referenced chart in the dashboard
    new_chart = find_by_field(new_dash.get('panels'), 'title', module.params['chart'])
    if not new_chart:
        module.fail_json(msg=f"Could not find chart '{module.params['chart']}' in AxonOps")
        return

    # Get the chart query if not specified in the params
    if not module.params['metric']:
        try:
            raw_query = new_chart['details']['queries'][0]['query']
        except (TypeError, IndexError):
            module.fail_json(msg='Failed getting the metric query from the specified chart')
            return

        # remove var similar to: dc=~'$dc',rack=~'$rack', host_id=~'$host_id'
        raw_query = re.sub(r'(\w+)=~\'([$]\w*)?\',?', '', raw_query)

        # remove eventual last comma
        raw_query = re.sub(r', *}', r'}', raw_query)

        # remove eventual multiple spaces
        raw_query = re.sub(r' +', r' ', raw_query)

        # change ($groupBy) to (dc)
        metric = re.sub(re.escape('($groupBy)'), r'(dc)', raw_query)

    else:
        metric = module.params['metric']

    # Find the existing alert (if present)
    old_alert = find_by_field(existing_alerts.get('metricrules'), 'alert', alert_name)

    # Bail out early if the alert doesn't exist, and we don't want it to
    if not old_alert and not module.params['present']:
        module.exit_json(**result)
        return

    if old_alert:
        # Find the current dashboard and widget by parsing the widget url
        widget_parts = old_alert['annotations']['widget_url'].split('/')
        old_dash_uuid = None
        old_widget_uuid = None
        old_url_filter = None
        old_dash_name = None
        old_chart_name = None
        if len(widget_parts) >= 6:
            uuid_parts = widget_parts[5].split('?')
            old_dash_uuid = uuid_parts[0]
            if len(uuid_parts) > 1:
                parts2 = uuid_parts[1].split('&')
                if parts2[0].startswith("uuid="):
                    old_widget_uuid = parts2[0][5:]
                else:
                    old_widget_uuid = parts2[0]
                if len(parts2) > 1:
                    old_url_filter = parts2[1]

        if old_dash_uuid:
            old_dash = find_by_field(dash_templates.get('dashboards'), 'uuid', old_dash_uuid)
            if old_dash:
                old_dash_name = old_dash.get('name')
                if old_widget_uuid:
                    old_chart = find_by_field(old_dash.get('panels'), 'uuid', old_widget_uuid)
                    if old_chart:
                        old_chart_name = old_chart['title']
        if not old_chart_name:
            old_chart_name = old_alert.get('alert')

        # Trim the last 2 space-separated sections from the string because they will be the operator and value.
        # This should leave just the metric
        metric = re.sub(' [^ ]+ [^ ]+$', '', old_alert['expr'])

        old_integrations = old_alert.get('integrations', {})
        if old_integrations:
            del old_integrations['Type']
            del old_integrations['OverrideError']
            del old_integrations['OverrideInfo']
            del old_integrations['OverrideWarning']
            for route_item in old_integrations['Routing']:
                del route_item['Params']

        old_data = {
            'name': old_alert.get('alert'),
            'description': old_alert.get('annotations', {}).get('description', ''),
            'dashboard': old_dash_name,
            'chart': old_chart_name,
            'metric': metric,
            'operator': old_alert.get('operator', ''),
            'warning_value': old_alert.get('warningValue', ''),
            'critical_value': old_alert.get('criticalValue', ''),
            'duration': old_alert.get('for', ''),
            'url_filter': old_url_filter or '',
            'scope': get_value_by_name(old_alert.get('filters', []), 'scope') or [],
            'dc': get_value_by_name(old_alert.get('filters', []), 'dc') or [],
            'rack': get_value_by_name(old_alert.get('filters', []), 'rack') or [],
            'host_id': get_value_by_name(old_alert.get('filters', []), 'host_id') or [],
            'group_by': get_value_by_name(old_alert.get('filters', []), 'groupBy') or [],
            'percentile': get_value_by_name(old_alert.get('filters', []), 'percentile') or [],
            'consistency': get_value_by_name(old_alert.get('filters', []), 'consistency') or [],
            'keyspace': get_value_by_name(old_alert.get('filters', []), 'keyspace') or [],
            'integrations': old_alert.get('integrations', {}),
            'present': True
        }

        # Check if 'integrations' and 'Routing' exist before adding routing to old_data
        # if 'integrations' in old_alert and 'Routing' in old_alert['integrations']:
        #     old_data['integrations']['routing'] = {}  # Initialize routing as an empty dictionary
        #     for routing in old_alert['integrations']['Routing'] or []:
        #         if routing['Severity']:
        #             # If this is the first time encountering the severity, create the list
        #             if routing['Severity'] not in old_data['routing']:
        #                 old_data['routing'][routing['Severity']] = []

        #             # Find the integration name for that ID
        #             integration_name, error = axonops.find_integration_name_by_id(cluster, routing['ID'])
        #             if error is not None:
        #                 module.fail_json(msg=error)
        #                 return

        #             # Add the integration name to the list for the specific severity
        #             # old_data['routing'][routing['Severity']].append(integration_name)
        #             old_data['routing'][routing['Severity']].append(routing['ID'])

        #     # If routing ends up being empty after processing, remove it from old_data
        #     if not old_data['routing']:
        #         del old_data['routing']
        # else:
        #     # Explicitly ensure no empty routing key remains in old_data
        #     old_data.pop('routing', None)





                            # # add the integration overrides if present
                            # if 'integrations' in old_alert and old_alert['integrations']['Routing']:
                            #     for routing in old_alert['integrations']['Routing'] or []:
                            #         # if it is the first time that we meet that severity, create the list
                            #         if routing['Severity']:
                            #             old_data['Routing'][routing['Severity']] = []

                            #         # search the integration relative to that IP
                            #         integration_name, error = axonops.find_integration_name_by_id(cluster, routing['ID'])
                            #         if error is not None:
                            #             module.fail_json(msg=error)
                            #             return

                            #         # add the integration name to the list relative to the specif severity
                            #         old_data['routing'][routing['Severity']].append(integration_name)

    else:
        old_data = {'present': False}

    old_data_normalized = normalize_numbers(old_data)

    if module.params['present']:
        new_data = {
            'name': alert_name,
            'description': module.params['description'],
            'dashboard': module.params['dashboard'],
            'chart': module.params['chart'],
            'metric': metric,
            'operator': module.params['operator'],
            'warning_value': module.params['warning_value'],
            'critical_value': module.params['critical_value'],
            'duration': module.params['duration'],
            'url_filter': url_filter,
            'dc': module.params['dc'],
            'rack': module.params['rack'],
            'host_id': module.params['host_id'],
            'group_by': module.params['group_by'],
            'percentile': percentile,
            'consistency': consistency,
            'keyspace': module.params['keyspace'],
            'scope': module.params['scope'],
            'present': True,
            'integrations': {}
        }
    else:
        new_data = {
            'name': alert_name,
            'dashboard': module.params['dashboard'],
            'chart': module.params['chart'],
            'present': False,
        }

    # create routing override list
    routing = []  # format [{id: 'id33s', severity: 'error'},...]
    for severity in module.params['routing']:
        for override in module.params['routing'][severity]:
            integration_id, error = axonops.find_integration_id_by_name(cluster, override)
            if error is not None:
                module.fail_json(msg=error)
                return
            routing.append({
                'ID': integration_id,
                'Severity': severity,
            })
    if routing:
        new_data['integrations']['Routing'] = routing
    elif 'integrations' in new_data:
        new_data['integrations']['Routing'] = []

    new_data_normalized = normalize_numbers(new_data)


    changed = dicts_are_different(new_data_normalized, old_data_normalized)
    result['changed'] = changed
    result['diff'] = {'before': old_data_normalized, 'after': new_data_normalized}

    # Exit if in check mode or no changes
    if module.check_mode or not changed:
        module.exit_json(**result)
        return

    # Delete the alert rule and exit if present is False
    if not module.params['present']:
        if old_alert:
            _, error = axonops.do_request(rel_url=alerts_url + '/' + old_alert["id"], method='DELETE')
            if error is not None:
                module.fail_json(msg=error)
        module.exit_json(msg='Failed to delete the existing alert rule', **result)
        return

    # Set up alert expression
    alert_expression = ''
    if (len(group_by) > 0):
        alert_expression = metric.replace('$groupBy', ",".join(group_by))
    else:
        alert_expression = f"{metric} {module.params['operator']} {module.params['warning_value']}"

    result['alert_expression'] = alert_expression


    # Create or update the alert rule
    payload = {
        'alert': alert_name,
        'for': module.params['duration'],
        'operator': module.params['operator'],
        'warningValue': module.params['warning_value'],
        'criticalValue': module.params['critical_value'],
        'annotations': {
            'description': module.params['description'],
            'summary': "%s is %s than %s (current value: {{$value}})" % (
                alert_name, module.params['operator'], module.params['warning_value']),
            'widget_url': "/%s/%s/%s/performance/%s?uuid=%s&%s" % (
                org, cluster_type, cluster, new_dash['uuid'], new_chart['uuid'], url_filter),
        },
        'integrations': {'Routing': routing},
        'expr': alert_expression,
        'widgetTitle': module.params['chart'],
        'id': old_alert["id"] if old_alert else str(uuid.uuid4()),
        'correlationId': new_chart['uuid'],
        'Filters': [
            {
                "Name": "consistency",
                "Value": consistency
            },
            {
                "Name": "percentile",
                "Value": percentile
            },
            {
                "Name": "keyspace",
                "Value": module.params['keyspace']
            },
            {
                "Name": "scope",
                "Value": module.params['scope']
            },
            {
                "Name": "dc",
                "Value": module.params["dc"]
            },
            {
                "Name": "rack",
                "Value": module.params["rack"]
            },
            {
                "Name": "host_id",
                "Value": module.params["host_id"]
            },
            {
                "Name": "groupBy",
                "Value": module.params["group_by"]
            }
        ]
    }

    result['payload'] = {'payload': payload }
    _, error = axonops.do_request(rel_url=alerts_url, method='POST', json_data=payload)
    if error is not None:
        module.fail_json(msg="Failed to create alert rule: " + str(payload), **result)
        module.f
        return

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
