# RHEL Linux System Health Management Guide

## Table of Contents
- [RHEL Linux System Health Management Guide](#rhel-linux-system-health-management-guide)
  - [System Logs](#system-logs)
    - [Journalctl (systemd Journal)](#journalctl-systemd-journal)
- [View all logs](#view-all-logs)
- [View logs since last boot](#view-logs-since-last-boot)
- [View logs for specific service](#view-logs-for-specific-service)
- [View logs in real-time (follow)](#view-logs-in-real-time-follow)
- [View logs from specific time](#view-logs-from-specific-time)
- [View kernel messages](#view-kernel-messages)
    - [Traditional Log Files](#traditional-log-files)
  - [System Process Management](#system-process-management)
    - [Systemctl Commands](#systemctl-commands)
- [Start a service](#start-a-service)
- [Stop a service](#stop-a-service)
- [Restart a service](#restart-a-service)
- [Reload service configuration](#reload-service-configuration)
- [Check service status](#check-service-status)
- [Enable service to start on boot](#enable-service-to-start-on-boot)
- [Disable service from starting on boot](#disable-service-from-starting-on-boot)
- [Check if service is enabled](#check-if-service-is-enabled)
- [Reload systemd manager configuration](#reload-systemd-manager-configuration)
    - [Process Status and Monitoring](#process-status-and-monitoring)
- [View all processes](#view-all-processes)
- [View process tree](#view-process-tree)
- [Interactive process viewer](#interactive-process-viewer)
- [Advanced interactive process viewer](#advanced-interactive-process-viewer)
- [View memory usage](#view-memory-usage)
- [View system uptime and load](#view-system-uptime-and-load)
  - [Creating System Services](#creating-system-services)
    - [Creating a Systemd Service](#creating-a-systemd-service)
  - [System Resource Monitoring](#system-resource-monitoring)
    - [CPU and Memory](#cpu-and-memory)
- [CPU information](#cpu-information)
- [Memory information](#memory-information)
- [Process resource usage](#process-resource-usage)
    - [Disk Usage](#disk-usage)
- [Disk space usage](#disk-space-usage)
- [Directory size](#directory-size)
- [I/O statistics](#i/o-statistics)
    - [Network Status](#network-status)
- [Network interfaces](#network-interfaces)
- [Network connections](#network-connections)
- [Network statistics](#network-statistics)
  - [System Health Checks](#system-health-checks)
    - [Basic Health Check Commands](#basic-health-check-commands)
- [System load averages](#system-load-averages)
- [Memory usage](#memory-usage)
- [Disk I/O](#disk-i/o)
- [Network statistics](#network-statistics)
- [System errors](#system-errors)
    - [Performance Monitoring Tools](#performance-monitoring-tools)
- [System activity reporter](#system-activity-reporter)
- [Process accounting](#process-accounting)
- [Performance monitoring](#performance-monitoring)
- [System statistics](#system-statistics)
  - [Best Practices](#best-practices)
  - [Troubleshooting Common Issues](#troubleshooting-common-issues)
  - [Additional Tools](#additional-tools)



This guide covers essential commands and procedures for managing system health on RHEL-based Linux systems.

## System Logs

### Journalctl (systemd Journal)

View system logs using journalctl:
```bash
# View all logs
journalctl

# View logs since last boot
journalctl -b

# View logs for specific service
journalctl -u service-name

# View logs in real-time (follow)
journalctl -f

# View logs from specific time
journalctl --since "2023-01-01" --until "2023-12-31"

# View kernel messages
journalctl -k
```

### Traditional Log Files

Important log file locations:
```
/var/log/messages     # General system messages
/var/log/secure      # Security and authentication logs
/var/log/maillog     # Mail server logs
/var/log/cron        # Cron job logs
/var/log/boot.log    # System boot logs
```

View logs in real-time:
```bash
tail -f /var/log/messages
```

## System Process Management

### Systemctl Commands

Basic service management:
```bash
# Start a service
systemctl start service-name

# Stop a service
systemctl stop service-name

# Restart a service
systemctl restart service-name

# Reload service configuration
systemctl reload service-name

# Check service status
systemctl status service-name

# Enable service to start on boot
systemctl enable service-name

# Disable service from starting on boot
systemctl disable service-name

# Check if service is enabled
systemctl is-enabled service-name

# Reload systemd manager configuration
systemctl daemon-reload
```

### Process Status and Monitoring

Monitor system processes:
```bash
# View all processes
ps aux

# View process tree
pstree

# Interactive process viewer
top

# Advanced interactive process viewer
htop

# View memory usage
free -h

# View system uptime and load
uptime
```

## Creating System Services

### Creating a Systemd Service

1. Create a service file in `/etc/systemd/system/myservice.service`:

```ini
[Unit]
Description=My Custom Service
After=network.target

[Service]
Type=simple
User=myuser
ExecStart=/path/to/your/program
Restart=on-failure
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=myservice

[Install]
WantedBy=multi-user.target
```

2. Reload systemd and enable the service:
```bash
systemctl daemon-reload
systemctl enable myservice
systemctl start myservice
```

## System Resource Monitoring

### CPU and Memory

```bash
# CPU information
lscpu
cat /proc/cpuinfo

# Memory information
free -h
cat /proc/meminfo

# Process resource usage
top
htop
```

### Disk Usage

```bash
# Disk space usage
df -h

# Directory size
du -sh /path/to/directory

# I/O statistics
iostat
```

### Network Status

```bash
# Network interfaces
ip addr
ifconfig

# Network connections
netstat -tuln
ss -tuln

# Network statistics
nethogs
iftop
```

## System Health Checks

### Basic Health Check Commands

```bash
# System load averages
uptime

# Memory usage
vmstat 1

# Disk I/O
iostat 1

# Network statistics
netstat -s

# System errors
dmesg | grep -i error
```

### Performance Monitoring Tools

```bash
# System activity reporter
sar

# Process accounting
psacct

# Performance monitoring
perf

# System statistics
nmon
```

## Best Practices

1. Regular Monitoring:
   - Set up regular monitoring of system logs
   - Monitor system resource usage
   - Track service status

2. Proactive Maintenance:
   - Regularly check system updates
   - Monitor disk space usage
   - Review system performance metrics

3. Documentation:
   - Keep records of system changes
   - Document custom service configurations
   - Maintain troubleshooting procedures

4. Automation:
   - Set up automated health checks
   - Configure automatic log rotation
   - Implement automated backups

## Troubleshooting Common Issues

1. High CPU Usage:
```bash
top
ps aux --sort=-%cpu | head -n 10
```

2. Memory Issues:
```bash
free -h
vmstat 1
```

3. Disk Space Problems:
```bash
df -h
du -sh /* | sort -hr
```

4. Service Failures:
```bash
systemctl status service-name
journalctl -u service-name -n 100
```

## Additional Tools

1. System Monitoring:
   - Nagios
   - Zabbix
   - Prometheus
   - Grafana

2. Log Management:
   - ELK Stack (Elasticsearch, Logstash, Kibana)
   - Graylog
   - Splunk

3. Performance Analysis:
   - atop
   - iotop
   - sysstat
