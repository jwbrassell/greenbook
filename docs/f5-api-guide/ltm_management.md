# F5 LTM (Local Traffic Manager) Management

## Table of Contents
- [F5 LTM (Local Traffic Manager) Management](#f5-ltm-local-traffic-manager-management)
  - [Virtual Server Management](#virtual-server-management)
  - [Pool and Node Management](#pool-and-node-management)
  - [Health Monitoring](#health-monitoring)
  - [SSL Profile Management](#ssl-profile-management)
  - [iRules Management](#irules-management)
  - [Usage Examples](#usage-examples)
- [Example usage of LTM management functions](#example-usage-of-ltm-management-functions)
  - [Best Practices](#best-practices)
  - [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)



This guide covers managing F5 LTM instances, including virtual servers, pools, nodes, and health monitors.

## Virtual Server Management

```python
from f5.bigip import ManagementRoot

def create_virtual_server(mgmt, name, destination, port=80, pool=None, 
                         protocol="tcp", profiles=None):
    """Create a virtual server"""
    try:
        vs = mgmt.tm.ltm.virtuals.virtual.create(
            name=name,
            partition='Common',
            destination=f'/Common/{destination}:{port}',
            pool=f'/Common/{pool}' if pool else None,
            ipProtocol=protocol,
            profiles=profiles or ['/Common/tcp']
        )
        print(f"Created virtual server: {name}")
        return vs
    except Exception as e:
        print(f"Failed to create virtual server: {str(e)}")
        return None

def get_virtual_server_stats(mgmt, name):
    """Get statistics for a virtual server"""
    try:
        vs = mgmt.tm.ltm.virtuals.virtual.load(name=name, partition='Common')
        stats = vs.stats.load()
        return {
            'name': name,
            'status': stats.entries['status.availabilityState']['description'],
            'current_connections': stats.entries['clientside.curConns']['value'],
            'total_connections': stats.entries['clientside.totConns']['value'],
            'bytes_in': stats.entries['clientside.bitsIn']['value'],
            'bytes_out': stats.entries['clientside.bitsOut']['value']
        }
    except Exception as e:
        print(f"Failed to get virtual server stats: {str(e)}")
        return None
```

## Pool and Node Management

```python
def create_ltm_pool(mgmt, name, lb_method='round-robin', monitor=None):
    """Create an LTM pool"""
    try:
        pool = mgmt.tm.ltm.pools.pool.create(
            name=name,
            partition='Common',
            loadBalancingMode=lb_method,
            monitor=f'/Common/{monitor}' if monitor else 'none'
        )
        print(f"Created LTM pool: {name}")
        return pool
    except Exception as e:
        print(f"Failed to create LTM pool: {str(e)}")
        return None

def add_pool_member(mgmt, pool_name, node_name, port=80):
    """Add a member to an LTM pool"""
    try:
        pool = mgmt.tm.ltm.pools.pool.load(name=pool_name, partition='Common')
        member = pool.members_s.members.create(
            name=f'{node_name}:{port}',
            partition='Common'
        )
        print(f"Added member {node_name}:{port} to pool {pool_name}")
        return member
    except Exception as e:
        print(f"Failed to add pool member: {str(e)}")
        return None

def create_node(mgmt, name, address):
    """Create a node"""
    try:
        node = mgmt.tm.ltm.nodes.node.create(
            name=name,
            partition='Common',
            address=address
        )
        print(f"Created node: {name}")
        return node
    except Exception as e:
        print(f"Failed to create node: {str(e)}")
        return None
```

## Health Monitoring

```python
def create_http_monitor(mgmt, name, send_string="GET /\r\n", 
                       receive_string="", interval=5, timeout=16):
    """Create an HTTP monitor"""
    try:
        monitor = mgmt.tm.ltm.monitor.https.http.create(
            name=name,
            partition='Common',
            send=send_string,
            recv=receive_string,
            interval=interval,
            timeout=timeout
        )
        print(f"Created HTTP monitor: {name}")
        return monitor
    except Exception as e:
        print(f"Failed to create HTTP monitor: {str(e)}")
        return None

def get_pool_member_status(mgmt, pool_name):
    """Get status of all members in a pool"""
    try:
        pool = mgmt.tm.ltm.pools.pool.load(name=pool_name, partition='Common')
        members = pool.members_s.get_collection()
        status = []
        for member in members:
            member_stats = member.stats.load()
            status.append({
                'name': member.name,
                'status': member_stats.entries['status.availabilityState']['description'],
                'current_connections': member_stats.entries['serverside.curConns']['value'],
                'total_connections': member_stats.entries['serverside.totConns']['value']
            })
        return status
    except Exception as e:
        print(f"Failed to get pool member status: {str(e)}")
        return None
```

## SSL Profile Management

```python
def create_ssl_profile(mgmt, name, cert_name, key_name):
    """Create an SSL profile"""
    try:
        profile = mgmt.tm.ltm.profile.client_ssls.client_ssl.create(
            name=name,
            partition='Common',
            cert=f'/Common/{cert_name}',
            key=f'/Common/{key_name}'
        )
        print(f"Created SSL profile: {name}")
        return profile
    except Exception as e:
        print(f"Failed to create SSL profile: {str(e)}")
        return None

def upload_ssl_cert(mgmt, cert_name, cert_content):
    """Upload an SSL certificate"""
    try:
        mgmt.shared.file_transfer.uploads.upload_bytes(
            cert_content.encode(),
            f'/var/config/rest/downloads/{cert_name}'
        )
        cert = mgmt.tm.sys.file.ssl_certs.ssl_cert.create(
            name=cert_name,
            partition='Common',
            sourcePath=f'/var/config/rest/downloads/{cert_name}'
        )
        print(f"Uploaded certificate: {cert_name}")
        return cert
    except Exception as e:
        print(f"Failed to upload certificate: {str(e)}")
        return None
```

## iRules Management

```python
def create_irule(mgmt, name, rule_content):
    """Create an iRule"""
    try:
        irule = mgmt.tm.ltm.rules.rule.create(
            name=name,
            partition='Common',
            apiAnonymous=rule_content
        )
        print(f"Created iRule: {name}")
        return irule
    except Exception as e:
        print(f"Failed to create iRule: {str(e)}")
        return None

def attach_irule_to_virtual(mgmt, vs_name, irule_name):
    """Attach an iRule to a virtual server"""
    try:
        vs = mgmt.tm.ltm.virtuals.virtual.load(name=vs_name, partition='Common')
        vs.modify(rules=[f'/Common/{irule_name}'])
        print(f"Attached iRule {irule_name} to virtual server {vs_name}")
        return True
    except Exception as e:
        print(f"Failed to attach iRule: {str(e)}")
        return False
```

## Usage Examples

```python
# Example usage of LTM management functions
if __name__ == "__main__":
    # Connect to F5 device
    mgmt = ManagementRoot("f5-device.example.com", "admin", "password")
    
    # Create HTTP monitor
    monitor = create_http_monitor(
        mgmt,
        "web_monitor",
        send_string="GET /health\r\n",
        receive_string="OK"
    )
    
    # Create nodes
    node1 = create_node(mgmt, "web1", "10.0.0.1")
    node2 = create_node(mgmt, "web2", "10.0.0.2")
    
    # Create pool and add members
    pool = create_ltm_pool(mgmt, "web_pool", monitor="web_monitor")
    add_pool_member(mgmt, "web_pool", "web1", 80)
    add_pool_member(mgmt, "web_pool", "web2", 80)
    
    # Create virtual server
    vs = create_virtual_server(
        mgmt,
        "web_vs",
        "192.0.2.10",
        port=80,
        pool="web_pool"
    )
    
    # Create and attach iRule
    irule_content = """
    when HTTP_REQUEST {
        if { [HTTP::uri] starts_with "/api" } {
            pool api_pool
        }
    }
    """
    irule = create_irule(mgmt, "api_routing", irule_content)
    attach_irule_to_virtual(mgmt, "web_vs", "api_routing")
    
    # Monitor status
    vs_stats = get_virtual_server_stats(mgmt, "web_vs")
    pool_status = get_pool_member_status(mgmt, "web_pool")
```

## Best Practices

1. Load Balancing:
   - Choose appropriate load balancing methods based on application needs
   - Monitor pool member health regularly
   - Set appropriate connection limits
   - Use session persistence when needed

2. SSL/TLS:
   - Keep certificates up to date
   - Use strong cipher suites
   - Implement proper certificate management
   - Consider using client SSL profiles

3. Monitoring:
   - Set appropriate monitor intervals
   - Use application-specific health checks
   - Monitor both pool members and virtual servers
   - Implement proper alerting

4. Security:
   - Use appropriate profiles
   - Implement rate limiting
   - Configure proper access controls
   - Regular security audits

## Common Issues and Troubleshooting

1. Connection Issues:
   - Check virtual server status
   - Verify pool member health
   - Review monitor configuration
   - Check network connectivity

2. Performance Issues:
   - Monitor connection counts
   - Check for resource constraints
   - Review pool member distribution
   - Analyze traffic patterns

3. SSL/TLS Issues:
   - Verify certificate validity
   - Check cipher suite compatibility
   - Review SSL profiles
   - Check client requirements
