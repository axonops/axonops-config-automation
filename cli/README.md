# AxonOps CLI 

This CLI is designed to extend the AxonOps Configuration Automation Ansible module.

## Installation

This CLI uses the same Python environment as the Ansible module and does not require any additional configuration.

### Export Environment Variables

This CLI accepts both command-line parameters and environment variables, just like the Ansible module.

## Using of CLI

### `repair`

Manages Adaptive Repair in AxonOps.

#### Options:

* `--org` Name of your organisation.
* `--cluster` Name of your cluster.
* `--token` AUTH_TOKEN used to authenticate with the API in SaaS.
* `--api_token` AXONOPS_API_TOKEN key.
* `--username` Username used for on-prem deployments when authentication is enabled.
* `--password` Password used for on-prem deployments when authentication is enabled.
* `--url` Specify the AxonOps URL if not using the SaaS production environment.
* `--enabled` If present, enables AxonOps Adaptive Repair; if absent, disables it.

#### Example: 

Activating Adaptive Repair for organisation `test` and cluster `thingscluster` on SaaS:


```shell
export AXONOPS_ORG='test'
export AXONOPS_CLUSTER="thingscluster"
export AXONOPS_TOKEN='aaaaabbbbccccddddeeee'

pipenv run python repair.py --enabled
```
