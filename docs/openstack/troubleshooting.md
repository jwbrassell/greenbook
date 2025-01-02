# OpenStack Troubleshooting Guide (Version 17.1)

## Table of Contents
- [OpenStack Troubleshooting Guide (Version 17.1)](#openstack-troubleshooting-guide-version-171)
  - [General Troubleshooting Methodology](#general-troubleshooting-methodology)
  - [Service Issues](#service-issues)
    - [Nova (Compute) Issues](#nova-compute-issues)
      - [Instance Launch Failures](#instance-launch-failures)
- [Check nova service status](#check-nova-service-status)
- [Verify compute node resources](#verify-compute-node-resources)
- [Check nova logs](#check-nova-logs)
- [Common solutions:](#common-solutions:)
- [1. Restart nova services](#1-restart-nova-services)
- [2. Verify nova-compute configuration](#2-verify-nova-compute-configuration)
- [3. Check instance quota](#3-check-instance-quota)
      - [Instance Stuck in Status](#instance-stuck-in-status)
- [Get instance details](#get-instance-details)
- [Check instance status](#check-instance-status)
- [Force instance state](#force-instance-state)
- [Reset instance state](#reset-instance-state)
- [Delete stuck instance](#delete-stuck-instance)
    - [Neutron (Network) Issues](#neutron-network-issues)
      - [Network Connectivity Problems](#network-connectivity-problems)
- [Check neutron service status](#check-neutron-service-status)
- [Verify network namespaces](#verify-network-namespaces)
- [Check neutron logs](#check-neutron-logs)
- [Common solutions:](#common-solutions:)
- [1. Restart neutron services](#1-restart-neutron-services)
- [2. Recreate network resources](#2-recreate-network-resources)
      - [DHCP Issues](#dhcp-issues)
- [Check DHCP agent status](#check-dhcp-agent-status)
- [Verify DHCP namespace](#verify-dhcp-namespace)
- [Check DHCP leases](#check-dhcp-leases)
- [Common solutions:](#common-solutions:)
- [1. Restart DHCP agent](#1-restart-dhcp-agent)
- [2. Recreate port](#2-recreate-port)
    - [Keystone (Identity) Issues](#keystone-identity-issues)
      - [Authentication Failures](#authentication-failures)
- [Check keystone logs](#check-keystone-logs)
- [Verify endpoint list](#verify-endpoint-list)
- [Test authentication](#test-authentication)
- [Common solutions:](#common-solutions:)
- [1. Verify credentials](#1-verify-credentials)
- [2. Check keystone configuration](#2-check-keystone-configuration)
- [3. Restart keystone](#3-restart-keystone)
    - [Cinder (Block Storage) Issues](#cinder-block-storage-issues)
      - [Volume Creation Failures](#volume-creation-failures)
- [Check cinder services](#check-cinder-services)
- [Verify backend status](#verify-backend-status)
- [Check cinder logs](#check-cinder-logs)
- [Common solutions:](#common-solutions:)
- [1. Restart cinder services](#1-restart-cinder-services)
- [2. Check storage backend](#2-check-storage-backend)
  - [Performance Issues](#performance-issues)
    - [High CPU Usage](#high-cpu-usage)
- [Check system CPU usage](#check-system-cpu-usage)
- [Monitor OpenStack processes](#monitor-openstack-processes)
- [Check for runaway processes](#check-for-runaway-processes)
- [Solutions:](#solutions:)
- [1. Adjust worker processes](#1-adjust-worker-processes)
- [2. Enable caching](#2-enable-caching)
    - [Memory Issues](#memory-issues)
- [Check memory usage](#check-memory-usage)
- [Monitor memory-intensive processes](#monitor-memory-intensive-processes)
- [Check for memory leaks](#check-for-memory-leaks)
- [Solutions:](#solutions:)
- [1. Adjust service memory limits](#1-adjust-service-memory-limits)
- [2. Clear system cache](#2-clear-system-cache)
  - [Database Issues](#database-issues)
    - [MySQL/MariaDB Problems](#mysql/mariadb-problems)
- [Check database status](#check-database-status)
- [Verify connections](#verify-connections)
- [Check table status](#check-table-status)
- [Common solutions:](#common-solutions:)
- [1. Repair databases](#1-repair-databases)
- [2. Optimize tables](#2-optimize-tables)
  - [API Issues](#api-issues)
    - [API Endpoint Problems](#api-endpoint-problems)
- [Test API endpoints](#test-api-endpoints)
- [Check API logs](#check-api-logs)
- [Solutions:](#solutions:)
- [1. Verify endpoint configuration](#1-verify-endpoint-configuration)
- [2. Restart API services](#2-restart-api-services)
  - [Resource Issues](#resource-issues)
    - [Out of Resources](#out-of-resources)
- [Check resource usage](#check-resource-usage)
- [Verify project quotas](#verify-project-quotas)
- [Monitor disk usage](#monitor-disk-usage)
- [Solutions:](#solutions:)
- [1. Adjust quotas](#1-adjust-quotas)
- [2. Clean up resources](#2-clean-up-resources)
  - [Network Debugging](#network-debugging)
    - [Advanced Network Troubleshooting](#advanced-network-troubleshooting)
- [Packet capture](#packet-capture)
- [Check network flows](#check-network-flows)
- [Trace network path](#trace-network-path)
- [Solutions:](#solutions:)
- [1. Reset network components](#1-reset-network-components)
- [2. Rebuild network](#2-rebuild-network)
  - [Recovery Procedures](#recovery-procedures)
    - [Service Recovery](#service-recovery)
- [Backup current state](#backup-current-state)
- [Reset services](#reset-services)
- [Verify recovery](#verify-recovery)
    - [Database Recovery](#database-recovery)
- [Backup database](#backup-database)
- [Stop services](#stop-services)
- [Repair database](#repair-database)
- [Sync database](#sync-database)



This guide provides solutions for common issues, debugging procedures, and troubleshooting methodologies for OpenStack deployments.

## General Troubleshooting Methodology

1. **Identify the Problem**
   - Check service status
   - Review error messages
   - Examine logs
   - Verify connectivity

2. **Gather Information**
   - Service logs
   - System logs
   - API responses
   - Resource states

3. **Analyze**
   - Compare with working state
   - Check recent changes
   - Verify configurations
   - Test connectivity

4. **Resolve**
   - Apply fix
   - Test solution
   - Document resolution
   - Update documentation

## Service Issues

### Nova (Compute) Issues

#### Instance Launch Failures
```bash
# Check nova service status
openstack compute service list
systemctl status nova-*

# Verify compute node resources
openstack hypervisor show compute1

# Check nova logs
tail -f /var/log/nova/nova-compute.log
tail -f /var/log/nova/nova-api.log

# Common solutions:
# 1. Restart nova services
systemctl restart nova-compute nova-api nova-scheduler

# 2. Verify nova-compute configuration
grep -r "^[^#;]" /etc/nova/nova.conf

# 3. Check instance quota
openstack quota show --compute current-project
```

#### Instance Stuck in Status
```bash
# Get instance details
openstack server show instance-id

# Check instance status
openstack server list --long

# Force instance state
openstack server set --state active instance-id

# Reset instance state
nova reset-state --active instance-id

# Delete stuck instance
openstack server delete --force instance-id
```

### Neutron (Network) Issues

#### Network Connectivity Problems
```bash
# Check neutron service status
openstack network agent list
systemctl status neutron-*

# Verify network namespaces
ip netns list
ip netns exec qrouter-xxx ip a

# Check neutron logs
tail -f /var/log/neutron/neutron-server.log
tail -f /var/log/neutron/neutron-l3-agent.log

# Common solutions:
# 1. Restart neutron services
systemctl restart neutron-server neutron-l3-agent neutron-dhcp-agent

# 2. Recreate network resources
openstack router remove subnet router1 subnet1
openstack router add subnet router1 subnet1
```

#### DHCP Issues
```bash
# Check DHCP agent status
openstack network agent list | grep DHCP

# Verify DHCP namespace
ip netns exec qdhcp-xxx ip a

# Check DHCP leases
ip netns exec qdhcp-xxx cat /var/lib/neutron/dhcp/*

# Common solutions:
# 1. Restart DHCP agent
systemctl restart neutron-dhcp-agent

# 2. Recreate port
openstack port delete problem-port
openstack port create --network network1 new-port
```

### Keystone (Identity) Issues

#### Authentication Failures
```bash
# Check keystone logs
tail -f /var/log/keystone/keystone.log

# Verify endpoint list
openstack endpoint list

# Test authentication
openstack token issue

# Common solutions:
# 1. Verify credentials
env | grep OS_

# 2. Check keystone configuration
cat /etc/keystone/keystone.conf | grep -v '^#'

# 3. Restart keystone
systemctl restart apache2
```

### Cinder (Block Storage) Issues

#### Volume Creation Failures
```bash
# Check cinder services
openstack volume service list

# Verify backend status
cinder get-pools

# Check cinder logs
tail -f /var/log/cinder/cinder-volume.log

# Common solutions:
# 1. Restart cinder services
systemctl restart cinder-volume cinder-scheduler

# 2. Check storage backend
lvs  # For LVM backend
```

## Performance Issues

### High CPU Usage
```bash
# Check system CPU usage
top -c

# Monitor OpenStack processes
ps aux | grep -E 'nova|neutron|cinder'

# Check for runaway processes
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head

# Solutions:
# 1. Adjust worker processes
sed -i 's/^workers=.*/workers=4/' /etc/nova/nova.conf

# 2. Enable caching
memcached-tool localhost stats
```

### Memory Issues
```bash
# Check memory usage
free -m
vmstat 1 10

# Monitor memory-intensive processes
ps -eo pid,ppid,cmd,%mem --sort=-%mem | head

# Check for memory leaks
dmesg | grep -i 'out of memory'

# Solutions:
# 1. Adjust service memory limits
systemctl set-property nova-api.service MemoryLimit=2G

# 2. Clear system cache
echo 3 > /proc/sys/vm/drop_caches
```

## Database Issues

### MySQL/MariaDB Problems
```bash
# Check database status
mysql -u root -p -e "SHOW STATUS;"

# Verify connections
mysql -u root -p -e "SHOW PROCESSLIST;"

# Check table status
mysqlcheck -u root -p --all-databases

# Common solutions:
# 1. Repair databases
mysqlcheck -u root -p --auto-repair --all-databases

# 2. Optimize tables
mysqlcheck -u root -p --optimize --all-databases
```

## API Issues

### API Endpoint Problems
```bash
# Test API endpoints
curl -i http://controller:5000/v3
curl -i http://controller:8774/v2.1

# Check API logs
tail -f /var/log/apache2/keystone.log
tail -f /var/log/nova/nova-api.log

# Solutions:
# 1. Verify endpoint configuration
openstack endpoint list --service keystone

# 2. Restart API services
systemctl restart apache2
systemctl restart nova-api
```

## Resource Issues

### Out of Resources
```bash
# Check resource usage
openstack hypervisor stats show

# Verify project quotas
openstack quota show current-project

# Monitor disk usage
df -h
lvs

# Solutions:
# 1. Adjust quotas
openstack quota set --cores 32 --instances 20 project-name

# 2. Clean up resources
openstack server list --status ERROR -f value -c ID | xargs -n1 openstack server delete
```

## Network Debugging

### Advanced Network Troubleshooting
```bash
# Packet capture
tcpdump -i any -n port 5672  # RabbitMQ
tcpdump -i any -n port 3306  # MySQL

# Check network flows
ovs-ofctl dump-flows br-int

# Trace network path
traceroute instance-ip

# Solutions:
# 1. Reset network components
neutron-ovs-cleanup
service openvswitch-switch restart

# 2. Rebuild network
neutron-netns-cleanup
```

## Recovery Procedures

### Service Recovery
```bash
# Backup current state
mysqldump --opt --all-databases > backup.sql
tar -czf /root/config-backup.tar.gz /etc/nova /etc/neutron /etc/keystone

# Reset services
systemctl stop nova-* neutron-* cinder-*
systemctl start nova-* neutron-* cinder-*

# Verify recovery
openstack service list --long
```

### Database Recovery
```bash
# Backup database
mysqldump --opt --all-databases > backup.sql

# Stop services
systemctl stop nova-* neutron-* cinder-*

# Repair database
mysqlcheck -u root -p --auto-repair --all-databases

# Sync database
nova-manage db sync
neutron-db-manage upgrade heads
```

For more detailed troubleshooting information, refer to:
- [OpenStack Operations Guide](https://docs.openstack.org/operations-guide/)
- [OpenStack Security Guide](https://docs.openstack.org/security-guide/)
- [OpenStack Administrator Guide](https://docs.openstack.org/admin-guide/)
