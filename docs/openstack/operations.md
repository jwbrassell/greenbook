# OpenStack Common Operations Guide (Version 17.1)

## Table of Contents
- [OpenStack Common Operations Guide (Version 17.1)](#openstack-common-operations-guide-version-171)
  - [Instance Management](#instance-management)
    - [Create and Manage Instances](#create-and-manage-instances)
- [Create new instance](#create-new-instance)
- [List instances](#list-instances)
- [Get instance details](#get-instance-details)
- [Stop instance](#stop-instance)
- [Start instance](#start-instance)
- [Reboot instance](#reboot-instance)
- [Delete instance](#delete-instance)
- [Create instance snapshot](#create-instance-snapshot)
    - [Instance Troubleshooting](#instance-troubleshooting)
- [Get console output](#get-console-output)
- [Get VNC console URL](#get-vnc-console-url)
- [Check instance status](#check-instance-status)
- [View instance actions](#view-instance-actions)
  - [Image Management](#image-management)
    - [Manage Images](#manage-images)
- [Upload new image](#upload-new-image)
- [List images](#list-images)
- [Show image details](#show-image-details)
- [Update image properties](#update-image-properties)
- [Delete image](#delete-image)
  - [Network Operations](#network-operations)
    - [Network Management](#network-management)
- [Create network](#create-network)
- [Create subnet](#create-subnet)
- [List networks](#list-networks)
- [Show network details](#show-network-details)
- [Delete network](#delete-network)
    - [Router Management](#router-management)
- [Create router](#create-router)
- [Add subnet to router](#add-subnet-to-router)
- [Set external gateway](#set-external-gateway)
- [List routers](#list-routers)
- [Show router details](#show-router-details)
- [Remove subnet from router](#remove-subnet-from-router)
  - [Volume Operations](#volume-operations)
    - [Volume Management](#volume-management)
- [Create volume](#create-volume)
- [Attach volume to instance](#attach-volume-to-instance)
- [List volumes](#list-volumes)
- [Show volume details](#show-volume-details)
- [Detach volume](#detach-volume)
- [Delete volume](#delete-volume)
  - [User and Project Management](#user-and-project-management)
    - [User Management](#user-management)
- [Create new user](#create-new-user)
- [List users](#list-users)
- [Update user](#update-user)
- [Delete user](#delete-user)
    - [Project Management](#project-management)
- [Create project](#create-project)
- [List projects](#list-projects)
- [Show project details](#show-project-details)
- [Update project](#update-project)
- [Delete project](#delete-project)
  - [Quota Management](#quota-management)
    - [Set and View Quotas](#set-and-view-quotas)
- [View project quotas](#view-project-quotas)
- [Update compute quotas](#update-compute-quotas)
- [Update volume quotas](#update-volume-quotas)
- [Update network quotas](#update-network-quotas)
  - [Service Management](#service-management)
    - [Service Operations](#service-operations)
- [List services](#list-services)
- [Show service details](#show-service-details)
- [Enable/Disable service](#enable/disable-service)
- [List compute services](#list-compute-services)
- [List network agents](#list-network-agents)
  - [Maintenance Tasks](#maintenance-tasks)
    - [Backup Operations](#backup-operations)
- [Backup databases](#backup-databases)
- [Backup configuration files](#backup-configuration-files)
- [Export instance list](#export-instance-list)
- [Export network configuration](#export-network-configuration)
    - [System Updates](#system-updates)
- [Update OpenStack packages](#update-openstack-packages)
- [Restart services](#restart-services)
  - [Performance Monitoring](#performance-monitoring)
    - [Resource Usage](#resource-usage)
- [Check compute resource usage](#check-compute-resource-usage)
- [Show hypervisor statistics](#show-hypervisor-statistics)
- [List hypervisor usage](#list-hypervisor-usage)
    - [Service Health Checks](#service-health-checks)
- [Check API endpoints](#check-api-endpoints)
- [Verify service status](#verify-service-status)
- [Check compute services](#check-compute-services)
- [Check block storage services](#check-block-storage-services)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
- [Check service logs](#check-service-logs)
- [Check system messages](#check-system-messages)
- [Check database connectivity](#check-database-connectivity)
    - [Network Debugging](#network-debugging)
- [Check network connectivity](#check-network-connectivity)
- [Verify network namespaces](#verify-network-namespaces)
- [Check DHCP status](#check-dhcp-status)
  - [Cleanup Operations](#cleanup-operations)
    - [Resource Cleanup](#resource-cleanup)
- [Delete inactive instances](#delete-inactive-instances)
- [Remove unused volumes](#remove-unused-volumes)
- [Clean up unused images](#clean-up-unused-images)
- [Remove stale security groups](#remove-stale-security-groups)



This guide provides common day-to-day operations and administrative tasks for OpenStack environments.

## Instance Management

### Create and Manage Instances
```bash
# Create new instance
openstack server create \
  --image ubuntu-20.04 \
  --flavor m1.medium \
  --network private-net \
  --security-group default \
  --key-name mykey \
  my-instance

# List instances
openstack server list

# Get instance details
openstack server show my-instance

# Stop instance
openstack server stop my-instance

# Start instance
openstack server start my-instance

# Reboot instance
openstack server reboot --hard my-instance

# Delete instance
openstack server delete my-instance

# Create instance snapshot
openstack server image create --name my-snapshot my-instance
```

### Instance Troubleshooting
```bash
# Get console output
openstack console log show my-instance

# Get VNC console URL
openstack console url show my-instance

# Check instance status
openstack server diagnostics show my-instance

# View instance actions
openstack server event list my-instance
```

## Image Management

### Manage Images
```bash
# Upload new image
openstack image create "ubuntu-20.04" \
  --disk-format qcow2 \
  --container-format bare \
  --file ubuntu-20.04-server-cloudimg-amd64.img \
  --property hw_disk_bus=scsi \
  --property hw_scsi_model=virtio-scsi \
  --property os_type=linux

# List images
openstack image list

# Show image details
openstack image show ubuntu-20.04

# Update image properties
openstack image set \
  --property hw_qemu_guest_agent=yes \
  ubuntu-20.04

# Delete image
openstack image delete ubuntu-20.04
```

## Network Operations

### Network Management
```bash
# Create network
openstack network create internal-net

# Create subnet
openstack subnet create internal-subnet \
  --network internal-net \
  --subnet-range 192.168.1.0/24 \
  --dns-nameserver 8.8.8.8

# List networks
openstack network list

# Show network details
openstack network show internal-net

# Delete network
openstack network delete internal-net
```

### Router Management
```bash
# Create router
openstack router create main-router

# Add subnet to router
openstack router add subnet main-router internal-subnet

# Set external gateway
openstack router set \
  --external-gateway public-net main-router

# List routers
openstack router list

# Show router details
openstack router show main-router

# Remove subnet from router
openstack router remove subnet main-router internal-subnet
```

## Volume Operations

### Volume Management
```bash
# Create volume
openstack volume create \
  --size 100 \
  --type high-performance \
  my-volume

# Attach volume to instance
openstack server add volume \
  my-instance my-volume \
  --device /dev/vdb

# List volumes
openstack volume list

# Show volume details
openstack volume show my-volume

# Detach volume
openstack server remove volume my-instance my-volume

# Delete volume
openstack volume delete my-volume
```

## User and Project Management

### User Management
```bash
# Create new user
openstack user create \
  --password-prompt \
  --email user@example.com \
  newuser

# List users
openstack user list

# Update user
openstack user set \
  --email new.email@example.com \
  newuser

# Delete user
openstack user delete newuser
```

### Project Management
```bash
# Create project
openstack project create \
  --description "Development Team Project" \
  devteam

# List projects
openstack project list

# Show project details
openstack project show devteam

# Update project
openstack project set \
  --description "New Description" \
  devteam

# Delete project
openstack project delete devteam
```

## Quota Management

### Set and View Quotas
```bash
# View project quotas
openstack quota show devteam

# Update compute quotas
openstack quota set \
  --instances 20 \
  --cores 40 \
  --ram 51200 \
  devteam

# Update volume quotas
openstack quota set \
  --volumes 20 \
  --gigabytes 1000 \
  --volume-type high-performance=500 \
  devteam

# Update network quotas
openstack quota set \
  --networks 10 \
  --subnets 20 \
  --ports 100 \
  devteam
```

## Service Management

### Service Operations
```bash
# List services
openstack service list

# Show service details
openstack service show compute

# Enable/Disable service
openstack compute service set \
  --enable/--disable \
  host1 nova-compute

# List compute services
openstack compute service list

# List network agents
openstack network agent list
```

## Maintenance Tasks

### Backup Operations
```bash
# Backup databases
mysqldump --opt --all-databases > openstack_db_backup.sql

# Backup configuration files
tar -czf openstack_config_backup.tar.gz /etc/nova /etc/neutron /etc/keystone /etc/cinder

# Export instance list
openstack server list -f json > instances_backup.json

# Export network configuration
openstack network list -f json > networks_backup.json
```

### System Updates
```bash
# Update OpenStack packages
apt update
apt list --upgradable | grep openstack
apt upgrade -y

# Restart services
systemctl restart nova-api nova-scheduler nova-conductor
systemctl restart neutron-server neutron-l3-agent
systemctl restart cinder-api cinder-scheduler
```

## Performance Monitoring

### Resource Usage
```bash
# Check compute resource usage
openstack usage list --start $(date -d "yesterday" +%Y-%m-%d) \
  --end $(date +%Y-%m-%d)

# Show hypervisor statistics
openstack hypervisor stats show

# List hypervisor usage
openstack hypervisor list --long
```

### Service Health Checks
```bash
# Check API endpoints
openstack endpoint list

# Verify service status
openstack service list --long

# Check compute services
openstack compute service list

# Check block storage services
openstack volume service list
```

## Troubleshooting

### Common Issues
```bash
# Check service logs
tail -f /var/log/nova/nova-api.log
tail -f /var/log/neutron/neutron-server.log
tail -f /var/log/cinder/cinder-api.log

# Check system messages
journalctl -u nova-api
journalctl -u neutron-server
journalctl -u cinder-api

# Check database connectivity
mysql -u root -p -e "show databases;"
mysql -u root -p -e "select * from nova.services where disabled=1;"
```

### Network Debugging
```bash
# Check network connectivity
ping instance_ip

# Verify network namespaces
ip netns list
ip netns exec qrouter-xxx ip a

# Check DHCP status
ip netns exec qdhcp-xxx ip a
```

## Cleanup Operations

### Resource Cleanup
```bash
# Delete inactive instances
openstack server list --status ERROR -f value -c ID | \
  xargs -n1 openstack server delete

# Remove unused volumes
openstack volume list --status error -f value -c ID | \
  xargs -n1 openstack volume delete

# Clean up unused images
openstack image list --status deactivated -f value -c ID | \
  xargs -n1 openstack image delete

# Remove stale security groups
openstack security group list --project unused-project -f value -c ID | \
  xargs -n1 openstack security group delete
```

For more detailed information about specific operations, refer to the [official OpenStack Operations Guide](https://docs.openstack.org/operations-guide/).
