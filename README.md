# AxonOps Configuration Automation

<p align="center">
  <strong>🚀 Enterprise-grade Ansible automation for AxonOps monitoring and management platform</strong>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#installation">Installation</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#usage">Usage</a> •
  <a href="#examples">Examples</a>
</p>

---

## Overview

This repository provides production-ready Ansible playbooks to automate the configuration of [AxonOps](https://axonops.com) - a comprehensive management platform for Apache Cassandra® and Apache Kafka®. With these playbooks, you can programmatically configure alerts, dashboards, backups, and monitoring rules without manual GUI interaction.

> **Note**: This project configures AxonOps settings on SaaS or self-hosted installations. For installing AxonOps itself, see:
> - [Helm Charts](https://github.com/axonops/helm-axonops)
> - [Ansible Collection](https://github.com/axonops/axonops-ansible-collection)
> - [Docker Compose](https://github.com/axonops/axonops-server-compose)
> - [Installer Packages](https://github.com/axonops/axonops-installer-packages-downloader)

### What Gets Configured?

This automation framework configures:

- **📊 100+ Pre-defined Metric Alerts** - CPU, memory, disk, latency, timeouts, and Cassandra/Kafka-specific metrics
- **📝 20+ Log Alert Rules** - Node failures, SSL issues, repairs, disk space, and error patterns
- **🔔 Multi-Channel Alert Routing** - Slack, PagerDuty, OpsGenie, ServiceNow, Microsoft Teams
- **💾 Automated Backup Schedules** - S3, Azure Blob, SFTP with retention policies
- **🏥 Service Health Checks** - TCP ports, shell scripts, SSL certificates, system maintenance
- **🔧 Advanced Features** - Adaptive repair, commit log archiving, agent tolerance settings

## Features

### 🎯 Key Capabilities

- **Multi-Cluster Support** - Configure all clusters in your organization or target specific ones
- **Hierarchical Configuration** - Organization-wide defaults with cluster-specific overrides
- **Idempotent Operations** - Safe to run multiple times
- **YAML Validation** - Built-in schema validation for all configurations
- **Enterprise Integrations** - Native support for major alerting and incident management platforms
- **Cross-Platform** - Support for both Apache Cassandra and Apache Kafka

### 📋 Pre-Configured Monitoring

<details>
<summary><b>Metric Alerts (Click to expand)</b></summary>

#### System & Performance
- CPU usage (warning: 90%, critical: 99%)
- Memory utilization (warning: 85%, critical: 95%)
- Disk usage per mount point (warning: 75%, critical: 90%)
- IO wait times (warning: 20%, critical: 50%)
- Garbage collection duration (warning: 5s, critical: 10s)
- NTP time drift monitoring

#### Cassandra-Specific
- Coordinator read/write latencies (per consistency level)
- Read/write timeouts and unavailables
- Dropped messages (mutations, reads, hints)
- Thread pool congestion (blocked tasks, pending requests)
- Compaction backlogs
- Tombstone scanning thresholds
- SSTable counts and bloom filter efficiency
- Hint creation rates
- Cache hit rates

#### Kafka-Specific
- Broker availability
- Controller status
- Network processor utilization
- Request queue sizes
- Offline/under-replicated partitions
- Authentication failures
- Metadata errors

</details>

<details>
<summary><b>Log Alerts (Click to expand)</b></summary>

- Node DOWN events
- TLS/SSL handshake failures
- Gossip message drops
- Stream session failures
- SSTable corruption
- Disk space issues
- JVM memory problems
- Large partition warnings
- Repair monitoring
- Jemalloc loading issues

</details>

<details>
<summary><b>Service Checks (Click to expand)</b></summary>

- Schema agreement validation
- Node status monitoring
- SSL certificate expiration
- System reboot requirements
- AWS maintenance events
- CQL connectivity tests
- Custom shell script checks

</details>

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/axonops/axonops-config-automation.git
cd axonops-config-automation

# 2. Set your environment variables
export AXONOPS_ORG='your-organization'
export AXONOPS_TOKEN='your-api-token'

# 3. Run the playbooks
make endpoints          # Configure alert integrations
make routes            # Set up alert routing
make metrics-alerts    # Create metric-based alerts
make log-alerts        # Create log-based alerts
make service-checks    # Configure health checks
make backups          # Set up backup schedules
```

## Installation

### Prerequisites

- **Ansible** >= 2.10
- **Python** >= 3.8
- **make** (or use the provided `make.sh` script)

### System-Specific Installation

<details>
<summary><b>RedHat/RockyLinux (8+)</b></summary>

```bash
sudo dnf -y install epel-release
sudo dnf -y install ansible make
```
</details>

<details>
<summary><b>Debian/Ubuntu</b></summary>

```bash
sudo apt update
sudo apt -y install ansible make
```
</details>

<details>
<summary><b>Using Virtualenv</b></summary>

```bash
virtualenv ~/py-axonops
source ~/py-axonops/bin/activate
pip3 install -r requirements.txt
```
</details>

<details>
<summary><b>Using Pipenv (Recommended)</b></summary>

```bash
pipenv install
export PIPENV=true
```
</details>

### Environment Configuration

Configure your environment using the provided template:

```bash
# Copy and edit the environment template
cp export_tokens.sh export_tokens.sh.local
vim export_tokens.sh.local

# Source your configuration
source ./export_tokens.sh.local
```

#### Required Variables

```bash
# Organization name (mandatory)
export AXONOPS_ORG='example'

# For AxonOps SaaS
export AXONOPS_TOKEN='your-api-token'

# For AxonOps On-Premise
export AXONOPS_URL='https://your-axonops-instance.com'
export AXONOPS_USERNAME='your-username'
export AXONOPS_PASSWORD='your-password'
# OR for anonymous access
export AXONOPS_ANONYMOUS='true'
```

## Configuration

### Directory Structure

```
config/
├── YOUR_ORG_NAME/                      # Organization-level configs
│   ├── alert_endpoints.yml             # Alert integrations (Slack, PagerDuty, etc.)
│   ├── metric_alert_rules.yml          # Default metric alerts for all clusters
│   ├── log_alert_rules.yml             # Default log alerts for all clusters
│   └── service_checks.yml              # Default service checks for all clusters
│   │
│   └── YOUR_CLUSTER_NAME/              # Cluster-specific overrides
│       ├── metric_alert_rules.yml      # Additional/override metric alerts
│       ├── log_alert_rules.yml         # Additional/override log alerts
│       ├── service_checks.yml          # Additional/override service checks
│       ├── backups.yml                 # Backup configurations
│       └── kafka_metrics_alert_rules.yml  # Kafka-specific alerts
```

### Configuration Hierarchy

1. **Organization Level**: Configurations in `config/ORG_NAME/` apply to all clusters
2. **Cluster Level**: Configurations in `config/ORG_NAME/CLUSTER_NAME/` override or extend organization settings

## Usage

### Available Commands

```bash
make help              # Show all available commands
make validate          # Validate YAML configurations
make endpoints         # Configure alert integrations
make routes           # Set up alert routing rules
make metrics-alerts   # Create metric-based alerts
make log-alerts       # Create log-based alerts  
make service-checks   # Configure service health checks
make backups          # Set up backup schedules
make check            # Run pre-commit tests
```

### Running Playbooks

You can run playbooks using either environment variables or command-line overrides:

```bash
# Using environment variables (after sourcing export_tokens.sh)
make metrics-alerts

# Using command-line overrides
make metrics-alerts AXONOPS_ORG=myorg AXONOPS_CLUSTER=prod-cluster

# Target all clusters (omit AXONOPS_CLUSTER)
make metrics-alerts AXONOPS_ORG=myorg
```

### Validation

Always validate your configurations before applying:

```bash
make validate
```

This will check all YAML files against their schemas and report any errors.

## Examples

### Alert Endpoints

<details>
<summary><b>Slack Integration</b></summary>

```yaml
# config/YOUR_ORG/alert_endpoints.yml
slack:
  - name: ops-team-alerts
    webhook_url: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
    present: true
  
  - name: dev-team-alerts
    webhook_url: https://hooks.slack.com/services/YOUR/OTHER/URL
    present: true
```
</details>

<details>
<summary><b>PagerDuty Integration</b></summary>

```yaml
# config/YOUR_ORG/alert_endpoints.yml
pagerduty:
  - name: critical-incidents
    integration_key: YOUR-PAGERDUTY-INTEGRATION-KEY
    present: true
```
</details>

### Metric Alerts

<details>
<summary><b>CPU Usage Alert</b></summary>

```yaml
# config/YOUR_ORG/metric_alert_rules.yml
axonops_alert_rules:
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
</details>

<details>
<summary><b>Cassandra Latency Alert</b></summary>

```yaml
# config/YOUR_ORG/metric_alert_rules.yml
axonops_alert_rules:
  - name: Read latency critical
    dashboard: Coordinator
    chart: Coordinator Read Latency - LOCAL_QUORUM 99thPercentile
    operator: '>='
    critical_value: 2000000  # 2 seconds in microseconds
    warning_value: 1000000   # 1 second in microseconds
    duration: 15m
    description: High read latency detected
    present: true
```
</details>

### Log Alerts

<details>
<summary><b>Node Down Detection</b></summary>

```yaml
# config/YOUR_ORG/log_alert_rules.yml
axonops_log_alert_rules:
  - name: Node Down
    content: "is now DOWN"
    source: "/var/log/cassandra/system.log"
    warning_value: 1
    critical_value: 5
    duration: 5m
    description: "Cassandra node marked as DOWN"
    level: error,warning
    present: true
```
</details>

### Service Checks

<details>
<summary><b>CQL Port Check</b></summary>

```yaml
# config/YOUR_ORG/service_checks.yml
tcp_checks:
  - name: cql_client_port
    target: "{{.comp_listen_address}}:{{.comp_native_transport_port}}"
    interval: 3m
    timeout: 1m
    present: true
```
</details>

<details>
<summary><b>Custom Shell Script</b></summary>

```yaml
# config/YOUR_ORG/service_checks.yml
shell_checks:
  - name: Check schema agreement
    interval: 5m
    timeout: 1m
    present: true
    command: |
      #!/bin/bash
      SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
      source $SCRIPT_PATH/common.sh
      schemas=$(nodetool gossipinfo | grep -i schema | awk '{print $2}' | sort | uniq | wc -l)
      if [[ $schemas -gt 1 ]]; then
        echo "CRITICAL - Multiple schema versions detected: $schemas"
        exit 2
      fi
      echo "OK - Schema agreement confirmed"
      exit 0
```
</details>

### Backups

<details>
<summary><b>S3 Backup Schedule</b></summary>

```yaml
# config/YOUR_ORG/YOUR_CLUSTER/backups.yml
backups:
  - name: Daily S3 backup
    remote_type: s3
    datacenters: 
      - dc1
    remote_path: my-backup-bucket/cassandra-backups
    local_retention: 10d
    remote_retention: 60d
    tag: "daily-backup"
    timeout: 10h
    remote: true
    schedule: true
    schedule_expr: "0 1 * * *"  # 1 AM daily
    s3_region: us-east-1
    s3_storage_class: STANDARD_IA
    present: true
```
</details>

<details>
<summary><b>Azure Blob Snapshot</b></summary>

```yaml
# config/YOUR_ORG/YOUR_CLUSTER/backups.yml
backups:
  - name: Critical table snapshot
    remote_type: azure
    datacenters:
      - dc1
    remote_path: backups-container/cassandra
    tables:
      - 'critical_keyspace.important_table'
    local_retention: 7d
    remote_retention: 30d
    tag: "critical-data"
    timeout: 2h
    remote: true
    schedule: false  # Immediate snapshot
    azure_account: mystorageaccount
    azure_use_msi: true
    present: true
```
</details>

### Alert Routing

<details>
<summary><b>Route Configuration</b></summary>

```yaml
# config/YOUR_ORG/alert_routes.yml
axonops_alert_routes:
  # Send all critical/error to PagerDuty
  - name: critical-to-pagerduty
    endpoint: critical-incidents
    endpoint_type: pagerduty
    severities:
      - error
      - critical
    override: false
    present: true
  
  # Send warnings to Slack
  - name: warnings-to-slack
    endpoint: ops-team-alerts
    endpoint_type: slack
    severities:
      - warning
    override: false
    present: true
  
  # Route backup alerts to dedicated channel
  - name: backup-alerts
    endpoint: backup-notifications
    endpoint_type: slack
    tags:
      - backup
    severities:
      - info
      - warning
      - error
      - critical
    override: true  # Override default routing
    present: true
```
</details>

## Advanced Configuration

### Using the CLI Tool

In addition to Ansible playbooks, a Python CLI is available for specific operations:

```bash
# Configure adaptive repair
python cli/axonops.py adaptive-repair \
  --cluster my-cluster \
  --enabled true \
  --percentage 20

# View current settings
python cli/axonops.py adaptive-repair \
  --cluster my-cluster \
  --show
```

### Custom Ansible Variables

You can override any Ansible variable:

```bash
# Custom API timeout
make metrics-alerts ANSIBLE_EXTRA_VARS="api_timeout=60"

# Dry run mode
make metrics-alerts ANSIBLE_EXTRA_VARS="check_mode=true"
```

## Troubleshooting

### Common Issues

<details>
<summary><b>Authentication Errors</b></summary>

- Verify your API token has DBA-level access or above
- Check token expiration
- For on-premise, ensure URL includes protocol (https://)
</details>

<details>
<summary><b>Configuration Not Applied</b></summary>

- Run `make validate` to check YAML syntax
- Ensure `present: true` is set for items you want to create
- Check that cluster names match exactly (case-sensitive)
</details>

<details>
<summary><b>Module Import Errors</b></summary>

- Ensure you're using Python 3.8+
- Install dependencies: `pip install -r requirements.txt`
- For pipenv users: ensure `PIPENV=true` is exported
</details>

## Best Practices

1. **Start with Organization Defaults**: Define common alerts at the org level
2. **Use Cluster Overrides Sparingly**: Only for cluster-specific requirements
3. **Validate Before Applying**: Always run `make validate` first
4. **Version Control**: Commit your `config/` directory to track changes
5. **Test in Non-Production**: Apply to test clusters before production
6. **Regular Reviews**: Periodically review and update alert thresholds

## Support

- **Documentation**: [AxonOps Docs](https://axonops.com/docs/)
- **Issues**: [GitHub Issues](https://github.com/axonops/axonops-config-automation/issues)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Additional Resources

- **📚 [Complete Alert Reference Guide](ALERT_REFERENCE.md)** - Detailed documentation of all pre-configured alerts, thresholds, and configurations
- **🔧 [AxonOps Documentation](https://axonops.com/docs/)** - Official AxonOps platform documentation

---

*This project may contain trademarks or logos for projects, products, or services. Any use of third-party trademarks or logos are subject to those third-party's policies. AxonOps is a registered trademark of AxonOps Limited. Apache, Apache Cassandra, Cassandra, Apache Spark, Spark, Apache TinkerPop, TinkerPop, Apache Kafka and Kafka are either registered trademarks or trademarks of the Apache Software Foundation or its subsidiaries in Canada, the United States and/or other countries. Elasticsearch is a trademark of Elasticsearch B.V., registered in the U.S. and in other countries. Docker is a trademark or registered trademark of Docker, Inc. in the United States and/or other countries.*
