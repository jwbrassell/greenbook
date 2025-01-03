# Network Automation Examples

This directory contains practical examples demonstrating the concepts covered in the network automation documentation.

## Network Inventory Script

The `network_inventory.py` script demonstrates how to collect and manage network device inventory using REST APIs. It shows best practices for:

- Object-oriented design
- Error handling
- Configuration management
- API interaction
- Logging
- Type hints
- Environment variable usage

### Prerequisites

1. Python 3.7+
2. Required packages:
   ```
   requests
   python-dotenv
   ```

### Setup

1. Create a `.env` file with your credentials:
   ```
   NETWORK_USER=your_username
   NETWORK_PASSWORD=your_password
   ```

2. Update `devices.json` with your network devices:
   ```json
   {
     "devices": [
       {
         "hostname": "device1.example.com",
         "type": "cisco_ios",
         "description": "Core Switch 1",
         "location": "Data Center"
       }
     ]
   }
   ```

### Usage

Run the inventory script:
```bash
python network_inventory.py
```

The script will:
1. Load device information from devices.json
2. Connect to each device via its API
3. Collect system and interface information
4. Save the inventory to a timestamped JSON file

### Output

The script generates a JSON file with the following structure:
```json
[
  {
    "hostname": "switch1.example.com",
    "device_type": "cisco_ios",
    "system": {
      "model": "C9300-48P",
      "serial": "FCW2123L0R3",
      "version": "17.3.1"
    },
    "interfaces": {
      "GigabitEthernet1/0/1": {
        "status": "up",
        "description": "Server1",
        "vlan": 10
      }
    },
    "collected_at": "2023-12-20T14:30:00"
  }
]
```

### Error Handling

The script includes comprehensive error handling for:
- API connection failures
- Authentication errors
- Invalid device configurations
- File I/O errors

Errors are logged with appropriate severity levels and helpful messages.

### Customization

You can extend the script by:
1. Adding new device types
2. Collecting additional information
3. Implementing different output formats
4. Adding custom error handling
5. Implementing parallel collection

### Security Notes

1. Never commit `.env` files with real credentials
2. Use environment variables for sensitive data
3. Implement proper SSL verification in production
4. Follow the principle of least privilege
5. Regularly rotate credentials

## Contributing

To contribute examples:
1. Follow the existing code style
2. Include comprehensive documentation
3. Add error handling
4. Include sample configurations
5. Test thoroughly

## Related Documentation

- [Getting Started Guide](../01-getting-started.md)
- [Working with APIs](../02-working-with-apis.md)
- [Network Device APIs](../network-device-apis.md)
