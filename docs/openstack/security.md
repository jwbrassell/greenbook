# OpenStack Security Best Practices (Version 17.1)

## Table of Contents
- [OpenStack Security Best Practices (Version 17.1)](#openstack-security-best-practices-version-171)
  - [Identity and Access Management (Keystone)](#identity-and-access-management-keystone)
    - [Password Policies](#password-policies)
- [/etc/keystone/keystone.conf](#/etc/keystone/keystoneconf)
    - [Token Configuration](#token-configuration)
    - [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
- [Create custom role](#create-custom-role)
- [Create security policy](#create-security-policy)
- [Create project for security team](#create-project-for-security-team)
- [Assign role to user](#assign-role-to-user)
  - [Network Security](#network-security)
    - [Security Groups](#security-groups)
- [Create restrictive default security group](#create-restrictive-default-security-group)
- [Allow only necessary ports](#allow-only-necessary-ports)
    - [Network Isolation](#network-isolation)
- [Create isolated network](#create-isolated-network)
- [Configure no-floating-ip policy](#configure-no-floating-ip-policy)
- [Create subnet without public DNS](#create-subnet-without-public-dns)
    - [SSL/TLS Configuration](#ssl/tls-configuration)
- [/etc/nova/nova.conf](#/etc/nova/novaconf)
- [/etc/neutron/neutron.conf](#/etc/neutron/neutronconf)
  - [Storage Security](#storage-security)
    - [Volume Encryption](#volume-encryption)
- [Create encrypted volume type](#create-encrypted-volume-type)
- [Enable encryption](#enable-encryption)
- [Create encrypted volume](#create-encrypted-volume)
    - [Object Storage Security](#object-storage-security)
- [/etc/swift/proxy-server.conf](#/etc/swift/proxy-serverconf)
- [Enable at-rest encryption](#enable-at-rest-encryption)
  - [Compute Security](#compute-security)
    - [Hypervisor Security](#hypervisor-security)
- [/etc/nova/nova.conf](#/etc/nova/novaconf)
- [Enable secure boot](#enable-secure-boot)
    - [Instance Security](#instance-security)
- [Create secure flavor](#create-secure-flavor)
- [Enable instance security monitoring](#enable-instance-security-monitoring)
  - [Logging and Monitoring](#logging-and-monitoring)
    - [Centralized Logging](#centralized-logging)
- [/etc/rsyslog.d/openstack.conf](#/etc/rsyslogd/openstackconf)
- [Enable detailed logging](#enable-detailed-logging)
    - [Security Monitoring](#security-monitoring)
- [Configure security monitoring](#configure-security-monitoring)
  - [Compliance and Auditing](#compliance-and-auditing)
    - [Audit Configuration](#audit-configuration)
- [/etc/keystone/keystone.conf](#/etc/keystone/keystoneconf)
- [Enable API request logging](#enable-api-request-logging)
    - [Compliance Checks](#compliance-checks)
- [Run security compliance check](#run-security-compliance-check)
- [Generate compliance report](#generate-compliance-report)
- [Verify service endpoints](#verify-service-endpoints)
  - [Firewall Configuration](#firewall-configuration)
    - [Host-based Firewall](#host-based-firewall)
- [Configure iptables rules](#configure-iptables-rules)
- [Allow established connections](#allow-established-connections)
- [Allow SSH from management network](#allow-ssh-from-management-network)
- [OpenStack API ports](#openstack-api-ports)
  - [Security Hardening Checklist](#security-hardening-checklist)
  - [Regular Security Tasks](#regular-security-tasks)
    - [Daily Tasks](#daily-tasks)
- [Check failed authentication attempts](#check-failed-authentication-attempts)
- [Monitor security group changes](#monitor-security-group-changes)
- [Check service status](#check-service-status)
    - [Weekly Tasks](#weekly-tasks)
- [Rotate encryption keys](#rotate-encryption-keys)
- [Review security group rules](#review-security-group-rules)
- [Audit user access](#audit-user-access)
    - [Monthly Tasks](#monthly-tasks)
- [Review and update security policies](#review-and-update-security-policies)
- [Check for inactive users](#check-for-inactive-users)
- [Update security patches](#update-security-patches)
  - [Incident Response](#incident-response)
    - [Security Incident Procedures](#security-incident-procedures)
- [Isolate compromised instance](#isolate-compromised-instance)
- [Capture forensics](#capture-forensics)
- [Create evidence snapshot](#create-evidence-snapshot)



This guide covers security best practices, configurations, and recommendations for securing OpenStack deployments.

## Identity and Access Management (Keystone)

### Password Policies
```ini
# /etc/keystone/keystone.conf
[security_compliance]
lockout_duration = 1800
lockout_failure_attempts = 5
password_expires_days = 90
password_regex = ^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()<>{}+=_\\\[\]\-?|~`,.;:]).{8,}$
password_regex_description = Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, 1 special character, and be at least 8 characters long
unique_last_password_count = 5
```

### Token Configuration
```ini
[token]
provider = fernet
expiration = 3600
allow_expired_window = 172800
```

### Role-Based Access Control (RBAC)
```bash
# Create custom role
openstack role create security-admin

# Create security policy
cat > security-policy.yaml << EOF
"identity:list_users": "role:security-admin"
"identity:get_user": "role:security-admin"
"identity:update_user": "role:security-admin"
"identity:delete_user": "role:security-admin"
EOF

# Create project for security team
openstack project create --domain default \
  --description "Security Operations" secops

# Assign role to user
openstack role add --project secops --user security-admin security-admin
```

## Network Security

### Security Groups
```bash
# Create restrictive default security group
openstack security group create restricted-default

# Allow only necessary ports
openstack security group rule create --protocol tcp \
  --dst-port 22:22 --remote-ip ADMIN_NETWORK_CIDR restricted-default

openstack security group rule create --protocol tcp \
  --dst-port 443:443 --remote-ip ADMIN_NETWORK_CIDR restricted-default
```

### Network Isolation
```bash
# Create isolated network
openstack network create --internal isolated-net

# Configure no-floating-ip policy
openstack network set --no-share isolated-net

# Create subnet without public DNS
openstack subnet create isolated-subnet \
  --network isolated-net \
  --subnet-range 192.168.100.0/24 \
  --no-dns-nameservers
```

### SSL/TLS Configuration
```ini
# /etc/nova/nova.conf
[DEFAULT]
ssl_only = true
ssl_cert_file = /etc/nova/ssl/nova.cert
ssl_key_file = /etc/nova/ssl/nova.key
ssl_ca_file = /etc/nova/ssl/ca.cert

# /etc/neutron/neutron.conf
[DEFAULT]
use_ssl = true
ssl_cert_file = /etc/neutron/ssl/neutron.cert
ssl_key_file = /etc/neutron/ssl/neutron.key
ssl_ca_file = /etc/neutron/ssl/ca.cert
```

## Storage Security

### Volume Encryption
```bash
# Create encrypted volume type
openstack volume type create encrypted

# Enable encryption
openstack volume type set --encryption-provider luks \
  --encryption-cipher aes-xts-plain64 \
  --encryption-key-size 256 \
  --encryption-control-location front-end encrypted

# Create encrypted volume
openstack volume create --type encrypted --size 10 secure-volume
```

### Object Storage Security
```ini
# /etc/swift/proxy-server.conf
[filter:encryption]
use = egg:swift#encryption
disable_encryption = False
encryption_key_id = your_key_id
encryption_root_secret = your_root_secret

# Enable at-rest encryption
[filter:encryption]
use = egg:swift#encryption
encryption_algorithm = AES256
```

## Compute Security

### Hypervisor Security
```ini
# /etc/nova/nova.conf
[libvirt]
virt_type = kvm
cpu_mode = host-passthrough
hw_machine_type = x86_64=q35
sysinfo_serial = unique

# Enable secure boot
[libvirt]
enable_secure_boot = True
secure_boot_certificates = "UEFI"
```

### Instance Security
```bash
# Create secure flavor
openstack flavor create --ram 4096 --disk 40 --vcpus 2 \
  --property hw:mem_page_size=2048 \
  --property hw:cpu_policy=dedicated \
  --property hw:cpu_thread_policy=isolate \
  secure.medium

# Enable instance security monitoring
openstack server set --property security_monitoring=true my-instance
```

## Logging and Monitoring

### Centralized Logging
```ini
# /etc/rsyslog.d/openstack.conf
*.* @@log-server:514

# Enable detailed logging
local0.* /var/log/openstack/audit.log
```

### Security Monitoring
```bash
# Configure security monitoring
cat > /etc/ossec-hids/ossec.conf << EOF
<ossec_config>
  <syscheck>
    <directories check_all="yes">/etc/nova,/etc/neutron,/etc/keystone</directories>
    <ignore>/etc/nova/nova.conf.d</ignore>
  </syscheck>
  
  <rootcheck>
    <system_audit>/var/ossec/etc/shared/system_audit_rcl.txt</system_audit>
  </rootcheck>
</ossec_config>
EOF
```

## Compliance and Auditing

### Audit Configuration
```ini
# /etc/keystone/keystone.conf
[audit]
enabled = True
audit_map_file = /etc/keystone/keystone_audit_map.conf
namespace = openstack

# Enable API request logging
[audit_middleware_notifications]
driver = messagingv2
topics = notifications
transport_url = rabbit://openstack:RABBIT_PASS@controller
```

### Compliance Checks
```bash
# Run security compliance check
openstack security compliance check

# Generate compliance report
openstack security compliance report --format json > compliance_report.json

# Verify service endpoints
openstack endpoint list --service keystone
```

## Firewall Configuration

### Host-based Firewall
```bash
# Configure iptables rules
cat > /etc/iptables/rules.v4 << EOF
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]

# Allow established connections
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH from management network
-A INPUT -p tcp -s MANAGEMENT_NETWORK --dport 22 -j ACCEPT

# OpenStack API ports
-A INPUT -p tcp --dport 5000 -j ACCEPT # Keystone
-A INPUT -p tcp --dport 8774 -j ACCEPT # Nova
-A INPUT -p tcp --dport 9696 -j ACCEPT # Neutron
-A INPUT -p tcp --dport 9292 -j ACCEPT # Glance

COMMIT
EOF
```

## Security Hardening Checklist

1. **System Hardening**
   ```bash
   # Disable unnecessary services
   systemctl disable bluetooth.service
   systemctl disable cups.service
   
   # Set secure permissions
   chmod 600 /etc/keystone/keystone.conf
   chmod 600 /etc/nova/nova.conf
   chmod 600 /etc/neutron/neutron.conf
   ```

2. **Service Security**
   ```bash
   # Enable TLS for all services
   openstack endpoint list --interface public -f value -c URL | \
     grep "http://" && echo "Warning: Non-HTTPS endpoints found"
   
   # Rotate Fernet keys
   keystone-manage fernet_rotate
   ```

3. **Database Security**
   ```bash
   # Secure MySQL configuration
   cat >> /etc/mysql/conf.d/security.cnf << EOF
   [mysqld]
   local-infile=0
   skip-symbolic-links
   secure-file-priv=/var/lib/mysql-files
   EOF
   ```

## Regular Security Tasks

### Daily Tasks
```bash
# Check failed authentication attempts
grep "Failed auth" /var/log/auth.log

# Monitor security group changes
openstack security group event list --days 1

# Check service status
openstack service list --long
```

### Weekly Tasks
```bash
# Rotate encryption keys
keystone-manage fernet_rotate

# Review security group rules
openstack security group list -f json | jq '.[] | {name:.name, rules:.rules}'

# Audit user access
openstack role assignment list --names
```

### Monthly Tasks
```bash
# Review and update security policies
openstack policy list

# Check for inactive users
openstack user list --long

# Update security patches
apt update && apt list --upgradable | grep openstack
```

## Incident Response

### Security Incident Procedures
```bash
# Isolate compromised instance
openstack server stop INSTANCE_ID
neutron port-update PORT_ID --admin-state-down

# Capture forensics
nova instance-action list INSTANCE_ID
openstack console log show INSTANCE_ID > incident_log.txt

# Create evidence snapshot
openstack volume snapshot create --volume VOLUME_ID forensic-snapshot
```

For more detailed security information and best practices, refer to:
- [OpenStack Security Guide](https://docs.openstack.org/security-guide/)
- [OpenStack Security Advisories](https://security.openstack.org/)
