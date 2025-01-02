# Backend Services Troubleshooting

## Table of Contents
- [Backend Services Troubleshooting](#backend-services-troubleshooting)
  - [Table of Contents](#table-of-contents)
  - [API Endpoint Issues](#api-endpoint-issues)
    - [Common API Problems](#common-api-problems)
- [Test endpoint availability](#test-endpoint-availability)
- [Check response times](#check-response-times)
- [Monitor API traffic](#monitor-api-traffic)
    - [API Testing Tools](#api-testing-tools)
- [Using curl with different methods](#using-curl-with-different-methods)
- [Using httpie (more readable output)](#using-httpie-more-readable-output)
- [Load testing with Apache Bench](#load-testing-with-apache-bench)
  - [Service Dependencies](#service-dependencies)
    - [Microservices Issues](#microservices-issues)
- [Check service status](#check-service-status)
- [View service logs](#view-service-logs)
- [Network connectivity](#network-connectivity)
    - [Service Management](#service-management)
- [Restart services](#restart-services)
- [Check resource usage](#check-resource-usage)
- [View service configuration](#view-service-configuration)
  - [Memory Leaks](#memory-leaks)
    - [Detection and Analysis](#detection-and-analysis)
- [Memory usage monitoring](#memory-usage-monitoring)
- [Node.js specific](#nodejs-specific)
- [Then connect Chrome DevTools](#then-connect-chrome-devtools)
- [Java specific](#java-specific)
    - [Heap Analysis](#heap-analysis)
- [Node.js heap snapshot](#nodejs-heap-snapshot)
- [Java heap dump](#java-heap-dump)
- [Analysis tools](#analysis-tools)
- [For Node.js](#for-nodejs)
- [For Java](#for-java)
  - [Runtime Errors](#runtime-errors)
    - [Application Crashes](#application-crashes)
- [Check system logs](#check-system-logs)
- [Application specific logs](#application-specific-logs)
- [Core dumps](#core-dumps)
    - [Error Tracking](#error-tracking)
- [Log aggregation](#log-aggregation)
- [Stack traces](#stack-traces)
  - [Performance Issues](#performance-issues)
    - [CPU Profiling](#cpu-profiling)
- [System-wide profiling](#system-wide-profiling)
- [Application specific](#application-specific)
    - [Memory Profiling](#memory-profiling)
- [System memory analysis](#system-memory-analysis)
- [Process memory](#process-memory)
  - [Logging and Monitoring](#logging-and-monitoring)
    - [Log Management](#log-management)
- [Real-time log monitoring](#real-time-log-monitoring)
- [Log statistics](#log-statistics)
- [Log rotation check](#log-rotation-check)
    - [Monitoring Setup](#monitoring-setup)
- [Prometheus setup](#prometheus-setup)
- [Grafana dashboard setup](#grafana-dashboard-setup)
  - [Security Issues](#security-issues)
    - [Access Control](#access-control)
- [Check file permissions](#check-file-permissions)
- [Process permissions](#process-permissions)
    - [SSL/TLS Configuration](#ssl/tls-configuration)
- [Check SSL configuration](#check-ssl-configuration)
- [Certificate validation](#certificate-validation)
  - [Deployment Issues](#deployment-issues)
    - [Container Problems](#container-problems)
- [Check container status](#check-container-status)
- [Resource usage](#resource-usage)
- [Clean up](#clean-up)
    - [Version Control](#version-control)
- [Check current version](#check-current-version)
- [Review changes](#review-changes)
  - [Best Practices](#best-practices)
    - [Monitoring Checklist](#monitoring-checklist)
    - [Documentation Requirements](#documentation-requirements)
  - [Recovery Procedures](#recovery-procedures)
    - [Service Recovery](#service-recovery)
    - [Data Recovery](#data-recovery)
  - [Preventive Measures](#preventive-measures)



## API Endpoint Issues

### Common API Problems

**Symptoms:**
- 4xx/5xx HTTP errors
- Slow response times
- Timeout errors
- Invalid responses

**Basic Checks:**
```bash
# Test endpoint availability
curl -I http://api-endpoint
curl -v http://api-endpoint

# Check response times
time curl -o /dev/null -s -w "%{time_total}\n" http://api-endpoint

# Monitor API traffic
tcpdump -i any port 80 -w api_traffic.pcap
```

### API Testing Tools

```bash
# Using curl with different methods
curl -X GET http://api/endpoint
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://api/endpoint

# Using httpie (more readable output)
http GET http://api/endpoint
http POST http://api/endpoint key=value

# Load testing with Apache Bench
ab -n 1000 -c 10 http://api/endpoint
```

## Service Dependencies

### Microservices Issues

**Symptoms:**
- Service discovery failures
- Circuit breaker triggers
- Cascading failures
- Communication timeouts

**Monitoring Commands:**
```bash
# Check service status
systemctl status service-name
docker ps
docker-compose ps

# View service logs
journalctl -u service-name -f
docker logs container_name
docker-compose logs service_name

# Network connectivity
netstat -tulpn
lsof -i :port
```

### Service Management

```bash
# Restart services
systemctl restart service-name
docker-compose restart service_name

# Check resource usage
docker stats
top -p $(pgrep -d',' service-name)

# View service configuration
cat /etc/systemd/system/service-name.service
docker-compose config
```

## Memory Leaks

### Detection and Analysis

**Tools and Commands:**
```bash
# Memory usage monitoring
ps aux | grep service-name
pmap -x PID

# Node.js specific
node --inspect app.js
# Then connect Chrome DevTools

# Java specific
jmap -heap PID
jstack PID
```

### Heap Analysis

```bash
# Node.js heap snapshot
node --heap-prof app.js

# Java heap dump
jmap -dump:format=b,file=heap.bin PID

# Analysis tools
# For Node.js
node --prof-process isolate-*.log

# For Java
jhat heap.bin
```

## Runtime Errors

### Application Crashes

**Initial Response:**
```bash
# Check system logs
journalctl -xe
tail -f /var/log/syslog

# Application specific logs
tail -f /var/log/application.log
docker logs -f container_name

# Core dumps
coredumpctl list
coredumpctl info PID
```

### Error Tracking

```bash
# Log aggregation
grep -r "Error" /var/log/
journalctl -p err

# Stack traces
dmesg | grep -i error
gdb program core
```

## Performance Issues

### CPU Profiling

```bash
# System-wide profiling
perf record -F 99 -a -g -- sleep 30
perf report

# Application specific
perf record -F 99 -p PID -g -- sleep 30
strace -c -p PID
```

### Memory Profiling

```bash
# System memory analysis
free -h
vmstat 1
sar -r 1 3

# Process memory
ps -eo pid,ppid,%mem,%cpu,cmd --sort=-%mem | head
pmap -x PID
```

## Logging and Monitoring

### Log Management

**Key Log Locations:**
```
/var/log/application/    # Application logs
/var/log/nginx/         # Web server logs
/var/log/docker/        # Container logs
/var/log/journal/       # SystemD journal
```

**Log Analysis Tools:**
```bash
# Real-time log monitoring
tail -f /var/log/application.log | grep --line-buffered "ERROR"

# Log statistics
awk '/ERROR/ {print $0}' /var/log/application.log | sort | uniq -c

# Log rotation check
logrotate -d /etc/logrotate.d/application
```

### Monitoring Setup

```bash
# Prometheus setup
cat > /etc/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'application'
    static_configs:
      - targets: ['localhost:8080']
EOF

# Grafana dashboard setup
grafana-cli plugins install grafana-piechart-panel
```

## Security Issues

### Access Control

```bash
# Check file permissions
ls -la /path/to/application
namei -l /path/to/application

# Process permissions
ps aux | grep application
sudo -l
```

### SSL/TLS Configuration

```bash
# Check SSL configuration
openssl s_client -connect host:443 -tls1_2
curl -vI https://host

# Certificate validation
openssl verify -CAfile chain.pem cert.pem
```

## Deployment Issues

### Container Problems

```bash
# Check container status
docker ps -a
docker inspect container_name

# Resource usage
docker stats
docker events

# Clean up
docker system prune
docker volume prune
```

### Version Control

```bash
# Check current version
git describe --tags
git rev-parse HEAD

# Review changes
git log --since="24 hours ago"
git diff master...develop
```

## Best Practices

### Monitoring Checklist

1. **Application Health:**
   - Endpoint response times
   - Error rates
   - Resource usage
   - Transaction volume

2. **System Health:**
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network traffic

3. **Dependencies:**
   - Database connections
   - Cache hit rates
   - Queue lengths
   - External service status

### Documentation Requirements

1. **System Architecture:**
   - Service dependencies
   - Network topology
   - Data flow diagrams
   - API documentation

2. **Operational Procedures:**
   - Deployment process
   - Backup procedures
   - Recovery plans
   - Scaling guidelines

3. **Monitoring Setup:**
   - Alert thresholds
   - Escalation procedures
   - On-call rotations
   - Incident response

## Recovery Procedures

### Service Recovery

1. **Initial Assessment:**
   ```bash
   # Check service status
   systemctl status service-name
   
   # View recent logs
   journalctl -u service-name -n 100
   
   # Check resource usage
   top -p $(pgrep -d',' service-name)
   ```

2. **Recovery Steps:**
   ```bash
   # Restart service
   systemctl restart service-name
   
   # Verify recovery
   curl -I http://service-endpoint
   
   # Monitor logs
   tail -f /var/log/service-name.log
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
   systemctl stop service-name
   
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
   # Log rotation
   logrotate -f /etc/logrotate.d/application
   
   # Cleanup old files
   find /tmp -type f -mtime +7 -delete
   ```

3. **Performance Optimization:**
   ```bash
   # Profile application
   perf record -F 99 -p PID -g -- sleep 30
   
   # Analyze results
   perf report
