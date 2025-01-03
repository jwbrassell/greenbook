# Getting Started with Network Automation

## Table of Contents
1. [Introduction](#introduction)
2. [Basic Setup](#basic-setup)
3. [First Automation Script](#first-automation-script)
4. [Common Tools](#common-tools)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Introduction
Network automation helps network engineers and administrators automate repetitive tasks, reduce errors, and manage network infrastructure more efficiently. This guide will help you get started with the basic concepts and tools.

### Why Automate?
- Eliminate repetitive manual tasks
- Reduce human error
- Ensure consistent configuration
- Enable rapid deployment
- Improve documentation

## Basic Setup

### Python Environment Setup
```bash
# Create virtual environment
python -m venv network_automation
source network_automation/bin/activate  # Linux/Mac
# or
.\network_automation\Scripts\activate    # Windows

# Install required packages
pip install -r requirements.txt
```

### Required Packages
Create a `requirements.txt` file with these dependencies:
```
netmiko>=4.1.0
paramiko>=3.0.0
requests>=2.28.0
pyyaml>=6.0
flask>=2.0.0
python-dotenv>=0.19.0
```

### Development Tools
1. Visual Studio Code or PyCharm
2. Git for version control
3. Postman for API testing
4. Network device emulator (GNS3 or EVE-NG)

## First Automation Script
Let's create a simple script to connect to a network device and retrieve its configuration:

```python
from netmiko import ConnectHandler
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_device_config(hostname, device_type="cisco_ios"):
    """
    Retrieve configuration from a network device.
    
    Args:
        hostname (str): Device hostname or IP
        device_type (str): Type of device (default: cisco_ios)
        
    Returns:
        str: Device configuration
    """
    device = {
        "device_type": device_type,
        "host": hostname,
        "username": os.getenv("NETWORK_USER"),
        "password": os.getenv("NETWORK_PASSWORD"),
        "secret": os.getenv("NETWORK_ENABLE")
    }
    
    try:
        # Connect to device
        with ConnectHandler(**device) as net_connect:
            # Enter enable mode if required
            net_connect.enable()
            
            # Get configuration
            config = net_connect.send_command("show running-config")
            return config
            
    except Exception as e:
        print(f"Error connecting to {hostname}: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    device_ip = "192.168.1.1"
    config = get_device_config(device_ip)
    
    if config:
        # Save configuration to file
        with open(f"{device_ip}_config.txt", "w") as f:
            f.write(config)
        print(f"Configuration saved to {device_ip}_config.txt")
```

### Environment Setup
Create a `.env` file:
```
NETWORK_USER=admin
NETWORK_PASSWORD=your_password
NETWORK_ENABLE=enable_password
```

## Common Tools
1. **Netmiko**
   - SSH connection handling
   - Multi-vendor support
   - Command automation

2. **Paramiko**
   - Low-level SSH implementation
   - Custom SSH solutions
   - Secure file transfers

3. **Requests**
   - REST API interactions
   - HTTP/HTTPS communication
   - API authentication

4. **PyYAML**
   - Configuration file parsing
   - Data structure serialization
   - Template processing

## Best Practices
1. **Security**
   - Never hardcode credentials
   - Use environment variables
   - Implement proper error handling
   - Validate input data

2. **Code Organization**
   - Use functions for reusability
   - Implement proper logging
   - Add meaningful comments
   - Follow PEP 8 style guide

3. **Version Control**
   - Use Git for code management
   - Create meaningful commits
   - Document changes properly
   - Use branches for features

4. **Testing**
   - Test in lab environment first
   - Implement error handling
   - Create backup configurations
   - Validate changes

## Troubleshooting
### Common Issues
1. **Connection Problems**
   - Check network connectivity
   - Verify credentials
   - Confirm device accessibility
   - Check SSH/API settings

2. **Authentication Errors**
   - Verify username/password
   - Check enable password
   - Confirm API tokens
   - Review access rights

3. **Script Errors**
   - Check Python version
   - Verify package versions
   - Review error messages
   - Check syntax

### Debugging Tips
- Enable verbose logging
- Use print statements
- Check device logs
- Test in isolation

## Next Steps
1. Explore more complex automation scenarios
2. Learn about network APIs
3. Build web interfaces with Flask
4. Implement configuration management
5. Create automated testing

## Related Resources
- [Python for Network Engineers](https://pynet.twb-tech.com/)
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [Network Automation Forums](https://networktocode.com/community/)
- [API Development Guide](../03-api-development.md)
