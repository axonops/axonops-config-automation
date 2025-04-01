# AxonOps Configuration Automation

This repository contains Ansible playbooks designed to automate the configuration of AxonOps after connecting your cluster to AxonOps.

AxonOps is a comprehensive management platform for Apache Cassandra® and Apache Kafka®. It simplifies monitoring, maintenance, backups, and development by providing unified operations and customizable dashboards. 

With these playbooks, you can easily set up alerts, dashboards, and other configurations for your AxonOps installation. For more information about AxonOps and its features, visit the [AxonOps website](https://axonops.com) or explore the [AxonOps documentation](https://axonops.com/docs/).

This project is intended to configure your AxonOps settings on our SaaS or self-hosted installations of AxonOps. AxonOps can be self-installed in a variety of ways. See: 
- https://github.com/axonops/helm-axonops
- https://github.com/axonops/axonops-ansible-collection
- https://github.com/axonops/axonops-server-compose
- https://github.com/axonops/axonops-installer-packages-downloader

## Installation

### What You Will Need Before Start

To run the Ansible AxonOps Playbook you will need:

- Anisble >= 2.10
- Python3.8 or above
- make

### Export Environment Variables

The Ansible Playbook takes as input environment variables, the standard for a SaaS connections are:

```shell
# export your org
# This is the only mandatory variable value
export AXONOPS_ORG='example'

# Create you API token within your AxonOps console. You will need DBA level access or above to the clusters
# you will be configuring.
export AXONOPS_TOKEN='aaaabbbbccccddddeeee'
```

To simplify the process, the `export_tokens.sh` file has been created with all the accepted variables. Modify this file with your specific details, and then export the variables.

```commandline
source ./export_tokens.sh
```

The `AXONOPS_TOKEN` parameter is used only for AxonOps SaaS. For AxonOps on-premises, you can use a username and password or configure it to allow anonymous login.
Refer to `export_tokens.sh` for more information on configuring the Ansible Playbook for AxonOps on-premises and on the accepted environment variables.

### Ansible preparation

The playbooks have been tested on Ansible 2.10 but it should work on most versions.

> *NOTE:* We prefer using the GNU Make to run these playbooks but you can
>         use the `make.sh` script instead if you prefer.

#### RedHat and RockyLinux

The system `ansible` package should work fine for RedHat and RockyLinux >=8

```sh
sudo dnf -y install epel-release
sudo dnf -y install ansible make
```

#### Debian and Ubuntu

It has been tested for Ubuntu 22.04 and Debian Bookworm:

```sh
sudo apt update
sudo apt -y install ansible make
```

#### Virtualenv

If you're using virtualenv, simply create a python 3 environment and install Ansible to it:

```sh
virtualenv ~/py-axonops
source ~/py-axonops/bin/activate
pip3 install -r requirements.txt
```

#### Pipenv

We recommend using `pipenv` to manage the environment. After installing `pipenv`, simply run:

```shell
pipenv install
```

and the export the variable:

```sh
export PIPENV=true
```

## Configuration

The configuration is structured in folders following the format within the directory `config`:

The `config/REPLACE_WITH_ORG_NAME` folder contains `alert_endpoints.yml` which defines alert endpoints at the org level,
since the alert endpoints are defined for the entire org and shared across all your clusters. All other
configurations are defined per cluster. This folder also contains the following files:

 - metric_alert_rules.yml
 - log_alert_rules.yml
 - service_checks.yml

These configurations defined in this folder will be applied to all of your clusters. You should define
common alert rules and service checks in this folder.

To define cluster specific configurations, overiding the rules and configurations defined at the org level, example
files are provided under `config/REPLACE_WITH_ORG_NAME/REPLACE_WITH_CLUSTER_NAME`. The rules and configurations
in this folder will append and override the settings provided in the org folder.


## Alert Endpoints
Alert endpoints such as Slack, Teams, PagerDuty, OpsGenie can be configured using this Ansible playbook.
Since alert endpoints configurations are AxonOps org-level setting, the configuration file is placed at `./config/<org_name>/alert_endpoints.yml`.


## Metric Alert Rules
The metric alert rules are configured against the charts that exists for the AxonOps dashboard in each cluster.
Multiple alert rules can be configured against each chart.

An example configuration for a metric alert is shown below.

```
- name: CPU usage per host
  dashboard: System
  chart: CPU usage per host
  operator: '>='
  critical_value: 99
  warning_value: 90
  duration: 1h
  description: Detected High CPU usage
  present: true
```
`name:` is the name of the alert

`dashboard:` must correspond to the dashboard name in the AxonOps right-hand menu.

![Dashboard -> System](./assets/axonops-dashboard-system.png)

`chart:` must correspond to the name of the chart within the above dashboard. In this case `CPU usage per host`. The metric query is
automatically detected by specifying the chart name.

![Chart - CPU usage per host](./assets/axonops-chart-cpu-usage.png)

`operator:` options are: `==`, `>=`, `>`, `<=`, `<`, `!=`.

![Alert Rule Operators](./assets/axonops-alert-rule-operators.png)

`critical_value:` is the critical value threshold.

`warning_value:` is the warning value threshold.

`duration:` is the duration the warning or critical values must violate the operator rule before the alert is triggered.

`description:` sets the description of the alert. You may want to add a description of an action to take when this alert is raised.

`present:` `true|false` - by setting it to `false` it will remove the alert.

## Log Alert Rules
Log alerts can be defined using this Ansible playbook.

An example configuration for a log alert is shown below.
```
- name: TLS failed to handshake with peer
  warning_value: 50
  critical_value: 100
  duration: 5m
  content: \"Failed to handshake with peer\"
  source: "/var/log/cassandra/system.log"
  description: "Detected TLS handshake error with peer"
  level: warning,error,info
  present: true
```
`name:` is the name of the alert.

`warning_value:` is the warning value threshold based on the count of matched logs.

`critical_value:` is the critical value threshold based on the count of matched logs.

`duration:` is the duration the warning or critical values must violate the operator rule before the alert is triggered.

`content`: is the text search. Double quotes must be escaped.
Currently the following matching syntax is supported:
* `hello` - matches `hello`
* `hello world` - matches `hello` or `world`
* `"hello world"` - matches exact `hello world`
* `+-hello` - matches excluding `hello`
* `+-"hello world"` - matches excluding `hello world`
* `+-hello +-world` - matches excluding `hello` or `world`

`source`: specifies the log source. This must match with one of the options available in the `Source` filter found in the Logs&Events view.

![Event Source](./assets/axonops-event-source.png)

`description:` sets the description of the alert. You may want to add a description of an action to take when this alert is raised.

`level:` sets the event level filter - a comma separated list with the following values: `debug`, `error`, `warning`, `info`

`present:` `true|false` - by setting it to `false` it will remove the alert.

## Service Checks
Service checks in AxonOps can be configured using this playbook. Example service check configurations can be found
in:
`./config/REPLACE_WITH_ORG_NAME/REPLACE_WITH_CLUSTER_NAME/service_checks.yml`


## Backups
Backup Schedules can be create and Backup snapshots taken

Supported backup locations are:
* local
* s3
* sftp
* azure

Remote Backup paths take the form of
```$remote_path/cassandra/$cluster_name/$node_id```

### General options
These following options apply to all backup configurations


| Option | Required | Type | Description |
| ------ | ------ | ------ | ------ |
| present | No | Bool | Whether a backup schedule should exist.  Setting to False will remove an existing schedule. Defaults to True |
| local_retention | No | Str | How long to keep a snapshot on the local node.  Defaults to 10d (10 Days) |
| remote | No | Bool | Whether backup is to a remote.  Defaults to False |
| remote_retention | No | Str | How long to keep a snapshot on the remote location.  Defaults to 60d (60 Days) |
| remote_type | Only if remote is True | Str |  Where to send backups.  One of 'local', 's3', 'sftp', 'azure'. Defaults to local.  |
| timeout | No | Str | Time before backup times out.  Defaults to 10h (10 Hours) |
| transfers | No | Int | File Transfers Parallelism |
| tps_limit | No | Int | Throttle transfer amount |
| bw_limit | No | Str | Apply bandwith throttling. Use a suffix b|k|M|G. The default is 0 which means no limit. 10M corresponds to 10 MBytes/s |
| tag | No | Str | Tag to apply to the backup |
| datacenters | Yes | List(Str) | Datacenters to include in backup |
| nodes | No | List(str) | Nodes to include in backup |
| tables_keyspace | No | List(str) | Mutually exclusive with tables |
| tables | No | List(str) | Tables to include in backup. Mutually exclusive with tables_keyspace |
| keyspaces | No | List(str) | Keyspaces to include in backup |
| schedule | No | Bool | Whether to schedule a future backup.  If False then an immediate snapshot will be taken |
| schedule_expre | No | Str | Crontab expression of backup schedule. Defaults to '0 1 * * *' |


### Local Options
Backs up to the local filesystem of the node.


### S3
Sends backups to an S3 bucket

#### S3 Options

| Option | Required | Type | Description |
| ------ | ------ | ------ | ------ |
| remote_path | Yes | Str | Path to store the backups, Needs to include the bucketname. eg mybucket/path/to/backups |
| s3_region | Yes | Bool | S3 region that bucket is in |
| s3_access_key_id | No | Str | S3 Access key ID if not using IAM authentication |
| s3_secret_access_key | No | Str | S3 Access key if not using IAM authentication |
| s3_storage_class | No | Str | Storage class of bucket.  Defaults to STANDARD. One of 'default', 'STANDARD', 'reduced_redundancy', 'standard_ia', 'onezone_ia', 'glacier', 'deep_archive', 'intelligent_tiering' |
| s3_acl | No | Str | ACL type of bucket. Defaults to private.  One of 'private', 'public-read', 'public-read-write','authenticated-read', 'bucket-owner-read' |
| s3_encryption | No | Str | Encryption to apply. Defaults to AES256.  One of 'none', 'AES256' |
| s3_no_check_bucket | No | Bool | |
| s3_disable_checksum | No | Bool | |


### SFTP
Sends backups to and SFTP/SSH server

#### sftp options
| Option | Required | Type | Description |
| ------ | ------ | ------ | ------ |
| remote_path | Yes | Str | Path to store the backups on the remote server |
| host | Yes | Str | Host to connect to |
| ssh_user | Yes | Str | Username to connect as |
| ssh_pass | No | Str | Password to connect with. Either ssh_pass or key_file needs to be set |
| key_file | No | Str | Location of key file on the host. Either ssh_pass or key_file needs to be set |


### Azure
Sends backups to an Azure Storage Blob container

#### Azure options
| Option | Required | Type | Description |
| ------ | ------ | ------ | ------ |
| remote_path | Yes | Str | Path to store the backups, Needs to include the container name. eg mycontainer/path/to/backups |
| azure_account | Yes | Str | The name of the Azure storage account |
| azure_endpoint | No | Str | To override the endpoint destination for the Azure storage account.  Generally not required |
| azure_key | No | Str | Storage account key.  Only required if not using Azure MSI authentication |
| azure_msi | No | Bool | Whether to use Azure MSI authentication to connect to the storage account |
| azure_msi_object_id | No | Only required if there are multiple user assigned identities.  Mutually exlusive with azure_msi_client_id and azure_msi_mi_res_id |
| azure_msi_client_id | No | Only required if there are multiple user assigned identities.  Mutually exlusive with azure_msi_object_id and azure_msi_mi_res_id |
| azure_msi_mi_res_id | No | Only required if there are multiple user assigned identities.  Mutually exlusive with azure_msi_object_id and azure_msi_client_id |


### Backup Examples
```
- name: Schedule a backup to S3 bucket
  remote_type: s3
  cluster: testcluster
  datacenters: dc1
  remote_path: bucketname/path
  local_retention: 10d
  remote_retention: 60d
  tag: "scheduled backup"
  timeout: 10h
  remote: True
  schedule: True
  schedule_expr: 0 1 * * *
  s3_region: eu-west-2
  s3_acl: private
```



```
- name: Snapshot a table to an Azure Blob
  remote_type: azure
  cluster: testcluster
  datacenters: dc1
  remote_path: foo
  local_retention: 10d
  remote_retention: 30d
  tag: "Snapshot appTable"
  timeout: 10h
  remote: True
  tables: ['appKeyspace.appTable']
  keyspaces: ['appKeyspace']
  schedule: False
  azure_account: azure_storage_account_name
  azure_use_msi: True
```


## Playbooks
The playbooks are designed to run in a predefined order as some of them depend on the others. For example,
you'll need to create the alert endpoints before you can set up alert routing.

1. Set up alert endpoints
2. Set up routes
3. Set up metrics alerts
4. Set up log alerts
5. Set up Service checks
6. Set up backup schedules

### Running
The provided [Makefile](./Makefile) is the easiest way to run the playbooks:

```
❯ make help
metrics-alerts                 Create alerts based on metrics
check                          run pre-commit tests
endpoints                      Create alert endpoints and integrations
log-alerts                     Create alerts based on logs
routes                         Create alert routes
service-checks                 Create alerts for TCP and shell connections
backups                        Create backup schedules
validate                       Validate YAML config
```

You can decide to either configure all the parameters as explained above using the [export_tokens.sh](./export_tokens.sh) file,
or you can set them in the command line overriding the environment configuration:

```shell
make endpoints AXONOPS_ORG=ORG_NAME
make routes AXONOPS_ORG=ORG_NAME AXONOPS_CLUSTER=CLUSTER_NAME
make metrics-alerts AXONOPS_ORG=ORG_NAME AXONOPS_CLUSTER=CLUSTER_NAME
make log-alerts AXONOPS_ORG=ORG_NAME AXONOPS_CLUSTER=CLUSTER_NAME
make service-checks AXONOPS_ORG=ORG_NAME AXONOPS_CLUSTER=CLUSTER_NAME
make backups AXONOPS_ORG=ORG_NAME AXONOPS_CLUSTER=CLUSTER_NAME
make validate
```

> *NOTE:* the environment variable AXONOPS_CLUSTER is optional.
> If the variable is missing, all clusters in the ORG will be selected.

### Validating the YAML configurations

To validate the format of the configurations files, first, ensure you installed [Virtualenv](#Virtualenv) or [Pipenv](#Pipenv), then run:

```shell
make validate
```

The validation will output a report for each file, for example in case of error:
```aiignore
Validating config/REPLACE_WITH_ORG_NAME/metric_alert_rules.yml against schemas/metric_alert_rules_schema.yml...
✖ config/REPLACE_WITH_ORG_NAME/metric_alert_rules.yml failed validation:
Error validating data 'config/REPLACE_WITH_ORG_NAME/metric_alert_rules.yml' with schema 'schemas/metric_alert_rules_schema.yml'
	axonops_alert_rules.23.operator: '>=!!' not in ('>', '>=', '=', '!=', '<=', '<')
```
Example of validation successful:
```aiignore
Validating config/REPLACE_WITH_ORG_NAME/REPLACE_WITH_CLUSTER_NAME/service_checks.yml against schemas/service_checks_schema.yml...
✔ config/REPLACE_WITH_ORG_NAME/REPLACE_WITH_CLUSTER_NAME/service_checks.yml is valid.
```

The script will also print a final report of the validations, example:
```aiignore
OK: 39
ERRORS: 1
MISSING: 0
```


### Other
The provided playbooks are only examples. Adapt the rules and configurations to suit your enterprise requirements.

***

*This project may contain trademarks or logos for projects, products, or services. Any use of third-party trademarks or logos are subject to those third-party's policies. AxonOps is a registered trademark of AxonOps Limited. Apache, Apache Cassandra, Cassandra, Apache Spark, Spark, Apache TinkerPop, TinkerPop, Apache Kafka and Kafka are either registered trademarks or trademarks of the Apache Software Foundation or its subsidiaries in Canada, the United States and/or other countries. Elasticsearch is a trademark of Elasticsearch B.V., registered in the U.S. and in other countries. Docker is a trademark or registered trademark of Docker, Inc. in the United States and/or other countries.*
