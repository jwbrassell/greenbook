# F5 Data Center Operations Guide

## Table of Contents
- [F5 Data Center Operations Guide](#f5-data-center-operations-guide)
  - [Data Center Management](#data-center-management)
  - [Data Center Server Management](#data-center-server-management)
  - [Data Center Health Monitoring](#data-center-health-monitoring)
  - [Data Center Load Balancing](#data-center-load-balancing)
  - [Data Center Maintenance](#data-center-maintenance)
  - [Usage Examples](#usage-examples)
  - [Best Practices](#best-practices)
  - [Common Issues and Solutions](#common-issues-and-solutions)



This guide covers managing F5 data centers, including creation, configuration, monitoring, and maintenance operations.

## Data Center Management

```python
from f5.bigip import ManagementRoot
from typing import Dict, List, Optional
import json

def create_datacenter(mgmt, name: str, location: str = None, 
                     contact: str = None, description: str = None):
    """
    Create a new data center
    
    Args:
        mgmt: F5 management connection
        name: Name of the data center
        location: Physical location of the data center
        contact: Contact information for the data center
        description: Description of the data center
    """
    try:
        dc = mgmt.tm.gtm.datacenters.datacenter.create(
            name=name,
            partition='Common',
            location=location,
            contact=contact,
            description=description
        )
        print(f"Created datacenter: {name}")
        return dc
    except Exception as e:
        print(f"Failed to create datacenter: {str(e)}")
        return None

def modify_datacenter(mgmt, name: str, **kwargs):
    """Modify data center properties"""
    try:
        dc = mgmt.tm.gtm.datacenters.datacenter.load(
            name=name,
            partition='Common'
        )
        dc.modify(**kwargs)
        print(f"Modified datacenter: {name}")
        return True
    except Exception as e:
        print(f"Failed to modify datacenter: {str(e)}")
        return False

def delete_datacenter(mgmt, name: str):
    """Delete a data center"""
    try:
        dc = mgmt.tm.gtm.datacenters.datacenter.load(
            name=name,
            partition='Common'
        )
        dc.delete()
        print(f"Deleted datacenter: {name}")
        return True
    except Exception as e:
        print(f"Failed to delete datacenter: {str(e)}")
        return False
```

## Data Center Server Management

```python
def add_server_to_datacenter(mgmt, dc_name: str, server_name: str, 
                           server_addresses: List[str], 
                           monitor: str = '/Common/bigip'):
    """Add a server to a data center"""
    try:
        server = mgmt.tm.gtm.servers.server.create(
            name=server_name,
            partition='Common',
            datacenter=f'/Common/{dc_name}',
            addresses=[{'name': addr} for addr in server_addresses],
            monitor=monitor
        )
        print(f"Added server {server_name} to datacenter {dc_name}")
        return server
    except Exception as e:
        print(f"Failed to add server: {str(e)}")
        return None

def get_datacenter_servers(mgmt, dc_name: str):
    """Get all servers in a data center"""
    try:
        servers = mgmt.tm.gtm.servers.get_collection()
        dc_servers = [
            {
                'name': server.name,
                'addresses': [addr['name'] for addr in server.addresses],
                'monitor': getattr(server, 'monitor', None),
                'enabled': getattr(server, 'enabled', True)
            }
            for server in servers
            if getattr(server, 'datacenter', '').endswith(f'/{dc_name}')
        ]
        return dc_servers
    except Exception as e:
        print(f"Failed to get datacenter servers: {str(e)}")
        return None
```

## Data Center Health Monitoring

```python
def configure_datacenter_monitor(mgmt, dc_name: str, 
                               probe_interval: int = 60,
                               probe_timeout: int = 120,
                               probe_attempts: int = 3):
    """Configure monitoring settings for a data center"""
    try:
        dc = mgmt.tm.gtm.datacenters.datacenter.load(
            name=dc_name,
            partition='Common'
        )
        dc.modify(
            probeInterval=probe_interval,
            probeTimeout=probe_timeout,
            probeAttempts=probe_attempts
        )
        print(f"Configured monitoring for datacenter: {dc_name}")
        return True
    except Exception as e:
        print(f"Failed to configure monitoring: {str(e)}")
        return False

def get_datacenter_health(mgmt, dc_name: str):
    """Get health status of a data center"""
    try:
        dc = mgmt.tm.gtm.datacenters.datacenter.load(
            name=dc_name,
            partition='Common'
        )
        servers = get_datacenter_servers(mgmt, dc_name)
        
        # Get server statuses
        server_status = []
        for server in servers:
            server_obj = mgmt.tm.gtm.servers.server.load(
                name=server['name'],
                partition='Common'
            )
            stats = server_obj.stats.load()
            server_status.append({
                'name': server['name'],
                'status': stats.entries['status.availabilityState']['description'],
                'enabled': server['enabled']
            })
        
        return {
            'name': dc_name,
            'enabled': getattr(dc, 'enabled', True),
            'status': getattr(dc, 'status', 'unknown'),
            'servers': server_status
        }
    except Exception as e:
        print(f"Failed to get datacenter health: {str(e)}")
        return None
```

## Data Center Load Balancing

```python
def configure_datacenter_load_balancing(mgmt, dc_name: str, 
                                      weight: int = 100,
                                      ratio: int = 1):
    """Configure load balancing settings for a data center"""
    try:
        dc = mgmt.tm.gtm.datacenters.datacenter.load(
            name=dc_name,
            partition='Common'
        )
        dc.modify(
            enabled=True,
            loadBalancingWeight=weight,
            ratio=ratio
        )
        print(f"Configured load balancing for datacenter: {dc_name}")
        return True
    except Exception as e:
        print(f"Failed to configure load balancing: {str(e)}")
        return False

def set_datacenter_failover(mgmt, primary_dc: str, backup_dc: str):
    """Configure failover between data centers"""
    try:
        # Set primary datacenter
        primary = mgmt.tm.gtm.datacenters.datacenter.load(
            name=primary_dc,
            partition='Common'
        )
        primary.modify(enabled=True)
        
        # Set backup datacenter
        backup = mgmt.tm.gtm.datacenters.datacenter.load(
            name=backup_dc,
            partition='Common'
        )
        backup.modify(
            enabled=True,
            failoverOrder=1  # Higher number means lower priority
        )
        
        print(f"Configured failover: {primary_dc} -> {backup_dc}")
        return True
    except Exception as e:
        print(f"Failed to configure failover: {str(e)}")
        return False
```

## Data Center Maintenance

```python
def enable_maintenance_mode(mgmt, dc_name: str):
    """Enable maintenance mode for a data center"""
    try:
        dc = mgmt.tm.gtm.datacenters.datacenter.load(
            name=dc_name,
            partition='Common'
        )
        # Disable new connections but maintain existing ones
        dc.modify(
            enabled=False,
            disableMode='maintenance'
        )
        print(f"Enabled maintenance mode for datacenter: {dc_name}")
        return True
    except Exception as e:
        print(f"Failed to enable maintenance mode: {str(e)}")
        return False

def backup_datacenter_config(mgmt, dc_name: str, filename: str = None):
    """Backup data center configuration"""
    try:
        dc = mgmt.tm.gtm.datacenters.datacenter.load(
            name=dc_name,
            partition='Common'
        )
        servers = get_datacenter_servers(mgmt, dc_name)
        
        config = {
            'datacenter': {
                'name': dc.name,
                'location': getattr(dc, 'location', None),
                'contact': getattr(dc, 'contact', None),
                'description': getattr(dc, 'description', None),
                'enabled': getattr(dc, 'enabled', True),
                'probeInterval': getattr(dc, 'probeInterval', 60),
                'probeTimeout': getattr(dc, 'probeTimeout', 120),
                'probeAttempts': getattr(dc, 'probeAttempts', 3)
            },
            'servers': servers
        }
        
        if not filename:
            filename = f"dc_{dc_name}_backup.json"
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Backed up datacenter configuration to: {filename}")
        return True
    except Exception as e:
        print(f"Failed to backup configuration: {str(e)}")
        return False
```

## Usage Examples

```python
if __name__ == "__main__":
    # Connect to F5 device
    mgmt = ManagementRoot("f5-device.example.com", "admin", "password")
    
    # Create a new data center
    dc = create_datacenter(
        mgmt,
        "DC1",
        location="New York",
        contact="admin@example.com",
        description="Primary data center"
    )
    
    # Add servers to the data center
    servers = [
        {
            'name': 'server1',
            'addresses': ['10.0.0.1', '10.0.0.2']
        },
        {
            'name': 'server2',
            'addresses': ['10.0.1.1', '10.0.1.2']
        }
    ]
    
    for server in servers:
        add_server_to_datacenter(
            mgmt,
            "DC1",
            server['name'],
            server['addresses']
        )
    
    # Configure monitoring
    configure_datacenter_monitor(
        mgmt,
        "DC1",
        probe_interval=30,
        probe_timeout=90,
        probe_attempts=3
    )
    
    # Configure load balancing
    configure_datacenter_load_balancing(
        mgmt,
        "DC1",
        weight=100,
        ratio=1
    )
    
    # Get health status
    health = get_datacenter_health(mgmt, "DC1")
    print(json.dumps(health, indent=2))
    
    # Backup configuration
    backup_datacenter_config(mgmt, "DC1")
```

## Best Practices

1. Data Center Management:
   - Use meaningful names and descriptions
   - Document physical locations and contacts
   - Implement proper monitoring
   - Regular configuration backups

2. Server Management:
   - Group servers logically
   - Monitor server health
   - Configure appropriate monitors
   - Regular maintenance windows

3. Load Balancing:
   - Configure appropriate weights
   - Implement proper failover
   - Test failover scenarios
   - Monitor traffic distribution

4. Maintenance:
   - Schedule maintenance windows
   - Use maintenance mode
   - Regular health checks
   - Document all changes

## Common Issues and Solutions

1. Connectivity Issues:
   - Check network connectivity
   - Verify server addresses
   - Review monitor settings
   - Check firewall rules

2. Performance Issues:
   - Monitor server loads
   - Review load balancing settings
   - Check resource utilization
   - Optimize monitor intervals

3. Configuration Issues:
   - Validate server configurations
   - Check monitor settings
   - Verify failover settings
   - Review backup configurations
