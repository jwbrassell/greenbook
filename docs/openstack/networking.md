# OpenStack Networking Guide (Version 17.1)

## Table of Contents
- [OpenStack Networking Guide (Version 17.1)](#openstack-networking-guide-version-171)
  - [Network Architecture](#network-architecture)
  - [Basic Network Setup](#basic-network-setup)
    - [Create Provider Network](#create-provider-network)
- [Create provider network](#create-provider-network)
- [Create subnet for provider network](#create-subnet-for-provider-network)
    - [Create Self-Service Network](#create-self-service-network)
- [Create private network](#create-private-network)
- [Create subnet for private network](#create-subnet-for-private-network)
- [Create router](#create-router)
- [Add private subnet to router](#add-private-subnet-to-router)
- [Set router gateway to provider network](#set-router-gateway-to-provider-network)
  - [Security Groups](#security-groups)
    - [Default Security Group Rules](#default-security-group-rules)
- [Create security group](#create-security-group)
- [Allow SSH access](#allow-ssh-access)
- [Allow HTTP access](#allow-http-access)
- [Allow HTTPS access](#allow-https-access)
- [Allow ICMP (ping)](#allow-icmp-ping)
    - [Managing Security Groups](#managing-security-groups)
- [List security groups](#list-security-groups)
- [Show security group details](#show-security-group-details)
- [List security group rules](#list-security-group-rules)
- [Delete security group rule](#delete-security-group-rule)
- [Delete security group](#delete-security-group)
  - [Network Ports](#network-ports)
    - [Port Management](#port-management)
- [List ports](#list-ports)
- [Create port](#create-port)
- [Show port details](#show-port-details)
- [Delete port](#delete-port)
- [Update port](#update-port)
  - [Floating IPs](#floating-ips)
    - [Managing Floating IPs](#managing-floating-ips)
- [Create floating IP](#create-floating-ip)
- [List floating IPs](#list-floating-ips)
- [Associate floating IP with instance](#associate-floating-ip-with-instance)
- [Disassociate floating IP](#disassociate-floating-ip)
- [Delete floating IP](#delete-floating-ip)
  - [Load Balancer (Octavia)](#load-balancer-octavia)
    - [Basic Load Balancer Setup](#basic-load-balancer-setup)
- [Create load balancer](#create-load-balancer)
- [Create listener](#create-listener)
- [Create pool](#create-pool)
- [Add members to pool](#add-members-to-pool)
- [Create health monitor](#create-health-monitor)
  - [Network Troubleshooting](#network-troubleshooting)
    - [Connectivity Tests](#connectivity-tests)
- [Check network connectivity](#check-network-connectivity)
- [Check port status](#check-port-status)
- [Verify network namespace](#verify-network-namespace)
- [Check router status](#check-router-status)
    - [Common Issues and Solutions](#common-issues-and-solutions)
- [Check neutron agent status](#check-neutron-agent-status)
- [Restart neutron agents](#restart-neutron-agents)
- [Check DHCP agent status](#check-dhcp-agent-status)
- [Verify DHCP namespace](#verify-dhcp-namespace)
- [Restart DHCP agent](#restart-dhcp-agent)
- [Verify router status](#verify-router-status)
- [Check router namespace](#check-router-namespace)
- [Verify security group rules](#verify-security-group-rules)
  - [Advanced Configurations](#advanced-configurations)
    - [ML2 Plugin Configuration](#ml2-plugin-configuration)
- [/etc/neutron/plugins/ml2/ml2_conf.ini](#/etc/neutron/plugins/ml2/ml2_confini)
    - [Linux Bridge Agent Configuration](#linux-bridge-agent-configuration)
- [/etc/neutron/plugins/ml2/linuxbridge_agent.ini](#/etc/neutron/plugins/ml2/linuxbridge_agentini)
  - [Network Monitoring](#network-monitoring)
    - [Network Statistics](#network-statistics)
- [Get network statistics](#get-network-statistics)
- [Monitor network traffic](#monitor-network-traffic)
    - [Log Analysis](#log-analysis)
- [View neutron logs](#view-neutron-logs)
- [Search for specific errors](#search-for-specific-errors)
  - [Network Maintenance](#network-maintenance)
    - [Cleanup Operations](#cleanup-operations)
- [Delete unused floating IPs](#delete-unused-floating-ips)
- [Delete unused ports](#delete-unused-ports)
- [Clean up defunct network namespaces](#clean-up-defunct-network-namespaces)
    - [Backup Network Configuration](#backup-network-configuration)
- [Backup neutron database](#backup-neutron-database)
- [Backup configuration files](#backup-configuration-files)
- [Export network information](#export-network-information)



This guide covers networking configurations, security groups, and common networking operations in OpenStack.

## Network Architecture

OpenStack networking (Neutron) supports two main network types:

1. **Provider Networks**
   - Direct connection to physical network
   - VLAN or flat network configurations
   - Typically used in production environments

2. **Self-Service Networks**
   - Virtual networks using overlay protocols
   - Tenant isolation using VXLAN/GRE
   - Software-defined networking features

## Basic Network Setup

### Create Provider Network
```bash
# Create provider network
openstack network create --share --external \
  --provider-physical-network provider \
  --provider-network-type flat provider

# Create subnet for provider network
openstack subnet create --network provider \
  --allocation-pool start=203.0.113.101,end=203.0.113.250 \
  --dns-nameserver 8.8.8.8 --gateway 203.0.113.1 \
  --subnet-range 203.0.113.0/24 provider-subnet
```

### Create Self-Service Network
```bash
# Create private network
openstack network create private-net

# Create subnet for private network
openstack subnet create private-subnet \
  --network private-net \
  --subnet-range 192.168.1.0/24 \
  --dns-nameserver 8.8.8.8

# Create router
openstack router create router1

# Add private subnet to router
openstack router add subnet router1 private-subnet

# Set router gateway to provider network
openstack router set router1 --external-gateway provider
```

## Security Groups

### Default Security Group Rules
```bash
# Create security group
openstack security group create webserver

# Allow SSH access
openstack security group rule create --protocol tcp \
  --dst-port 22:22 --remote-ip 0.0.0.0/0 webserver

# Allow HTTP access
openstack security group rule create --protocol tcp \
  --dst-port 80:80 --remote-ip 0.0.0.0/0 webserver

# Allow HTTPS access
openstack security group rule create --protocol tcp \
  --dst-port 443:443 --remote-ip 0.0.0.0/0 webserver

# Allow ICMP (ping)
openstack security group rule create --protocol icmp webserver
```

### Managing Security Groups
```bash
# List security groups
openstack security group list

# Show security group details
openstack security group show webserver

# List security group rules
openstack security group rule list webserver

# Delete security group rule
openstack security group rule delete RULE_ID

# Delete security group
openstack security group delete webserver
```

## Network Ports

### Port Management
```bash
# List ports
openstack port list

# Create port
openstack port create --network private-net \
  --fixed-ip subnet=private-subnet,ip-address=192.168.1.20 \
  my-port

# Show port details
openstack port show my-port

# Delete port
openstack port delete my-port

# Update port
openstack port set --disable-port-security my-port
```

## Floating IPs

### Managing Floating IPs
```bash
# Create floating IP
openstack floating ip create provider

# List floating IPs
openstack floating ip list

# Associate floating IP with instance
openstack server add floating ip my-instance FLOATING_IP

# Disassociate floating IP
openstack server remove floating ip my-instance FLOATING_IP

# Delete floating IP
openstack floating ip delete FLOATING_IP
```

## Load Balancer (Octavia)

### Basic Load Balancer Setup
```bash
# Create load balancer
openstack loadbalancer create --name lb1 --vip-subnet-id private-subnet

# Create listener
openstack loadbalancer listener create --name listener1 \
  --protocol HTTP --protocol-port 80 lb1

# Create pool
openstack loadbalancer pool create --name pool1 \
  --lb-algorithm ROUND_ROBIN --listener listener1 \
  --protocol HTTP

# Add members to pool
openstack loadbalancer member create --subnet-id private-subnet \
  --address 192.168.1.10 --protocol-port 80 pool1

# Create health monitor
openstack loadbalancer healthmonitor create --delay 5 \
  --max-retries 3 --timeout 5 --type HTTP --url-path /health pool1
```

## Network Troubleshooting

### Connectivity Tests
```bash
# Check network connectivity
ping INSTANCE_IP

# Check port status
openstack port show PORT_ID

# Verify network namespace
ip netns list
ip netns exec qrouter-ROUTER_ID ping INSTANCE_IP

# Check router status
openstack router show router1
```

### Common Issues and Solutions

1. **No Network Connectivity**
```bash
# Check neutron agent status
openstack network agent list

# Restart neutron agents
sudo systemctl restart neutron-linuxbridge-agent
sudo systemctl restart neutron-l3-agent
sudo systemctl restart neutron-dhcp-agent
```

2. **DHCP Issues**
```bash
# Check DHCP agent status
openstack network agent list | grep DHCP

# Verify DHCP namespace
ip netns exec qdhcp-NETWORK_ID ip a

# Restart DHCP agent
sudo systemctl restart neutron-dhcp-agent
```

3. **Floating IP Not Working**
```bash
# Verify router status
openstack router show router1

# Check router namespace
ip netns exec qrouter-ROUTER_ID ip a

# Verify security group rules
openstack security group rule list SECURITY_GROUP_ID
```

## Advanced Configurations

### ML2 Plugin Configuration
```ini
# /etc/neutron/plugins/ml2/ml2_conf.ini
[ml2]
type_drivers = flat,vlan,vxlan
tenant_network_types = vxlan
mechanism_drivers = linuxbridge,l2population
extension_drivers = port_security

[ml2_type_flat]
flat_networks = provider

[ml2_type_vxlan]
vni_ranges = 1:1000

[securitygroup]
enable_security_group = true
enable_ipset = true
```

### Linux Bridge Agent Configuration
```ini
# /etc/neutron/plugins/ml2/linuxbridge_agent.ini
[linux_bridge]
physical_interface_mappings = provider:PROVIDER_INTERFACE_NAME

[vxlan]
enable_vxlan = true
local_ip = OVERLAY_INTERFACE_IP
l2_population = true

[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```

## Network Monitoring

### Network Statistics
```bash
# Get network statistics
openstack network agent list
openstack network list --long
openstack router list --long

# Monitor network traffic
sudo tcpdump -i any -n port 4789  # VXLAN traffic
sudo tcpdump -i any -n port 5671  # AMQP traffic
```

### Log Analysis
```bash
# View neutron logs
sudo tail -f /var/log/neutron/neutron-server.log
sudo tail -f /var/log/neutron/neutron-linuxbridge-agent.log
sudo tail -f /var/log/neutron/neutron-l3-agent.log
sudo tail -f /var/log/neutron/neutron-dhcp-agent.log

# Search for specific errors
sudo grep ERROR /var/log/neutron/neutron-server.log
```

## Network Maintenance

### Cleanup Operations
```bash
# Delete unused floating IPs
openstack floating ip list --status DOWN -f value -c ID | xargs -n1 openstack floating ip delete

# Delete unused ports
openstack port list --status DOWN -f value -c ID | xargs -n1 openstack port delete

# Clean up defunct network namespaces
for ns in $(ip netns list | grep -v id); do
  ip netns delete $ns
done
```

### Backup Network Configuration
```bash
# Backup neutron database
mysqldump --databases neutron > neutron_backup.sql

# Backup configuration files
sudo tar -czf neutron_config_backup.tar.gz /etc/neutron/

# Export network information
openstack network list -f json > networks_backup.json
openstack router list -f json > routers_backup.json
openstack security group list -f json > security_groups_backup.json
```

For more detailed information about networking features and configurations, refer to the [official OpenStack Networking Guide](https://docs.openstack.org/neutron/latest/).
