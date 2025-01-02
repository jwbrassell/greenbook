# DevOps & Deployment Troubleshooting

## Table of Contents
- [DevOps & Deployment Troubleshooting](#devops-&-deployment-troubleshooting)
  - [Table of Contents](#table-of-contents)
  - [CI/CD Pipeline Issues](#ci/cd-pipeline-issues)
    - [Common Pipeline Problems](#common-pipeline-problems)
- [Check Jenkins status](#check-jenkins-status)
- [View Jenkins logs](#view-jenkins-logs)
- [Check workspace](#check-workspace)
- [Clean workspace](#clean-workspace)
    - [GitLab CI Issues](#gitlab-ci-issues)
- [Check runner status](#check-runner-status)
- [View runner logs](#view-runner-logs)
- [Clean runner cache](#clean-runner-cache)
  - [Container Problems](#container-problems)
    - [Docker Issues](#docker-issues)
- [Check Docker status](#check-docker-status)
- [View container logs](#view-container-logs)
- [Check container health](#check-container-health)
    - [Container Debugging](#container-debugging)
- [Enter container](#enter-container)
- [Check container network](#check-container-network)
- [View container processes](#view-container-processes)
- [Check container resources](#check-container-resources)
  - [Environment Variables](#environment-variables)
    - [Configuration Issues](#configuration-issues)
- [Check environment variables](#check-environment-variables)
- [Source environment files](#source-environment-files)
- [Check for missing variables](#check-for-missing-variables)
    - [Secrets Management](#secrets-management)
- [Vault operations](#vault-operations)
- [Check AWS secrets](#check-aws-secrets)
  - [Deployment Failures](#deployment-failures)
    - [Common Issues](#common-issues)
- [Check service status](#check-service-status)
- [Check logs](#check-logs)
- [Monitor resources](#monitor-resources)
    - [Kubernetes Issues](#kubernetes-issues)
- [Check pod status](#check-pod-status)
- [View pod logs](#view-pod-logs)
- [Check cluster health](#check-cluster-health)
  - [Infrastructure Problems](#infrastructure-problems)
    - [Server Issues](#server-issues)
- [Check system resources](#check-system-resources)
- [Monitor system load](#monitor-system-load)
- [Check system logs](#check-system-logs)
    - [Network Problems](#network-problems)
- [Check connectivity](#check-connectivity)
- [Monitor network traffic](#monitor-network-traffic)
- [Check open ports](#check-open-ports)
  - [Monitoring and Alerts](#monitoring-and-alerts)
    - [Prometheus Issues](#prometheus-issues)
- [Check Prometheus status](#check-prometheus-status)
- [Query metrics](#query-metrics)
- [Check targets](#check-targets)
    - [Grafana Problems](#grafana-problems)
- [Check Grafana status](#check-grafana-status)
- [Reset admin password](#reset-admin-password)
- [Check datasources](#check-datasources)
  - [Backup and Recovery](#backup-and-recovery)
    - [Backup Issues](#backup-issues)
- [Check backup status](#check-backup-status)
- [Verify backup integrity](#verify-backup-integrity)
- [Test restore](#test-restore)
    - [Disaster Recovery](#disaster-recovery)
- [Check DR procedures](#check-dr-procedures)
- [Test failover](#test-failover)
- [Verify replication](#verify-replication)
  - [Security Issues](#security-issues)
    - [SSL/TLS Problems](#ssl/tls-problems)
- [Check certificate](#check-certificate)
- [Verify chain](#verify-chain)
- [Test SSL connection](#test-ssl-connection)
    - [Firewall Issues](#firewall-issues)
- [Check firewall status](#check-firewall-status)
- [Test port access](#test-port-access)
- [Monitor connections](#monitor-connections)
  - [Best Practices](#best-practices)
    - [Deployment Checklist](#deployment-checklist)
    - [Monitoring Setup](#monitoring-setup)
    - [Documentation Requirements](#documentation-requirements)
  - [Recovery Procedures](#recovery-procedures)
    - [Service Recovery](#service-recovery)
    - [Data Recovery](#data-recovery)
  - [Preventive Measures](#preventive-measures)



## CI/CD Pipeline Issues

### Common Pipeline Problems

**Symptoms:**
- Build failures
- Test failures
- Deployment timeouts
- Integration errors

**Jenkins Issues:**
```bash
# Check Jenkins status
systemctl status jenkins
journalctl -u jenkins

# View Jenkins logs
tail -f /var/log/jenkins/jenkins.log

# Check workspace
ls -la /var/lib/jenkins/workspace/

# Clean workspace
rm -rf /var/lib/jenkins/workspace/*
```

### GitLab CI Issues

```bash
# Check runner status
gitlab-runner status
gitlab-runner verify

# View runner logs
gitlab-runner debug

# Clean runner cache
gitlab-runner cache clean
```

## Container Problems

### Docker Issues

**Common Problems:**
```bash
# Check Docker status
systemctl status docker
docker info

# View container logs
docker logs container_name
docker logs --tail 100 container_name

# Check container health
docker inspect container_name
docker stats container_name
```

### Container Debugging

```bash
# Enter container
docker exec -it container_name /bin/bash

# Check container network
docker network inspect network_name

# View container processes
docker top container_name

# Check container resources
docker stats --no-stream container_name
```

## Environment Variables

### Configuration Issues

```bash
# Check environment variables
printenv
env | grep SERVICE_

# Source environment files
source .env
set -a; source .env; set +a

# Check for missing variables
env | grep -i key_name
```

### Secrets Management

```bash
# Vault operations
vault status
vault list secret/

# Check AWS secrets
aws secretsmanager list-secrets
aws secretsmanager get-secret-value --secret-id name
```

## Deployment Failures

### Common Issues

**Symptoms:**
- Service won't start
- Configuration errors
- Permission issues
- Resource constraints

**Basic Checks:**
```bash
# Check service status
systemctl status service_name
journalctl -u service_name -f

# Check logs
tail -f /var/log/syslog
docker-compose logs -f

# Monitor resources
top
htop
free -h
```

### Kubernetes Issues

```bash
# Check pod status
kubectl get pods
kubectl describe pod pod_name

# View pod logs
kubectl logs pod_name
kubectl logs -f pod_name -c container_name

# Check cluster health
kubectl get nodes
kubectl cluster-info
```

## Infrastructure Problems

### Server Issues

```bash
# Check system resources
df -h
free -m
uptime

# Monitor system load
sar -u 1 5
vmstat 1

# Check system logs
journalctl -xe
dmesg | tail
```

### Network Problems

```bash
# Check connectivity
ping host
traceroute host

# Monitor network traffic
iftop
nethogs

# Check open ports
netstat -tulpn
ss -tulpn
```

## Monitoring and Alerts

### Prometheus Issues

```bash
# Check Prometheus status
systemctl status prometheus
curl localhost:9090/-/healthy

# Query metrics
promtool query instant http://localhost:9090 query

# Check targets
curl -s localhost:9090/api/v1/targets
```

### Grafana Problems

```bash
# Check Grafana status
systemctl status grafana-server

# Reset admin password
grafana-cli admin reset-admin-password newpass

# Check datasources
ls -l /var/lib/grafana/datasources/
```

## Backup and Recovery

### Backup Issues

```bash
# Check backup status
systemctl status backup-service
ls -l /backup/

# Verify backup integrity
md5sum backup_file
tar tvf backup.tar.gz

# Test restore
tar xvf backup.tar.gz -C /tmp/test/
```

### Disaster Recovery

```bash
# Check DR procedures
cat disaster-recovery.md

# Test failover
drbd-overview
pcs status

# Verify replication
mysql -e "SHOW SLAVE STATUS\G"
```

## Security Issues

### SSL/TLS Problems

```bash
# Check certificate
openssl x509 -in cert.pem -text -noout

# Verify chain
openssl verify -CAfile chain.pem cert.pem

# Test SSL connection
openssl s_client -connect host:443
```

### Firewall Issues

```bash
# Check firewall status
ufw status
iptables -L

# Test port access
nc -zv host port
telnet host port

# Monitor connections
netstat -ant
lsof -i
```

## Best Practices

### Deployment Checklist

1. **Pre-deployment:**
   - Backup verification
   - Environment validation
   - Resource check
   - Security scan

2. **Deployment Process:**
   - Rolling updates
   - Health checks
   - Monitoring
   - Rollback plan

3. **Post-deployment:**
   - Service verification
   - Performance check
   - Log analysis
   - User notification

### Monitoring Setup

1. **System Monitoring:**
   ```bash
   # Install monitoring stack
   apt-get install prometheus
   apt-get install grafana
   apt-get install node_exporter
   ```

2. **Application Monitoring:**
   ```bash
   # Check application metrics
   curl localhost:8080/metrics
   
   # View application logs
   tail -f /var/log/application/
   ```

### Documentation Requirements

1. **System Architecture:**
   - Infrastructure diagram
   - Network topology
   - Service dependencies
   - Security zones

2. **Operational Procedures:**
   - Deployment steps
   - Rollback procedures
   - Backup processes
   - Emergency responses

3. **Monitoring Setup:**
   - Alert thresholds
   - Escalation paths
   - On-call rotation
   - Incident response

## Recovery Procedures

### Service Recovery

1. **Initial Assessment:**
   ```bash
   # Check service status
   systemctl status service_name
   
   # View recent logs
   journalctl -u service_name -n 100
   
   # Check dependencies
   systemctl list-dependencies service_name
   ```

2. **Recovery Steps:**
   ```bash
   # Restart service
   systemctl restart service_name
   
   # Verify recovery
   curl -I http://service-endpoint
   
   # Monitor logs
   tail -f /var/log/service_name.log
   ```

### Data Recovery

1. **Backup Verification:**
   ```bash
   # List backups
   ls -l /backup/directory
   
   # Check backup integrity
   md5sum backup_file
   ```

2. **Restore Process:**
   ```bash
   # Stop service
   systemctl stop service_name
   
   # Restore data
   tar xzf backup.tar.gz -C /restore/path
   
   # Verify restoration
   diff -r /backup/path /restore/path
   ```

## Preventive Measures

1. **Automated Monitoring:**
   ```bash
   # Set up monitoring
   apt-get install prometheus node-exporter
   
   # Configure alerts
   vim /etc/prometheus/alerts.yml
   ```

2. **Regular Maintenance:**
   ```bash
   # Update systems
   apt-get update && apt-get upgrade
   
   # Clean old files
   find /tmp -type f -mtime +7 -delete
   ```

3. **Security Updates:**
   ```bash
   # Check security updates
   apt-get update && apt-get upgrade
   
   # Audit system
   lynis audit system
