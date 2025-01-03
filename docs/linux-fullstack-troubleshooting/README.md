# Linux Full-Stack Troubleshooting Guide

## Table of Contents
- [Linux Full-Stack Troubleshooting Guide](#linux-full-stack-troubleshooting-guide)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [System Level Troubleshooting](#system-level-troubleshooting)
  - [Network Layer Issues](#network-layer-issues)
  - [Database Layer Problems](#database-layer-problems)
  - [Backend Services](#backend-services)
  - [Frontend Development](#frontend-development)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing Strategies](#testing-strategies)
  - [Best Practices](#best-practices)
  - [Integration Points](#integration-points)
  - [Next Steps](#next-steps)

## Overview
This comprehensive guide provides systematic approaches to troubleshooting full-stack development environments on Linux systems. Learn how to diagnose and resolve issues across different layers of the stack, from system-level problems to application-specific challenges.

## Prerequisites
- Basic Linux administration skills
- Understanding of:
  - System architecture
  - Networking concepts
  - Web technologies
  - Database systems
- Access to root/sudo privileges
- Familiarity with common development tools

## Installation and Setup
1. Essential Tools Installation:
```bash
# System monitoring tools
sudo apt install htop iotop iftop
sudo apt install sysstat net-tools

# Log analysis tools
sudo apt install logwatch goaccess

# Network debugging
sudo apt install tcpdump wireshark
```

2. Monitoring Setup:
```bash
# Enable system statistics
sudo systemctl enable sysstat
sudo systemctl start sysstat

# Configure log rotation
sudo nano /etc/logrotate.d/custom-logs
```

## System Level Troubleshooting
1. Resource Monitoring:
```bash
# CPU and Memory
top -b n 1
vmstat 1 5
free -h

# Disk Usage
df -h
iostat -x 1 5
```

2. Process Management:
```bash
# List processes
ps aux | grep [service]

# Check service status
systemctl status [service]
journalctl -u [service] -f

# Process tree
pstree -p
```

## Network Layer Issues
1. Connectivity Checks:
```bash
# Port status
netstat -tulpn
ss -tunlp

# Network interfaces
ip addr show
ifconfig -a

# DNS resolution
dig example.com
nslookup example.com
```

2. Firewall Configuration:
```bash
# UFW status
sudo ufw status verbose

# IPTables rules
sudo iptables -L -n -v
```

## Database Layer Problems
1. Connection Testing:
```bash
# MySQL
mysqladmin ping -h localhost -u root -p

# PostgreSQL
pg_isready -h localhost -p 5432

# MongoDB
mongosh --eval "db.adminCommand('ping')"
```

2. Performance Analysis:
```sql
-- MySQL slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- PostgreSQL
SELECT * FROM pg_stat_activity WHERE state = 'active';
```

## Backend Services
1. API Endpoint Testing:
```bash
# HTTP request testing
curl -v http://localhost:8080/api/health

# WebSocket testing
websocat ws://localhost:8080/ws
```

2. Log Analysis:
```bash
# Application logs
tail -f /var/log/application/app.log

# Error tracking
grep -r "ERROR" /var/log/application/
```

## Frontend Development
1. Build Process:
```bash
# Node.js diagnostics
node --trace-deprecation app.js

# Webpack analysis
webpack --profile --json > stats.json
```

2. Performance Monitoring:
```javascript
// Browser performance metrics
console.time('Operation');
// Your code here
console.timeEnd('Operation');
```

## Security Considerations
1. SSL/TLS Verification:
```bash
# Check SSL certificate
openssl s_client -connect example.com:443 -tls1_2

# Security headers
curl -I https://example.com
```

2. File Permissions:
```bash
# Check permissions
namei -l /path/to/app

# Set secure permissions
chmod 750 /path/to/app
chown -R www-data:www-data /path/to/app
```

## Performance Optimization
1. System Tuning:
```bash
# System limits
ulimit -n 65535

# Kernel parameters
sysctl -w net.core.somaxconn=65535
```

2. Application Profiling:
```python
import cProfile

def profile_code():
    profiler = cProfile.Profile()
    profiler.enable()
    # Your code here
    profiler.disable()
    profiler.print_stats()
```

## Testing Strategies
1. System Testing:
```bash
# Load testing
ab -n 1000 -c 10 http://localhost:8080/

# Network testing
iperf3 -c localhost -p 5201
```

2. Application Testing:
```python
def test_service_health():
    response = requests.get('http://localhost:8080/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'
```

## Best Practices
1. Logging Strategy:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

2. Monitoring Setup:
```yaml
# Prometheus configuration
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

## Integration Points
1. Service Integration:
```python
def check_service_dependencies():
    services = [
        'database',
        'cache',
        'message_queue'
    ]
    for service in services:
        check_service_health(service)
```

2. External APIs:
```python
def verify_external_services():
    endpoints = {
        'auth': 'http://auth-service:8080/health',
        'payment': 'http://payment-service:8080/health'
    }
    for service, url in endpoints.items():
        check_endpoint_health(url)
```

## Next Steps
1. Advanced Topics
   - Container orchestration
   - Microservices debugging
   - Distributed tracing
   - Chaos engineering

2. Further Learning
   - [Linux Performance](http://www.brendangregg.com/linuxperf.html)
   - [System Design Primer](https://github.com/donnemartin/system-design-primer)
   - [SRE Books](https://sre.google/books/)
   - Community resources
