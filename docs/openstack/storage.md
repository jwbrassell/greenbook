# OpenStack Storage Guide (Version 17.1)

## Table of Contents
- [OpenStack Storage Guide (Version 17.1)](#openstack-storage-guide-version-171)
  - [Block Storage (Cinder)](#block-storage-cinder)
    - [Configuration](#configuration)
      - [Basic Cinder Configuration](#basic-cinder-configuration)
- [/etc/cinder/cinder.conf](#/etc/cinder/cinderconf)
    - [Volume Operations](#volume-operations)
      - [Basic Volume Management](#basic-volume-management)
- [Create volume](#create-volume)
- [List volumes](#list-volumes)
- [Show volume details](#show-volume-details)
- [Delete volume](#delete-volume)
- [Extend volume size](#extend-volume-size)
      - [Volume Attachments](#volume-attachments)
- [Attach volume to instance](#attach-volume-to-instance)
- [List volume attachments](#list-volume-attachments)
- [Detach volume](#detach-volume)
      - [Volume Snapshots](#volume-snapshots)
- [Create snapshot](#create-snapshot)
- [List snapshots](#list-snapshots)
- [Create volume from snapshot](#create-volume-from-snapshot)
- [Delete snapshot](#delete-snapshot)
      - [Volume Types](#volume-types)
- [Create volume type](#create-volume-type)
- [Set volume type properties](#set-volume-type-properties)
- [List volume types](#list-volume-types)
- [Show volume type details](#show-volume-type-details)
    - [Volume Backup and Restore](#volume-backup-and-restore)
- [Create volume backup](#create-volume-backup)
- [List backups](#list-backups)
- [Show backup details](#show-backup-details)
- [Restore backup to new volume](#restore-backup-to-new-volume)
- [Delete backup](#delete-backup)
  - [Object Storage (Swift)](#object-storage-swift)
    - [Configuration](#configuration)
      - [Proxy Server Configuration](#proxy-server-configuration)
- [/etc/swift/proxy-server.conf](#/etc/swift/proxy-serverconf)
      - [Storage Node Configuration](#storage-node-configuration)
- [/etc/swift/account-server.conf](#/etc/swift/account-serverconf)
- [/etc/swift/container-server.conf](#/etc/swift/container-serverconf)
- [/etc/swift/object-server.conf](#/etc/swift/object-serverconf)
    - [Container Operations](#container-operations)
      - [Basic Container Management](#basic-container-management)
- [Create container](#create-container)
- [List containers](#list-containers)
- [Show container details](#show-container-details)
- [Delete container](#delete-container)
- [Set container metadata](#set-container-metadata)
      - [Object Operations](#object-operations)
- [Upload object](#upload-object)
- [List objects in container](#list-objects-in-container)
- [Download object](#download-object)
- [Delete object](#delete-object)
- [Show object metadata](#show-object-metadata)
    - [Access Control](#access-control)
      - [Container Access Control](#container-access-control)
- [Make container public](#make-container-public)
- [Make container private](#make-container-private)
- [Set container read ACL](#set-container-read-acl)
- [Set container write ACL](#set-container-write-acl)
    - [Storage Policies](#storage-policies)
      - [Managing Storage Policies](#managing-storage-policies)
- [List storage policies](#list-storage-policies)
- [Create new storage policy](#create-new-storage-policy)
- [Edit /etc/swift/swift.conf](#edit-/etc/swift/swiftconf)
    - [Maintenance Operations](#maintenance-operations)
      - [Ring Management](#ring-management)
- [Create account ring](#create-account-ring)
- [Add devices to ring](#add-devices-to-ring)
- [Rebalance rings](#rebalance-rings)
      - [System Maintenance](#system-maintenance)
- [Check cluster health](#check-cluster-health)
- [Verify ring consistency](#verify-ring-consistency)
- [Run object auditor](#run-object-auditor)
- [Clean up expired objects](#clean-up-expired-objects)
    - [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
      - [Monitoring](#monitoring)
- [Check cluster status](#check-cluster-status)
- [Check disk usage](#check-disk-usage)
- [Check replication status](#check-replication-status)
- [Check async pending](#check-async-pending)
      - [Log Analysis](#log-analysis)
- [View proxy server logs](#view-proxy-server-logs)
- [View account server logs](#view-account-server-logs)
- [View container server logs](#view-container-server-logs)
- [View object server logs](#view-object-server-logs)
    - [Backup and Recovery](#backup-and-recovery)
      - [Backup Procedures](#backup-procedures)
- [Backup Swift configuration](#backup-swift-configuration)
- [Backup ring files](#backup-ring-files)
- [Export container metadata](#export-container-metadata)



This guide covers storage management in OpenStack, including both block storage (Cinder) and object storage (Swift).

## Block Storage (Cinder)

### Configuration

#### Basic Cinder Configuration
```ini
# /etc/cinder/cinder.conf
[DEFAULT]
auth_strategy = keystone
enabled_backends = lvm
transport_url = rabbit://openstack:RABBIT_PASS@controller
glance_api_servers = http://controller:9292

[database]
connection = mysql+pymysql://cinder:CINDER_DBPASS@controller/cinder

[keystone_authtoken]
www_authenticate_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = cinder
password = CINDER_PASS

[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
target_protocol = iscsi
target_helper = tgtadm
```

### Volume Operations

#### Basic Volume Management
```bash
# Create volume
openstack volume create --size 10 my-volume

# List volumes
openstack volume list

# Show volume details
openstack volume show my-volume

# Delete volume
openstack volume delete my-volume

# Extend volume size
openstack volume set --size 20 my-volume
```

#### Volume Attachments
```bash
# Attach volume to instance
openstack server add volume my-instance my-volume

# List volume attachments
openstack server volume list my-instance

# Detach volume
openstack server remove volume my-instance my-volume
```

#### Volume Snapshots
```bash
# Create snapshot
openstack volume snapshot create --volume my-volume my-snapshot

# List snapshots
openstack volume snapshot list

# Create volume from snapshot
openstack volume create --snapshot my-snapshot --size 10 new-volume

# Delete snapshot
openstack volume snapshot delete my-snapshot
```

#### Volume Types
```bash
# Create volume type
openstack volume type create ssd

# Set volume type properties
openstack volume type set --property volume_backend_name=lvm ssd

# List volume types
openstack volume type list

# Show volume type details
openstack volume type show ssd
```

### Volume Backup and Restore

```bash
# Create volume backup
openstack volume backup create --name my-backup my-volume

# List backups
openstack volume backup list

# Show backup details
openstack volume backup show my-backup

# Restore backup to new volume
openstack volume backup restore my-backup new-volume

# Delete backup
openstack volume backup delete my-backup
```

## Object Storage (Swift)

### Configuration

#### Proxy Server Configuration
```ini
# /etc/swift/proxy-server.conf
[DEFAULT]
bind_port = 8080
user = swift
swift_dir = /etc/swift

[pipeline:main]
pipeline = catch_errors gatekeeper healthcheck proxy-logging cache container_sync bulk ratelimit authtoken keystoneauth container-quotas account-quotas slo dlo versioned_writes proxy-logging proxy-server

[filter:keystoneauth]
use = egg:swift#keystoneauth
operator_roles = admin,swiftoperator
```

#### Storage Node Configuration
```ini
# /etc/swift/account-server.conf
[DEFAULT]
bind_ip = STORAGE_NODE_IP
bind_port = 6202
user = swift
swift_dir = /etc/swift
devices = /srv/node

[pipeline:main]
pipeline = healthcheck recon account-server

# /etc/swift/container-server.conf
[DEFAULT]
bind_ip = STORAGE_NODE_IP
bind_port = 6201
user = swift
swift_dir = /etc/swift
devices = /srv/node

[pipeline:main]
pipeline = healthcheck recon container-server

# /etc/swift/object-server.conf
[DEFAULT]
bind_ip = STORAGE_NODE_IP
bind_port = 6200
user = swift
swift_dir = /etc/swift
devices = /srv/node

[pipeline:main]
pipeline = healthcheck recon object-server
```

### Container Operations

#### Basic Container Management
```bash
# Create container
openstack container create my-container

# List containers
openstack container list

# Show container details
openstack container show my-container

# Delete container
openstack container delete my-container

# Set container metadata
openstack container set --property "description=My Files" my-container
```

#### Object Operations
```bash
# Upload object
openstack object create my-container myfile.txt

# List objects in container
openstack object list my-container

# Download object
openstack object save my-container myfile.txt

# Delete object
openstack object delete my-container myfile.txt

# Show object metadata
openstack object show my-container myfile.txt
```

### Access Control

#### Container Access Control
```bash
# Make container public
openstack container set --property access=public my-container

# Make container private
openstack container set --property access=private my-container

# Set container read ACL
openstack container set --read-acl ".r:*,.rlistings" my-container

# Set container write ACL
openstack container set --write-acl "project:team1" my-container
```

### Storage Policies

#### Managing Storage Policies
```bash
# List storage policies
swift-ring-builder object.builder

# Create new storage policy
# Edit /etc/swift/swift.conf
[storage-policy:0]
name = policy-0
default = yes

[storage-policy:1]
name = policy-1
deprecated = no
```

### Maintenance Operations

#### Ring Management
```bash
# Create account ring
swift-ring-builder account.builder create 10 3 1

# Add devices to ring
swift-ring-builder account.builder add --region 1 --zone 1 \
  --ip STORAGE_NODE_IP --port 6202 --device sdb --weight 100

# Rebalance rings
swift-ring-builder account.builder rebalance
swift-ring-builder container.builder rebalance
swift-ring-builder object.builder rebalance
```

#### System Maintenance
```bash
# Check cluster health
swift-dispersion-report

# Verify ring consistency
swift-ring-builder-analyzer

# Run object auditor
swift-object-auditor /etc/swift/object-server.conf once

# Clean up expired objects
swift-container-updater /etc/swift/container-server.conf
```

### Monitoring and Troubleshooting

#### Monitoring
```bash
# Check cluster status
swift-recon --all

# Check disk usage
swift-recon --disk

# Check replication status
swift-recon --replication

# Check async pending
swift-recon --async
```

#### Log Analysis
```bash
# View proxy server logs
tail -f /var/log/swift/proxy-server.log

# View account server logs
tail -f /var/log/swift/account-server.log

# View container server logs
tail -f /var/log/swift/container-server.log

# View object server logs
tail -f /var/log/swift/object-server.log
```

### Backup and Recovery

#### Backup Procedures
```bash
# Backup Swift configuration
tar -czf swift_config_backup.tar.gz /etc/swift/

# Backup ring files
cp /etc/swift/*.ring.gz /backup/swift/rings/

# Export container metadata
for container in $(openstack container list -f value -c Name); do
    openstack container show $container > /backup/swift/metadata/$container.json
done
```

For more detailed information about storage features and configurations, refer to:
- [Cinder Documentation](https://docs.openstack.org/cinder/latest/)
- [Swift Documentation](https://docs.openstack.org/swift/latest/)
