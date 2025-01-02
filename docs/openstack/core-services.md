# OpenStack Core Services (Version 17.1)

## Table of Contents
- [OpenStack Core Services (Version 17.1)](#openstack-core-services-version-171)
  - [Nova (Compute Service)](#nova-compute-service)
    - [Configuration](#configuration)
- [/etc/nova/nova.conf](#/etc/nova/novaconf)
    - [Common Operations](#common-operations)
- [List compute services](#list-compute-services)
- [Create a new instance](#create-a-new-instance)
- [List instances](#list-instances)
- [Stop/Start/Reboot instance](#stop/start/reboot-instance)
- [Delete instance](#delete-instance)
- [Show instance details](#show-instance-details)
  - [Neutron (Networking Service)](#neutron-networking-service)
    - [Configuration](#configuration)
- [/etc/neutron/neutron.conf](#/etc/neutron/neutronconf)
    - [Common Operations](#common-operations)
- [List networks](#list-networks)
- [Create private network](#create-private-network)
- [Create router](#create-router)
- [List ports](#list-ports)
- [Show network details](#show-network-details)
  - [Cinder (Block Storage Service)](#cinder-block-storage-service)
    - [Configuration](#configuration)
- [/etc/cinder/cinder.conf](#/etc/cinder/cinderconf)
    - [Common Operations](#common-operations)
- [List volumes](#list-volumes)
- [Create volume](#create-volume)
- [Attach volume to instance](#attach-volume-to-instance)
- [Detach volume](#detach-volume)
- [Delete volume](#delete-volume)
- [Create volume snapshot](#create-volume-snapshot)
  - [Keystone (Identity Service)](#keystone-identity-service)
    - [Configuration](#configuration)
- [/etc/keystone/keystone.conf](#/etc/keystone/keystoneconf)
    - [Common Operations](#common-operations)
- [List users](#list-users)
- [Create user](#create-user)
- [List projects](#list-projects)
- [Create project](#create-project)
- [Create role](#create-role)
- [Assign role to user](#assign-role-to-user)
- [Create service](#create-service)
  - [Glance (Image Service)](#glance-image-service)
    - [Configuration](#configuration)
- [/etc/glance/glance-api.conf](#/etc/glance/glance-apiconf)
    - [Common Operations](#common-operations)
- [List images](#list-images)
- [Create image](#create-image)
- [Show image details](#show-image-details)
- [Delete image](#delete-image)
- [Update image properties](#update-image-properties)
  - [Swift (Object Storage Service)](#swift-object-storage-service)
    - [Configuration](#configuration)
- [/etc/swift/proxy-server.conf](#/etc/swift/proxy-serverconf)
    - [Common Operations](#common-operations)
- [List containers](#list-containers)
- [Create container](#create-container)
- [Upload object](#upload-object)
- [Download object](#download-object)
- [List objects in container](#list-objects-in-container)
- [Delete object](#delete-object)
  - [Service Management](#service-management)
    - [Starting/Stopping Services](#starting/stopping-services)
- [Nova services](#nova-services)
- [Neutron services](#neutron-services)
- [Cinder services](#cinder-services)
- [Glance services](#glance-services)
    - [Service Status Check](#service-status-check)
- [Check all OpenStack services](#check-all-openstack-services)
- [Check compute services](#check-compute-services)
- [Check network agents](#check-network-agents)
- [Check block storage services](#check-block-storage-services)
  - [Maintenance Operations](#maintenance-operations)
    - [Database Management](#database-management)
- [Backup databases](#backup-databases)
- [Clean up deleted instances](#clean-up-deleted-instances)
- [Sync database schema](#sync-database-schema)
    - [Log Management](#log-management)
- [View service logs](#view-service-logs)
- [Clear old logs](#clear-old-logs)



This document provides detailed information about OpenStack core services, their configurations, and common management operations.

## Nova (Compute Service)

### Configuration
```ini
# /etc/nova/nova.conf
[DEFAULT]
compute_driver = libvirt.LibvirtDriver
default_schedule_zone = nova
metadata_workers = 4
osapi_compute_workers = 4

[api_database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller/nova_api

[database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller/nova

[placement]
auth_url = http://controller:5000/v3
auth_type = password
project_domain_name = Default
project_name = service
user_domain_name = Default
username = placement
password = PLACEMENT_PASS
```

### Common Operations
```bash
# List compute services
openstack compute service list

# Create a new instance
openstack server create --flavor m1.small --image ubuntu-20.04 \
  --network private-net --security-group default my-instance

# List instances
openstack server list

# Stop/Start/Reboot instance
openstack server stop my-instance
openstack server start my-instance
openstack server reboot my-instance

# Delete instance
openstack server delete my-instance

# Show instance details
openstack server show my-instance
```

## Neutron (Networking Service)

### Configuration
```ini
# /etc/neutron/neutron.conf
[DEFAULT]
core_plugin = ml2
service_plugins = router
auth_strategy = keystone
notify_nova_on_port_status_changes = true
notify_nova_on_port_data_changes = true

[database]
connection = mysql+pymysql://neutron:NEUTRON_DBPASS@controller/neutron

[keystone_authtoken]
www_authenticate_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = NEUTRON_PASS
```

### Common Operations
```bash
# List networks
openstack network list

# Create private network
openstack network create private-net
openstack subnet create private-subnet \
  --network private-net \
  --subnet-range 192.168.1.0/24 \
  --dns-nameserver 8.8.8.8

# Create router
openstack router create main-router
openstack router add subnet main-router private-subnet
openstack router set --external-gateway provider main-router

# List ports
openstack port list

# Show network details
openstack network show private-net
```

## Cinder (Block Storage Service)

### Configuration
```ini
# /etc/cinder/cinder.conf
[DEFAULT]
rootwrap_config = /etc/cinder/rootwrap.conf
api_paste_confg = /etc/cinder/api-paste.ini
auth_strategy = keystone
state_path = /var/lib/cinder
lock_path = /var/lock/cinder
volumes_dir = /var/lib/cinder/volumes

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
```

### Common Operations
```bash
# List volumes
openstack volume list

# Create volume
openstack volume create --size 10 my-volume

# Attach volume to instance
openstack server add volume my-instance my-volume

# Detach volume
openstack server remove volume my-instance my-volume

# Delete volume
openstack volume delete my-volume

# Create volume snapshot
openstack volume snapshot create --volume my-volume my-snapshot
```

## Keystone (Identity Service)

### Configuration
```ini
# /etc/keystone/keystone.conf
[DEFAULT]
log_dir = /var/log/keystone

[database]
connection = mysql+pymysql://keystone:KEYSTONE_DBPASS@controller/keystone

[token]
provider = fernet
expiration = 3600
```

### Common Operations
```bash
# List users
openstack user list

# Create user
openstack user create --password-prompt my-user

# List projects
openstack project list

# Create project
openstack project create --description "My Project" my-project

# Create role
openstack role create my-role

# Assign role to user
openstack role add --project my-project --user my-user my-role

# Create service
openstack service create --name glance \
  --description "OpenStack Image" image
```

## Glance (Image Service)

### Configuration
```ini
# /etc/glance/glance-api.conf
[DEFAULT]
bind_host = 0.0.0.0

[database]
connection = mysql+pymysql://glance:GLANCE_DBPASS@controller/glance

[keystone_authtoken]
www_authenticate_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = glance
password = GLANCE_PASS
```

### Common Operations
```bash
# List images
openstack image list

# Create image
openstack image create "ubuntu-20.04" \
  --file ubuntu-20.04-server-cloudimg-amd64.img \
  --disk-format qcow2 --container-format bare \
  --public

# Show image details
openstack image show ubuntu-20.04

# Delete image
openstack image delete ubuntu-20.04

# Update image properties
openstack image set --property hw_disk_bus=scsi ubuntu-20.04
```

## Swift (Object Storage Service)

### Configuration
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

### Common Operations
```bash
# List containers
openstack container list

# Create container
openstack container create my-container

# Upload object
openstack object create my-container my-file.txt

# Download object
openstack object save my-container my-file.txt

# List objects in container
openstack object list my-container

# Delete object
openstack object delete my-container my-file.txt
```

## Service Management

### Starting/Stopping Services
```bash
# Nova services
sudo systemctl start/stop/restart nova-api
sudo systemctl start/stop/restart nova-scheduler
sudo systemctl start/stop/restart nova-conductor
sudo systemctl start/stop/restart nova-compute

# Neutron services
sudo systemctl start/stop/restart neutron-server
sudo systemctl start/stop/restart neutron-linuxbridge-agent
sudo systemctl start/stop/restart neutron-dhcp-agent
sudo systemctl start/stop/restart neutron-metadata-agent

# Cinder services
sudo systemctl start/stop/restart cinder-api
sudo systemctl start/stop/restart cinder-scheduler
sudo systemctl start/stop/restart cinder-volume

# Glance services
sudo systemctl start/stop/restart glance-api
```

### Service Status Check
```bash
# Check all OpenStack services
openstack service list

# Check compute services
openstack compute service list

# Check network agents
openstack network agent list

# Check block storage services
openstack volume service list
```

## Maintenance Operations

### Database Management
```bash
# Backup databases
mysqldump --all-databases > openstack_backup.sql

# Clean up deleted instances
nova-manage db archive_deleted_rows --max_rows 100

# Sync database schema
keystone-manage db_sync
nova-manage api_db sync
nova-manage cell_v2 map_cell0
cinder-manage db sync
```

### Log Management
```bash
# View service logs
sudo tail -f /var/log/nova/nova-api.log
sudo tail -f /var/log/neutron/neutron-server.log
sudo tail -f /var/log/cinder/cinder-api.log
sudo tail -f /var/log/glance/api.log

# Clear old logs
sudo find /var/log/nova -name "*.log.*" -mtime +30 -delete
```

For more detailed information about each service, refer to the [official OpenStack documentation](https://docs.openstack.org/).
