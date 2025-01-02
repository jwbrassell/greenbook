# Network Layer Troubleshooting

## Table of Contents
- [Network Layer Troubleshooting](#network-layer-troubleshooting)
  - [Table of Contents](#table-of-contents)
  - [Common Network Issues](#common-network-issues)
    - [Connectivity Problems](#connectivity-problems)
- [Test basic connectivity](#test-basic-connectivity)
- [Trace route to destination](#trace-route-to-destination)
- [DNS resolution](#dns-resolution)
    - [Port and Service Issues](#port-and-service-issues)
- [Check listening ports](#check-listening-ports)
- [Check service status](#check-service-status)
- [Test specific port](#test-specific-port)
    - [Firewall Configuration](#firewall-configuration)
- [Check firewall status](#check-firewall-status)
- [List firewall rules](#list-firewall-rules)
- [Add/Remove rules](#add/remove-rules)
  - [SSL/TLS Issues](#ssl/tls-issues)
    - [Certificate Problems](#certificate-problems)
- [Check certificate](#check-certificate)
- [Verify certificate](#verify-certificate)
- [Check expiration](#check-expiration)
    - [Common SSL Fixes](#common-ssl-fixes)
- [Generate self-signed certificate](#generate-self-signed-certificate)
- [Generate CSR](#generate-csr)
- [Convert certificate formats](#convert-certificate-formats)
  - [Network Performance](#network-performance)
    - [Bandwidth Issues](#bandwidth-issues)
- [Monitor bandwidth](#monitor-bandwidth)
- [Test network speed](#test-network-speed)
- [Check interface stats](#check-interface-stats)
    - [Network Monitoring](#network-monitoring)
- [Capture packets](#capture-packets)
- [Monitor connections](#monitor-connections)
- [Check network load](#check-network-load)
  - [Web Server Issues](#web-server-issues)
    - [Nginx Troubleshooting](#nginx-troubleshooting)
- [Test nginx configuration](#test-nginx-configuration)
- [Check access logs](#check-access-logs)
- [Check error logs](#check-error-logs)
- [Reload configuration](#reload-configuration)
    - [Apache Troubleshooting](#apache-troubleshooting)
- [Test configuration](#test-configuration)
- [Check status](#check-status)
- [Check logs](#check-logs)
  - [Docker Network Issues](#docker-network-issues)
    - [Container Connectivity](#container-connectivity)
- [List networks](#list-networks)
- [Check container networking](#check-container-networking)
- [View container logs](#view-container-logs)
    - [Docker Network Debugging](#docker-network-debugging)
- [Check port mappings](#check-port-mappings)
- [Inspect container networking](#inspect-container-networking)
- [Reset Docker networking](#reset-docker-networking)
  - [Load Balancer Issues](#load-balancer-issues)
    - [Health Check Problems](#health-check-problems)
- [HAProxy stats](#haproxy-stats)
- [Nginx Plus status](#nginx-plus-status)
- [Check backend connectivity](#check-backend-connectivity)
  - [Network Security](#network-security)
    - [Security Monitoring](#security-monitoring)
- [Monitor suspicious activity](#monitor-suspicious-activity)
- [Check open connections](#check-open-connections)
    - [Security Hardening](#security-hardening)
- [Configure SSH](#configure-ssh)
- [Disable root login](#disable-root-login)
- [Use key authentication](#use-key-authentication)
- [Change default port](#change-default-port)
- [Set up fail2ban](#set-up-fail2ban)
- [Configure iptables](#configure-iptables)
  - [Preventive Measures](#preventive-measures)



## Common Network Issues

### Connectivity Problems

**Symptoms:**
- Service unreachable
- Intermittent connections
- Slow response times
- DNS resolution failures

**Basic Connectivity Checks:**
```bash
# Test basic connectivity
ping -c 4 target_host
ping6 -c 4 ipv6_host

# Trace route to destination
traceroute target_host
mtr target_host

# DNS resolution
dig domain_name
nslookup domain_name
host domain_name
```

### Port and Service Issues

**Symptoms:**
- Connection refused errors
- Service timeout
- Address already in use
- Unable to bind to port

**Commands:**
```bash
# Check listening ports
ss -tuln
netstat -tuln
lsof -i :port_number

# Check service status
systemctl status service_name
journalctl -u service_name

# Test specific port
nc -zv host port
telnet host port
```

### Firewall Configuration

**Symptoms:**
- Connection timeouts
- Service inaccessible
- Partial connectivity

**Commands:**
```bash
# Check firewall status
systemctl status firewalld
ufw status verbose

# List firewall rules
iptables -L -n -v
firewall-cmd --list-all

# Add/Remove rules
firewall-cmd --add-port=80/tcp --permanent
ufw allow 80/tcp
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

## SSL/TLS Issues

### Certificate Problems

**Symptoms:**
- SSL handshake failures
- Certificate validation errors
- Expired certificates
- Chain of trust issues

**Commands:**
```bash
# Check certificate
openssl x509 -in cert.pem -text -noout
openssl s_client -connect host:443 -showcerts

# Verify certificate
openssl verify -CAfile chain.pem cert.pem
openssl s_client -connect host:443 -verify 5

# Check expiration
echo | openssl s_client -servername host -connect host:443 2>/dev/null | openssl x509 -noout -dates
```

### Common SSL Fixes
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout private.key -out certificate.crt

# Generate CSR
openssl req -new -newkey rsa:2048 -nodes \
  -keyout private.key -out request.csr

# Convert certificate formats
openssl pkcs12 -export -out certificate.pfx \
  -inkey private.key -in certificate.crt
```

## Network Performance

### Bandwidth Issues

**Symptoms:**
- Slow data transfer
- High latency
- Packet loss
- Network congestion

**Commands:**
```bash
# Monitor bandwidth
iftop -i eth0
nethogs
iptraf-ng

# Test network speed
speedtest-cli
iperf3 -s  # Server
iperf3 -c server_ip  # Client

# Check interface stats
ip -s link show eth0
ethtool eth0
```

### Network Monitoring

**Tools and Commands:**
```bash
# Capture packets
tcpdump -i eth0 'port 80'
wireshark

# Monitor connections
netstat -ant | awk '{print $6}' | sort | uniq -c
watch -n1 'netstat -ant | grep ESTABLISHED | wc -l'

# Check network load
nload eth0
bmon
```

## Web Server Issues

### Nginx Troubleshooting

**Common Problems:**
- 502 Bad Gateway
- 504 Gateway Timeout
- SSL certificate issues
- Proxy configuration

**Commands:**
```bash
# Test nginx configuration
nginx -t

# Check access logs
tail -f /var/log/nginx/access.log

# Check error logs
tail -f /var/log/nginx/error.log

# Reload configuration
nginx -s reload
```

### Apache Troubleshooting

**Commands:**
```bash
# Test configuration
apachectl configtest

# Check status
systemctl status apache2

# Check logs
tail -f /var/log/apache2/error.log
tail -f /var/log/apache2/access.log
```

## Docker Network Issues

### Container Connectivity

**Symptoms:**
- Container can't reach internet
- Inter-container communication fails
- Port mapping issues
- DNS resolution problems

**Commands:**
```bash
# List networks
docker network ls
docker network inspect network_name

# Check container networking
docker exec container_name ping host
docker exec container_name nslookup domain

# View container logs
docker logs container_name
```

### Docker Network Debugging
```bash
# Check port mappings
docker port container_name
netstat -tulpn | grep docker

# Inspect container networking
docker inspect container_name | grep -A 20 "NetworkSettings"

# Reset Docker networking
systemctl restart docker
docker network prune
```

## Load Balancer Issues

### Health Check Problems

**Symptoms:**
- Backend servers marked as down
- Uneven load distribution
- Connection pooling issues

**Checks:**
```bash
# HAProxy stats
echo "show stat" | socat stdio /var/run/haproxy.sock

# Nginx Plus status
curl http://localhost/nginx_status

# Check backend connectivity
nc -zv backend_host port
curl -I http://backend_host
```

## Network Security

### Security Monitoring

**Commands:**
```bash
# Monitor suspicious activity
fail2ban-client status
lastb | head
grep "Failed password" /var/log/auth.log

# Check open connections
lsof -i
ss -tap
```

### Security Hardening
```bash
# Configure SSH
vim /etc/ssh/sshd_config
# Disable root login
# Use key authentication
# Change default port

# Set up fail2ban
vim /etc/fail2ban/jail.local
systemctl restart fail2ban

# Configure iptables
iptables-save > /etc/iptables/rules.v4
```

## Preventive Measures

1. **Regular Monitoring**
   - Set up network monitoring (Nagios, Prometheus)
   - Configure alerting
   - Monitor bandwidth usage
   - Track error rates

2. **Documentation**
   - Network topology diagrams
   - IP address inventory
   - Service dependencies
   - Configuration changes

3. **Backup and Recovery**
   - Regular configuration backups
   - Disaster recovery plans
   - Failover testing
   - Configuration version control

4. **Security Measures**
   - Regular security audits
   - SSL certificate monitoring
   - Firewall rule review
   - Access control updates
