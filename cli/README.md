# AxonOps CLI 

This CLI is designed to extend the AxonOps Configuration Automation Ansible module.

## Installation

This CLI uses the same Python environment as the Ansible module and does not require any additional configuration.

### Export Environment Variables

This CLI accepts both command-line parameters and environment variables, just like the Ansible module.

## Using of CLI

### Global Options

All commands accept those attributes

* `--org` Name of your organisation.
* `--cluster` Name of your cluster.
* `--token` AUTH_TOKEN used to authenticate with the API in AxonOps Cloud.
* `--username` Username used for AxonOps Self-Hosted when authentication is enabled.
* `--password` Password used for AxonOps Self-Hosted when authentication is enabled.
* `--url` Specify the AxonOps URL if not using the AxonOps Cloud environment.

### `repair` Subcommand

Manages **Adaptive Repair** in AxonOps.

#### Options:

* `--enabled` Enables AxonOps Adaptive Repair.
* `--disabled` Disable AxonOps Adaptive Repair.
* `--gcgrace` GG Grace Threshold in Seconds.
* `--tableparallelism` Cuncurrent Repair Processes.
* `--segmentretries` Segment Retries.
* `--excludedtables` Excluded Tables. This parameter accepts a comma-separated list in the format `keyspace.table1,keyspace.table2`.
* `--excludetwcstables` Exclude TWCS tables.
* `--segmenttargetsizemb` Segment Target Size in MB.

#### Example: 

Activating Adaptive Repair for organisation `test` and cluster `thingscluster` on AxonOps Cloud:

```shell
export AXONOPS_ORG='test'
export AXONOPS_CLUSTER="thingscluster"
export AXONOPS_TOKEN='aaaaabbbbccccddddeeee'

pipenv run python axonops.py repair --enabled
```
