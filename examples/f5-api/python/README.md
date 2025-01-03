# F5 API with Python Examples

## Table of Contents
- [F5 API with Python Examples](#f5-api-with-python-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Operations](#basic-operations)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Operations
   - Authentication and connection
   - Virtual server management
   - Pool management
   - Node management

2. Advanced Features
   - iRules management
   - SSL profile handling
   - Health monitoring
   - Traffic management

3. Integration Features
   - Load balancer automation
   - Configuration management
   - Monitoring integration
   - Backup operations

4. Full Applications
   - Load balancer dashboard
   - Configuration manager
   - Health monitor
   - Deployment automator

## Project Structure

```
python/
├── basic/
│   ├── connection/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── config.py
│   ├── virtual_servers/
│   ├── pools/
│   └── nodes/
├── advanced/
│   ├── irules/
│   ├── ssl_profiles/
│   ├── monitors/
│   └── traffic/
├── integration/
│   ├── automation/
│   ├── config_mgmt/
│   ├── monitoring/
│   └── backup/
└── applications/
    ├── lb_dashboard/
    ├── config_manager/
    ├── health_monitor/
    └── deploy_automator/
```

## Getting Started

1. Setup Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3. Configure F5 Connection:
```python
# config.py
F5_HOST = "https://your-f5-host"
F5_USERNAME = "admin"
F5_PASSWORD = "your-password"
F5_VERIFY_SSL = False  # Set to True in production
```

## Basic Operations

### Connection Management
```python
from f5.bigip import ManagementRoot
from config import *
import requests
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for development
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_f5_client():
    """Create authenticated F5 client"""
    try:
        mgmt = ManagementRoot(
            F5_HOST,
            F5_USERNAME,
            F5_PASSWORD,
            verify=F5_VERIFY_SSL
        )
        return mgmt
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        raise

def test_connection():
    """Test F5 connection"""
    try:
        mgmt = get_f5_client()
        version = mgmt.tmos_version
        print(f"Connected to F5 version: {version}")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
```

### Virtual Server Management
```python
class VirtualServerManager:
    def __init__(self):
        self.mgmt = get_f5_client()
    
    def create_virtual(self, name, destination, port, pool=None):
        """Create virtual server"""
        try:
            vs = self.mgmt.tm.ltm.virtuals.virtual.create(
                name=name,
                partition='Common',
                destination=f'/Common/{destination}:{port}',
                pool=f'/Common/{pool}' if pool else None,
                sourceAddressTranslation={'type': 'automap'},
                profiles=['/Common/tcp']
            )
            return vs
        except Exception as e:
            print(f"Failed to create virtual server: {str(e)}")
            raise
    
    def get_virtual(self, name):
        """Get virtual server by name"""
        try:
            return self.mgmt.tm.ltm.virtuals.virtual.load(
                name=name,
                partition='Common'
            )
        except Exception as e:
            print(f"Virtual server not found: {str(e)}")
            return None
    
    def update_virtual(self, name, **kwargs):
        """Update virtual server properties"""
        vs = self.get_virtual(name)
        if not vs:
            raise ValueError(f"Virtual server {name} not found")
        
        try:
            for key, value in kwargs.items():
                setattr(vs, key, value)
            vs.update()
            return vs
        except Exception as e:
            print(f"Failed to update virtual server: {str(e)}")
            raise
    
    def delete_virtual(self, name):
        """Delete virtual server"""
        vs = self.get_virtual(name)
        if not vs:
            raise ValueError(f"Virtual server {name} not found")
        
        try:
            vs.delete()
            return True
        except Exception as e:
            print(f"Failed to delete virtual server: {str(e)}")
            raise
```

### Pool Management
```python
class PoolManager:
    def __init__(self):
        self.mgmt = get_f5_client()
    
    def create_pool(self, name, lb_method='round-robin', monitor=None):
        """Create new pool"""
        try:
            pool = self.mgmt.tm.ltm.pools.pool.create(
                name=name,
                partition='Common',
                loadBalancingMode=lb_method,
                monitor=f'/Common/{monitor}' if monitor else 'none'
            )
            return pool
        except Exception as e:
            print(f"Failed to create pool: {str(e)}")
            raise
    
    def add_pool_member(self, pool_name, node_name, port):
        """Add member to pool"""
        pool = self.get_pool(pool_name)
        if not pool:
            raise ValueError(f"Pool {pool_name} not found")
        
        try:
            member = pool.members_s.members.create(
                name=f'{node_name}:{port}',
                partition='Common'
            )
            return member
        except Exception as e:
            print(f"Failed to add pool member: {str(e)}")
            raise
    
    def get_pool_status(self, name):
        """Get pool status and statistics"""
        pool = self.get_pool(name)
        if not pool:
            raise ValueError(f"Pool {name} not found")
        
        try:
            stats = pool.stats.load()
            return {
                'status': pool.availability_status,
                'current_connections': stats['serverside.curConns']['value'],
                'total_connections': stats['serverside.totConns']['value']
            }
        except Exception as e:
            print(f"Failed to get pool status: {str(e)}")
            raise
```

## Advanced Features

### iRules Management
```python
class iRuleManager:
    def __init__(self):
        self.mgmt = get_f5_client()
    
    def create_irule(self, name, content):
        """Create new iRule"""
        try:
            irule = self.mgmt.tm.ltm.rules.rule.create(
                name=name,
                partition='Common',
                apiAnonymous=content
            )
            return irule
        except Exception as e:
            print(f"Failed to create iRule: {str(e)}")
            raise
    
    def attach_irule_to_virtual(self, irule_name, virtual_name):
        """Attach iRule to virtual server"""
        vs = self.get_virtual(virtual_name)
        if not vs:
            raise ValueError(f"Virtual server {virtual_name} not found")
        
        try:
            rules = vs.rules
            if not rules:
                rules = []
            rules.append(f'/Common/{irule_name}')
            vs.rules = rules
            vs.update()
            return True
        except Exception as e:
            print(f"Failed to attach iRule: {str(e)}")
            raise
```

### SSL Profile Management
```python
class SSLProfileManager:
    def __init__(self):
        self.mgmt = get_f5_client()
    
    def create_client_ssl_profile(self, name, cert, key, chain=None):
        """Create client SSL profile"""
        try:
            profile = self.mgmt.tm.ltm.profile.client_ssls.client_ssl.create(
                name=name,
                partition='Common',
                cert=f'/Common/{cert}',
                key=f'/Common/{key}',
                chain=f'/Common/{chain}' if chain else None
            )
            return profile
        except Exception as e:
            print(f"Failed to create SSL profile: {str(e)}")
            raise
    
    def update_ssl_profile(self, name, **kwargs):
        """Update SSL profile properties"""
        profile = self.get_ssl_profile(name)
        if not profile:
            raise ValueError(f"SSL profile {name} not found")
        
        try:
            for key, value in kwargs.items():
                setattr(profile, key, value)
            profile.update()
            return profile
        except Exception as e:
            print(f"Failed to update SSL profile: {str(e)}")
            raise
```

## Security Considerations

1. Certificate Management:
```python
class CertificateManager:
    def __init__(self):
        self.mgmt = get_f5_client()
    
    def install_certificate(self, name, cert_content):
        """Install SSL certificate"""
        try:
            cert = self.mgmt.tm.sys.crypto.certs.cert.create(
                name=name,
                partition='Common',
                fromLocalFile=cert_content
            )
            return cert
        except Exception as e:
            print(f"Failed to install certificate: {str(e)}")
            raise
    
    def install_key(self, name, key_content):
        """Install SSL private key"""
        try:
            key = self.mgmt.tm.sys.crypto.keys.key.create(
                name=name,
                partition='Common',
                fromLocalFile=key_content
            )
            return key
        except Exception as e:
            print(f"Failed to install key: {str(e)}")
            raise
```

2. Access Control:
```python
class AccessManager:
    def __init__(self):
        self.mgmt = get_f5_client()
    
    def create_access_policy(self, name, rules):
        """Create access policy"""
        try:
            policy = self.mgmt.tm.apm.policy.access_policy.create(
                name=name,
                partition='Common',
                rules=rules
            )
            return policy
        except Exception as e:
            print(f"Failed to create access policy: {str(e)}")
            raise
```

## Performance Optimization

1. Connection Handling:
```python
class ConnectionOptimizer:
    def __init__(self):
        self.mgmt = get_f5_client()
    
    def optimize_virtual_server(self, name):
        """Apply performance optimizations to virtual server"""
        vs = self.get_virtual(name)
        if not vs:
            raise ValueError(f"Virtual server {name} not found")
        
        try:
            # Apply optimizations
            vs.update(
                profiles=[
                    {'name': 'tcp-wan-optimized'},
                    {'name': 'http-acceleration'}
                ],
                rateLimitMode='object',
                maxConnections=10000
            )
            return vs
        except Exception as e:
            print(f"Failed to optimize virtual server: {str(e)}")
            raise
```

2. Monitoring:
```python
class PerformanceMonitor:
    def __init__(self):
        self.mgmt = get_f5_client()
    
    def get_virtual_stats(self, name):
        """Get virtual server statistics"""
        vs = self.get_virtual(name)
        if not vs:
            raise ValueError(f"Virtual server {name} not found")
        
        try:
            stats = vs.stats.load()
            return {
                'current_connections': stats['clientside.curConns']['value'],
                'total_connections': stats['clientside.totConns']['value'],
                'bytes_in': stats['clientside.bitsIn']['value'],
                'bytes_out': stats['clientside.bitsOut']['value']
            }
        except Exception as e:
            print(f"Failed to get statistics: {str(e)}")
            raise
```

## Testing

1. Unit Tests:
```python
import unittest
from unittest.mock import patch

class F5Tests(unittest.TestCase):
    def setUp(self):
        self.mgmt = get_f5_client()
    
    def test_virtual_server_creation(self):
        manager = VirtualServerManager()
        result = manager.create_virtual(
            'test_virtual',
            '192.168.1.10',
            80
        )
        self.assertIsNotNone(result)
    
    def test_pool_operations(self):
        manager = PoolManager()
        
        # Create pool
        pool = manager.create_pool('test_pool')
        
        # Add member
        member = manager.add_pool_member(
            'test_pool',
            '192.168.1.20',
            80
        )
        
        # Verify status
        status = manager.get_pool_status('test_pool')
        self.assertEqual(status['status'], 'available')
```

2. Integration Tests:
```python
class F5IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.mgmt = get_f5_client()
        self.vs_manager = VirtualServerManager()
        self.pool_manager = PoolManager()
    
    def test_load_balancing_workflow(self):
        # Create pool
        pool = self.pool_manager.create_pool('integration_pool')
        
        # Add members
        self.pool_manager.add_pool_member(
            'integration_pool',
            '192.168.1.21',
            80
        )
        self.pool_manager.add_pool_member(
            'integration_pool',
            '192.168.1.22',
            80
        )
        
        # Create virtual server
        vs = self.vs_manager.create_virtual(
            'integration_vs',
            '192.168.1.100',
            80,
            'integration_pool'
        )
        
        # Verify configuration
        self.assertEqual(vs.pool, '/Common/integration_pool')
        
        # Clean up
        self.vs_manager.delete_virtual('integration_vs')
        self.pool_manager.delete_pool('integration_pool')
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
