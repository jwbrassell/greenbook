# F5 Monitoring and Health Checks Guide

## Table of Contents
- [F5 Monitoring and Health Checks Guide](#f5-monitoring-and-health-checks-guide)
  - [System Health Monitoring](#system-health-monitoring)
  - [GTM Monitoring](#gtm-monitoring)
  - [LTM Monitoring](#ltm-monitoring)
  - [SSL Certificate Monitoring](#ssl-certificate-monitoring)
  - [Comprehensive Health Check](#comprehensive-health-check)
  - [Usage Example](#usage-example)
  - [Monitoring Best Practices](#monitoring-best-practices)
  - [Common Monitoring Issues](#common-monitoring-issues)



This guide covers comprehensive monitoring strategies for F5 GTM and LTM instances, including health checks, performance monitoring, and status reporting.

## System Health Monitoring

```python
from f5.bigip import ManagementRoot
from datetime import datetime
import json

def get_system_health(mgmt):
    """Get overall system health status"""
    try:
        # Get system statistics
        sys_stats = mgmt.tm.sys.performance.get_collection()
        
        # Get CPU usage
        cpu_stats = mgmt.tm.sys.cpu.get_collection()
        
        # Get memory usage
        memory = mgmt.tm.sys.memory.get_collection()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': [{'name': cpu.name, 'usage': cpu.usageRatio} for cpu in cpu_stats],
            'memory_usage': [{'name': mem.name, 'used': mem.memoryUsed} for mem in memory],
            'system_performance': {
                'throughput': sys_stats[0].throughputPerformance,
                'cpu_score': sys_stats[0].cpuScore,
                'memory_score': sys_stats[0].memoryScore
            }
        }
    except Exception as e:
        print(f"Failed to get system health: {str(e)}")
        return None

def monitor_disk_usage(mgmt):
    """Monitor disk usage across partitions"""
    try:
        disk_info = mgmt.tm.sys.disk.get_collection()
        return [{
            'partition': disk.name,
            'total_size': disk.size,
            'used_space': disk.usedSpace,
            'free_space': disk.freeSpace
        } for disk in disk_info]
    except Exception as e:
        print(f"Failed to get disk usage: {str(e)}")
        return None
```

## GTM Monitoring

```python
def monitor_gtm_wide_ips(mgmt):
    """Monitor all GTM Wide IPs"""
    try:
        wide_ips = mgmt.tm.gtm.wideips.get_collection()
        status = []
        for wide_ip in wide_ips:
            stats = wide_ip.stats.load()
            status.append({
                'name': wide_ip.name,
                'pools': wide_ip.pools,
                'load_balancing_mode': wide_ip.loadBalancingMode,
                'status': stats.entries['status.availabilityState']['description'],
                'requests_per_second': stats.entries['requestsPerSecond']['value']
            })
        return status
    except Exception as e:
        print(f"Failed to monitor Wide IPs: {str(e)}")
        return None

def check_gtm_datacenter_status(mgmt):
    """Check status of all GTM data centers"""
    try:
        dcs = mgmt.tm.gtm.datacenters.get_collection()
        return [{
            'name': dc.name,
            'enabled': getattr(dc, 'enabled', True),
            'status': getattr(dc, 'status', 'unknown'),
            'probe_protocol': getattr(dc, 'probeProtocol', 'tcp'),
            'probe_timeout': getattr(dc, 'probeTimeout', 300)
        } for dc in dcs]
    except Exception as e:
        print(f"Failed to check datacenter status: {str(e)}")
        return None
```

## LTM Monitoring

```python
def monitor_virtual_servers(mgmt):
    """Monitor all virtual servers"""
    try:
        virtuals = mgmt.tm.ltm.virtuals.get_collection()
        status = []
        for virtual in virtuals:
            stats = virtual.stats.load()
            status.append({
                'name': virtual.name,
                'destination': virtual.destination,
                'pool': getattr(virtual, 'pool', None),
                'status': stats.entries['status.availabilityState']['description'],
                'current_connections': stats.entries['clientside.curConns']['value'],
                'total_connections': stats.entries['clientside.totConns']['value'],
                'bytes_in': stats.entries['clientside.bitsIn']['value'],
                'bytes_out': stats.entries['clientside.bitsOut']['value']
            })
        return status
    except Exception as e:
        print(f"Failed to monitor virtual servers: {str(e)}")
        return None

def check_pool_health(mgmt):
    """Check health of all pools and their members"""
    try:
        pools = mgmt.tm.ltm.pools.get_collection()
        status = []
        for pool in pools:
            pool_stats = pool.stats.load()
            members = pool.members_s.get_collection()
            member_status = []
            
            for member in members:
                member_stats = member.stats.load()
                member_status.append({
                    'name': member.name,
                    'address': member.address,
                    'status': member_stats.entries['status.availabilityState']['description'],
                    'current_connections': member_stats.entries['serverside.curConns']['value']
                })
            
            status.append({
                'name': pool.name,
                'lb_method': pool.loadBalancingMode,
                'status': pool_stats.entries['status.availabilityState']['description'],
                'active_member_count': pool_stats.entries['activeMemberCnt']['value'],
                'members': member_status
            })
        return status
    except Exception as e:
        print(f"Failed to check pool health: {str(e)}")
        return None
```

## SSL Certificate Monitoring

```python
def monitor_ssl_certificates(mgmt):
    """Monitor SSL certificate expiration and status"""
    try:
        certs = mgmt.tm.sys.file.ssl_certs.get_collection()
        return [{
            'name': cert.name,
            'expires_on': cert.expiresOn,
            'issuer': cert.issuer,
            'subject': cert.subject,
            'bits_length': cert.bitsLength
        } for cert in certs]
    except Exception as e:
        print(f"Failed to monitor SSL certificates: {str(e)}")
        return None
```

## Comprehensive Health Check

```python
def comprehensive_health_check(mgmt):
    """Perform a comprehensive health check of the F5 device"""
    health_status = {
        'timestamp': datetime.now().isoformat(),
        'system': get_system_health(mgmt),
        'disk': monitor_disk_usage(mgmt),
        'gtm': {
            'wide_ips': monitor_gtm_wide_ips(mgmt),
            'datacenters': check_gtm_datacenter_status(mgmt)
        },
        'ltm': {
            'virtual_servers': monitor_virtual_servers(mgmt),
            'pools': check_pool_health(mgmt)
        },
        'ssl': monitor_ssl_certificates(mgmt)
    }
    
    return health_status

def save_health_report(health_status, filename=None):
    """Save health check results to a file"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'f5_health_report_{timestamp}.json'
    
    try:
        with open(filename, 'w') as f:
            json.dump(health_status, f, indent=2)
        print(f"Health report saved to: {filename}")
        return True
    except Exception as e:
        print(f"Failed to save health report: {str(e)}")
        return False
```

## Usage Example

```python
if __name__ == "__main__":
    # Connect to F5 device
    mgmt = ManagementRoot("f5-device.example.com", "admin", "password")
    
    # Perform comprehensive health check
    health_status = comprehensive_health_check(mgmt)
    
    # Save report
    save_health_report(health_status)
    
    # Print critical status
    if health_status:
        print("\nCritical Status Summary:")
        
        # System Health
        sys_health = health_status['system']
        print(f"\nSystem CPU Usage: {sys_health['cpu_usage'][0]['usage']}%")
        print(f"System Memory Used: {sys_health['memory_usage'][0]['used']} MB")
        
        # GTM Status
        gtm = health_status['gtm']
        print("\nGTM Status:")
        for dc in gtm['datacenters']:
            print(f"Datacenter {dc['name']}: {dc['status']}")
        
        # LTM Status
        ltm = health_status['ltm']
        print("\nLTM Status:")
        for vs in ltm['virtual_servers']:
            print(f"Virtual Server {vs['name']}: {vs['status']}")
        
        # SSL Certificates
        print("\nSSL Certificates:")
        for cert in health_status['ssl']:
            print(f"Certificate {cert['name']} expires on {cert['expires_on']}")
```

## Monitoring Best Practices

1. Regular Health Checks:
   - Schedule regular comprehensive health checks
   - Monitor system resources (CPU, memory, disk)
   - Track virtual server and pool performance
   - Monitor SSL certificate expiration

2. Alert Configuration:
   - Set up alerts for critical thresholds
   - Monitor pool member availability
   - Track connection limits
   - Watch for certificate expiration

3. Performance Monitoring:
   - Monitor throughput and latency
   - Track connection counts
   - Monitor pool member distribution
   - Watch for resource bottlenecks

4. Logging and Reporting:
   - Maintain historical health data
   - Generate regular status reports
   - Track long-term trends
   - Document incidents and resolutions

## Common Monitoring Issues

1. Resource Constraints:
   - High CPU usage
   - Memory exhaustion
   - Disk space limitations
   - Network bandwidth saturation

2. Availability Issues:
   - Pool member failures
   - Virtual server outages
   - Monitor timeouts
   - Connection problems

3. Certificate Issues:
   - Expiring certificates
   - Invalid certificates
   - Chain validation problems
   - Cipher suite mismatches

4. Performance Problems:
   - Slow response times
   - Connection queuing
   - Uneven load distribution
   - Resource contention
