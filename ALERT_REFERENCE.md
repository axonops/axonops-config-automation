# AxonOps Alert Reference Guide

This document provides a comprehensive reference for all pre-configured alerts, service checks, and backup configurations available in the AxonOps Configuration Automation framework.

## Table of Contents

- [Metric Alerts](#metric-alerts)
  - [System Metrics](#system-metrics)
  - [Coordinator Metrics](#coordinator-metrics)
  - [Thread Pool & Performance](#thread-pool--performance)
  - [Dropped Messages](#dropped-messages)
  - [Entropy & Hints](#entropy--hints)
  - [Cache Performance](#cache-performance)
  - [Security Metrics](#security-metrics)
  - [Table-Level Metrics](#table-level-metrics)
  - [Kafka Metrics](#kafka-metrics)
- [Log Alerts](#log-alerts)
  - [Critical System Events](#critical-system-events)
  - [Performance & Repair Events](#performance--repair-events)
  - [Security & Configuration](#security--configuration)
- [Service Checks](#service-checks)
  - [Health Check Scripts](#health-check-scripts)
  - [TCP Port Checks](#tcp-port-checks)
- [Backup Configuration](#backup-configuration)

## Metric Alerts

### System Metrics

| Alert Name | Dashboard | Chart | Warning | Critical | Duration | Description |
|------------|-----------|-------|---------|----------|----------|-------------|
| CPU usage per host | System | CPU usage per host | ≥90% | ≥99% | 1h | Detected High CPU usage |
| CPU is Underutilized | System | CPU usage per host | ≤5% | ≤1% | 1w | CPU load has been very low for 1 week |
| Disk % Usage $mountpoint | System | Disk % Usage $mountpoint | ≥75% | ≥90% | 12h | Detected High disk utilization |
| Avg IO wait CPU per Host | System | Avg IO wait CPU per Host | ≥20% | ≥50% | 2h | Detected high Average IOWait |
| GC duration | System | GC duration | ≥5000ms | ≥10000ms | 2m | Detected high Garbage Collection cycle time |
| Used Memory Percentage | System | Used Memory Percentage | ≥95% | ≥85% | 1h | High memory utilization detected |
| Memory is Underutilized | System | Used Memory Percentage | ≤20% | ≤10% | 1w | Node memory has been very low for 1 week |
| NTP offset (milliseconds) | System | NTP offset (milliseconds) | ≥5ms | ≥10ms | 15m | High NTP time offset detected |

### Coordinator Metrics

| Alert Name | Dashboard | Chart | Warning | Critical | Duration | Description |
|------------|-----------|-------|---------|----------|----------|-------------|
| Coordinator Read Latency - LOCAL_QUORUM 99thPercentile | Coordinator | Read Latency - LOCAL_QUORUM | ≥1000000μs | ≥2000000μs | 15m | High read latency at LOCAL_QUORUM |
| Coordinator Read Latency - LOCAL_ONE 99thPercentile | Coordinator | Read Latency - LOCAL_ONE | ≥1000000μs | ≥2000000μs | 15m | High read latency at LOCAL_ONE |
| Coordinator Range Read Latency - 99thPercentile | Coordinator | Range Read Latency | ≥1500000μs | ≥2500000μs | 15m | High range read latency |
| Coordinator Write Latency - LOCAL_QUORUM 99thPercentile | Coordinator | Write Latency - LOCAL_QUORUM | ≥1000000μs | ≥1500000μs | 15m | High write latency at LOCAL_QUORUM |
| Coordinator Write Latency - LOCAL_ONE 99thPercentile | Coordinator | Write Latency - LOCAL_ONE | ≥1000000μs | ≥1500000μs | 15m | High write latency at LOCAL_ONE |
| Coordinator Read Timeouts Per Second | Coordinator | Read Timeouts | ≥2 | ≥5 | 10m | Excessive read timeouts |
| Coordinator Write Timeouts Per Second | Coordinator | Write Timeouts | ≥2 | ≥5 | 10m | Excessive write timeouts |
| Coordinator Read Unavailables Per Second | Coordinator | Read Unavailables | ≥10 | ≥100 | 1h | Read unavailable errors |
| Coordinator Write Unavailables Per Second | Coordinator | Write Unavailables | ≥10 | ≥100 | 1h | Write unavailable errors |
| CAS Read/Write Failures | Coordinator | CAS Operations | ≥10 | ≥100 | 30m | Compare-and-swap operation failures |

### Thread Pool & Performance

| Alert Name | Dashboard | Chart | Warning | Critical | Duration | Description |
|------------|-----------|-------|---------|----------|----------|-------------|
| Total Blocked Tasks Rate | Thread Pool Stats | Total Blocked Tasks Rate | ≥64 | ≥128 | 15m | Thread pool congestion |
| Total Blocked Compaction Tasks Rate | Thread Pool Stats | Blocked Compaction Tasks | ≥16 | ≥32 | 15m | Compaction thread pool blocked |
| Pending Native_Transport_Requests | Thread Pool Stats | Native Transport | ≥500 | ≥1000 | 15m | Client request backlog |
| Pending ReadStage | Thread Pool Stats | ReadStage | ≥500 | ≥1000 | 15m | Read operations backlog |
| Pending MutationStage | Thread Pool Stats | MutationStage | ≥500 | ≥1000 | 15m | Write operations backlog |
| Total Blocked Flush Writer Tasks Rate | Thread Pool Stats | Flush Writer | ≥16 | ≥32 | 10m | Memtable flush backlog |
| Total Blocked Repair_Task | Thread Pool Stats | Repair Task | ≥64 | ≥128 | 1h | Repair operations blocked |
| Pending Repair_Task | Thread Pool Stats | Repair Task | ≥128 | ≥256 | 3h | Repair operations pending |
| Pending TP Compaction Tasks | Thread Pool Stats | Compaction Tasks | ≥200 | ≥500 | 4h | Compaction backlog |

### Dropped Messages

| Alert Name | Dashboard | Chart | Warning | Critical | Duration | Description |
|------------|-----------|-------|---------|----------|----------|-------------|
| Dropped Mutations | Dropped Messages | Mutations | ≥1 | ≥1 | 30s | Write operations dropped |
| Dropped Reads | Dropped Messages | Reads | ≥1 | ≥1 | 30s | Read operations dropped |
| Dropped Hints | Dropped Messages | Hints | ≥1 | ≥1 | 10m | Hint messages dropped |

### Entropy & Hints

| Alert Name | Dashboard | Chart | Warning | Critical | Duration | Description |
|------------|-----------|-------|---------|----------|----------|-------------|
| Total Hints Created By Each Node | Entropy | Hints Created | ≥50 | ≥100 | 2h | Excessive hint creation |

### Cache Performance

| Alert Name | Dashboard | Chart | Warning | Critical | Duration | Description |
|------------|-----------|-------|---------|----------|----------|-------------|
| KeyCache HitRate Per node | Cache | KeyCache HitRate | ≤0.03 | ≤0.01 | 20m | Poor key cache performance |

### Security Metrics

| Alert Name | Dashboard | Chart | Warning | Critical | Duration | Description |
|------------|-----------|-------|---------|----------|----------|-------------|
| Failed Authentications | Security | Auth Failures | ≥1 | ≥20 | 3m | Authentication failures detected |
| JMX connections | Security | JMX Connections | ≥10 | ≥100 | 3m | Excessive JMX connections |
| Failed Authorizations | Security | Authz Failures | ≥5 | ≥20 | 3m | Authorization failures detected |
| DDL queries | Security | DDL Operations | ≥5 | ≥100 | 3m | Schema modification activity |
| DCL queries | Security | DCL Operations | ≥5 | ≥100 | 3m | Permission modification activity |
| DML queries | Security | DML Operations | ≥5 | ≥100 | 3m | Data modification activity |

### Table-Level Metrics

These alerts are configured per table. The example below shows system.peers, but can be applied to any table:

| Alert Name | Table | Warning | Critical | Duration | Description |
|------------|-------|---------|----------|----------|-------------|
| Tombstones Scanned per Table - 99thPercentile | system.peers | ≥500 | ≥1000 | 3h | High tombstone scanning rate |
| Max Partition Size | system.peers | ≥100MB | ≥200MB | 6h | Large partition detected |
| Bloom Filter False Positive Ratio | system.peers | ≥0.03 | ≥0.05 | 3h | High false positive rate |
| SSTables Read Per Query - 99thPercentile | system.peers | ≥15 | ≥50 | 2h | Too many SSTables per read |
| Live SSTables | system.peers | ≥100 | ≥300 | 6h | High SSTable count |
| Speculative Retries | system.peers | ≥200 | ≥500 | 2h | High speculative retry rate |

### Kafka Metrics

For Kafka clusters, the following alerts are available:

| Alert Name | Dashboard | Warning | Critical | Duration | Description |
|------------|-----------|---------|----------|----------|-------------|
| Brokers Down | Kafka Overview | <4 | <4 | 15m | Kafka brokers are down |
| Multiple Active Controllers | Kafka Controller | ≥2 | ≥2 | 5m | Split-brain scenario detected |
| Network Processor Avg Idle Percent | Kafka Network | <20% | <10% | 15m | Network processor overloaded |
| Request Queue Size | Kafka Request | >20 | >10 | 15m | Request queue backing up |
| Offline Partitions | Kafka Partitions | ≥1 | ≥10 | 5m | Partitions are offline |
| Under Min ISR Partitions | Kafka Partitions | ≥1 | ≥1 | 5m | Under-replicated partitions |
| Under Replicated Partitions | Kafka Partitions | ≥1 | ≥1 | 5m | Replication lag detected |
| Fenced Broker Count | Kafka Brokers | ≥1 | ≥1 | 5m | Brokers fenced from cluster |
| Metadata Error Rate | Kafka Metadata | ≥1 | ≥1 | 15m | Metadata operation errors |
| Failed Auth Rate | Kafka Security | ≥10 | ≥50 | 15m | Authentication failures |

## Log Alerts

### Critical System Events

| Alert Name | Search Pattern | Warning | Critical | Duration | Log Level | Description |
|------------|----------------|---------|----------|----------|-----------|-------------|
| Node Down | "is now DOWN" | ≥1 | ≥5 | 5m | error,warning | Cassandra node marked as DOWN |
| Corrupt SSTable | "Corrupt sstable" | ≥1 | ≥1 | 10s | error | SSTable corruption detected |
| Failed stream session | "failed stream session" | ≥1 | ≥1 | 5ms | error | Streaming operation failed |
| Unable to compact due to disk space | "Not enough space for compaction" | ≥1 | ≥1 | 15m | error | Disk space preventing compaction |
| Unable to lock JVM memory | "Unable to lock JVM memory (ENOMEM)" | ≥1 | ≥1 | 15m | error | Memory locking failed |
| Unknown mlockall error | "Unknown mlockall error" | ≥1 | ≥1 | 15m | error | Memory locking error |
| Maximum memory usage reached | "networking buffer pool, cannot allocate chunk of" | ≥1 | ≥1 | 15m | error | Network buffer exhausted |

### Performance & Repair Events

| Alert Name | Search Pattern | Warning | Critical | Duration | Description |
|------------|----------------|---------|----------|----------|-------------|
| Writing large partition | "Writing large partition" | ≥1 | ≥500 | 15m | Large partitions being written |
| Repair not in progress | "repair" | <1 | <1 | 24h | No repairs running for 24h (uses < operator) |
| Anticompaction | "Starting anticompaction" | ≥1 | ≥1000 | 5m | Anticompaction activity |
| Dropped messages during repairs | "LARGE_MESSAGES-[a-zA-Z0-9]+ overloaded" | ≥1 | ≥500 | 15m | Node overloaded during repair |
| Dropping gossip message | "dropping message of type GOSSIP" | ≥1 | ≥1 | 1m | Gossip messages being dropped |

### Security & Configuration

| Alert Name | Search Pattern | Warning | Critical | Duration | Description |
|------------|----------------|---------|----------|----------|-------------|
| TLS handshake failure | "Failed to handshake with peer" | ≥50 | ≥100 | 5m | SSL/TLS handshake failures |
| Unsupported Protocol | "Invalid or unsupported protocol version" | ≥1 | ≥30 | 5m | Protocol version mismatch |
| JNA not found | "JNA not found" | ≥1 | ≥1 | 30s | Java Native Access missing |
| Obsolete JNA version | "Obsolete version of JNA present" | ≥1 | ≥1 | 15m | Outdated JNA library |
| Jemalloc not loaded | "jemalloc shared library could not be preloaded" | ≥1 | ≥500 | 15m | Memory allocator not loaded |
| Unsupported OS | "the current operating system" | ≥1 | ≥1 | 15m | Operating system not supported |

## Service Checks

### Health Check Scripts

| Check Name | Type | Interval | Timeout | Description | Script Purpose |
|------------|------|----------|---------|-------------|----------------|
| Check for schema disagreement | Shell | 5m | 1m | Validates all nodes have same schema version | Uses nodetool gossipinfo to detect schema variations |
| Check for node DOWN | Shell | 30s | 1m | Checks for DOWN nodes by DC and rack | Monitors cluster health and node availability |
| SSL certificate check | Shell | 12h | 1m | Validates SSL cert expiration and OCSP | Warns 5-10 days before certificate expiration |
| Debian/Ubuntu - Check host needs reboot | Shell | 12h | 1m | Checks if system reboot needed | Looks for /var/run/reboot-required file |
| Check AWS events | Shell | 12h | 1m | Queries AWS metadata for scheduled events | Detects upcoming AWS maintenance windows |
| Cassandra CQL Consistency Level Test | Shell | 12h | 1m | Tests read operations at different consistency levels | Validates EACH_QUORUM, LOCAL_QUORUM, and LOCAL_ONE |

### TCP Port Checks

| Check Name | Target | Interval | Description |
|------------|--------|----------|-------------|
| cql_client_port | {{.comp_listen_address}}:{{.comp_native_transport_port}} | 3m | Verifies Cassandra CQL port availability |

## Backup Configuration

### General Backup Options

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| present | No | true | Whether backup schedule should exist. Set to false to remove |
| local_retention | No | 10d | How long to keep snapshots on local node |
| remote_retention | No | 60d | How long to keep snapshots on remote location |
| remote_type | Yes (if remote) | local | Destination type: local, s3, sftp, azure |
| timeout | No | 10h | Time before backup operation times out |
| transfers | No | - | Number of parallel file transfers |
| tps_limit | No | - | Throttle transfer operations per second |
| bw_limit | No | 0 | Bandwidth limit (e.g., 10M = 10MB/s, 0 = unlimited) |
| tag | No | - | Tag to apply to the backup |
| datacenters | Yes | - | List of datacenters to include in backup |
| nodes | No | - | Specific nodes to include (optional) |
| tables_keyspace | No | - | Tables to backup (mutually exclusive with tables) |
| tables | No | - | Specific tables to backup (mutually exclusive with tables_keyspace) |
| keyspaces | No | - | Keyspaces to include in backup |
| schedule | No | false | Whether to schedule or take immediate snapshot |
| schedule_expr | No | '0 1 * * *' | Cron expression for scheduled backups |

### S3-Specific Options

| Parameter | Required | Description |
|-----------|----------|-------------|
| remote_path | Yes | S3 path including bucket (e.g., mybucket/path/to/backups) |
| s3_region | Yes | AWS region where bucket is located |
| s3_access_key_id | No | AWS access key (if not using IAM) |
| s3_secret_access_key | No | AWS secret key (if not using IAM) |
| s3_storage_class | No | Storage class: STANDARD, STANDARD_IA, GLACIER, etc. |
| s3_acl | No | ACL setting: private, public-read, etc. |
| s3_encryption | No | Encryption type: none or AES256 |
| s3_no_check_bucket | No | Skip bucket validation |
| s3_disable_checksum | No | Disable checksum validation |

### Azure-Specific Options

| Parameter | Required | Description |
|-----------|----------|-------------|
| remote_path | Yes | Azure path including container (e.g., mycontainer/path) |
| azure_account | Yes | Azure storage account name |
| azure_endpoint | No | Override endpoint for storage account |
| azure_key | No | Storage account key (if not using MSI) |
| azure_msi | No | Use Azure Managed Service Identity |
| azure_msi_object_id | No | MSI object ID (if multiple identities) |
| azure_msi_client_id | No | MSI client ID (if multiple identities) |
| azure_msi_mi_res_id | No | MSI resource ID (if multiple identities) |

### SFTP-Specific Options

| Parameter | Required | Description |
|-----------|----------|-------------|
| remote_path | Yes | Path on remote SFTP server |
| host | Yes | SFTP server hostname or IP |
| ssh_user | Yes | SSH username for connection |
| ssh_pass | No | SSH password (if not using key) |
| key_file | No | Path to SSH key file (if not using password) |

## Alert Configuration Tips

### Setting Appropriate Thresholds

1. **Start Conservative**: Begin with the provided thresholds and adjust based on your workload
2. **Consider Workload Patterns**: Batch processing may require different thresholds than real-time operations
3. **Account for Peak Times**: Ensure thresholds don't trigger false positives during expected high-load periods
4. **Test in Non-Production**: Validate alert sensitivity in test environments first

### Duration Settings

- **Short Duration (< 5m)**: For critical issues requiring immediate attention
- **Medium Duration (5m - 1h)**: For performance degradation that needs investigation
- **Long Duration (> 1h)**: For trend-based alerts and capacity planning

### Alert Routing Best Practices

1. **Severity-Based Routing**:
   - Critical → PagerDuty/OpsGenie (wake someone up)
   - Warning → Slack/Teams (notify during business hours)
   - Info → Email/Dashboard (for reporting)

2. **Tag-Based Routing**:
   - Use tags to route specific alert types (backup, security, performance)
   - Override default routing for specialized teams

3. **Time-Based Considerations**:
   - Consider different routing for business hours vs. after-hours
   - Use escalation policies in your alerting platform

## Customization

All alerts can be customized by:

1. **Modifying Thresholds**: Adjust warning/critical values
2. **Changing Duration**: Modify how long a condition must persist
3. **Adding Descriptions**: Provide context-specific guidance
4. **Setting present: false**: Disable alerts that aren't relevant
5. **Creating New Alerts**: Use existing alerts as templates

Remember to validate your configurations using `make validate` before applying changes.