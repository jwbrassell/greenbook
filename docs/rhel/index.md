# RHEL-based Linux Documentation

## Table of Contents
- [RHEL-based Linux Documentation](#rhel-based-linux-documentation)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [System Management](#system-management)
  - [Security Configuration](#security-configuration)
  - [Performance Optimization](#performance-optimization)
  - [Testing and Validation](#testing-and-validation)
  - [Troubleshooting](#troubleshooting)
  - [Best Practices](#best-practices)
  - [Integration Points](#integration-points)
  - [Next Steps](#next-steps)

## Overview
This comprehensive guide covers Red Hat Enterprise Linux (RHEL) and its derivatives like CentOS and Rocky Linux. Learn essential system administration tasks, security hardening, and performance optimization techniques.

## Prerequisites
- Basic Linux knowledge
- Understanding of:
  - Command line interface
  - System administration concepts
  - Networking fundamentals
  - Security principles
- Hardware requirements:
  - Minimum 2GB RAM
  - 20GB disk space
  - x86_64 architecture

## Installation and Setup
1. System Installation:
```bash
# Check system requirements
dmidecode -t system

# Create bootable USB (on Linux)
sudo dd if=rhel-8.5-x86_64.iso of=/dev/sdX bs=8M status=progress
```

2. Initial Configuration:
```bash
# Set hostname
hostnamectl set-hostname rhel-server

# Configure network
nmcli connection modify eth0 ipv4.addresses "192.168.1.100/24"
nmcli connection modify eth0 ipv4.gateway "192.168.1.1"
nmcli connection up eth0
```

## System Management
1. Package Management:
```bash
# Update system
sudo dnf update -y

# Install package group
sudo dnf group install "Development Tools"

# Search for package
dnf search httpd

# Show package info
dnf info httpd
```

2. Service Management:
```bash
# Start and enable service
sudo systemctl start httpd
sudo systemctl enable httpd

# Check service status
systemctl status httpd

# View service logs
journalctl -u httpd
```

## Security Configuration
1. Firewall Management:
```bash
# Configure firewall
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload

# View configuration
firewall-cmd --list-all
```

2. SELinux Configuration:
```bash
# Check SELinux status
getenforce

# Configure SELinux context
semanage fcontext -a -t httpd_sys_content_t "/var/www/html(/.*)?"
restorecon -Rv /var/www/html/
```

## Performance Optimization
1. System Tuning:
```bash
# Configure system limits
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_max_syn_backlog = 4096
net.core.somaxconn = 4096
net.ipv4.tcp_fin_timeout = 30
EOF

sysctl -p
```

2. Resource Management:
```bash
# Monitor system resources
top -b n 1
vmstat 1 5
iostat -x 1 5

# Configure process limits
ulimit -n 65535
```

## Testing and Validation
1. System Testing:
```bash
# Check system health
sudo dnf install -y stress-ng
stress-ng --cpu 4 --io 2 --vm 1 --vm-bytes 1G --timeout 60s

# Network testing
ping -c 4 google.com
traceroute google.com
```

2. Security Testing:
```bash
# Scan for vulnerabilities
sudo dnf install -y openscap-scanner
oscap info /usr/share/xml/scap/ssg/content/ssg-rhel8-ds.xml
```

## Troubleshooting
1. System Issues:
```bash
# Check system logs
journalctl -xe
tail -f /var/log/messages

# Check disk space
df -h
du -sh /*
```

2. Network Issues:
```bash
# Test connectivity
nc -zv localhost 80
tcpdump -i any port 80

# Check routing
ip route
traceroute google.com
```

## Best Practices
1. Security Hardening:
```bash
# Disable unused services
systemctl disable bluetooth
systemctl disable cups

# Configure password policy
authconfig --passminlen=12 --update
```

2. Backup Strategy:
```bash
# Create system backup
tar -czf /backup/system-$(date +%F).tar.gz /etc /var/log

# Configure automated backups
cat > /etc/cron.daily/backup << EOF
#!/bin/bash
tar -czf /backup/daily-$(date +%F).tar.gz /important/data
find /backup -name "daily-*.tar.gz" -mtime +7 -delete
EOF
chmod +x /etc/cron.daily/backup
```

## Integration Points
1. Directory Services:
```bash
# Configure LDAP client
authconfig --enableldap \
          --enableldapauth \
          --ldapserver=ldap.example.com \
          --ldapbasedn="dc=example,dc=com" \
          --update
```

2. Monitoring Integration:
```bash
# Install and configure node_exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
tar xvfz node_exporter-*.tar.gz
sudo mv node_exporter-*/node_exporter /usr/local/bin/

# Create systemd service
cat > /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now node_exporter
```

## Next Steps
1. Advanced Topics
   - Clustering and high availability
   - Container orchestration
   - Advanced storage management
   - Performance tuning

2. Further Learning
   - [Red Hat Documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8)
   - [CentOS Documentation](https://docs.centos.org/)
   - [Rocky Linux Documentation](https://docs.rockylinux.org/)
   - Community resources

## Related Documentation
- [ACL Permissions](acl_permissions.md)
- [Crontab Management](crontab_management.md)
- [System Health](system_health.md)
- [User Permission Management](user_permission_management.md)

## Contributing
Feel free to contribute to this documentation by submitting pull requests or opening issues for improvements. Please ensure your contributions follow our documentation standards and include practical examples.
