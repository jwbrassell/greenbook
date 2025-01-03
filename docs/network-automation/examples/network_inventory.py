#!/usr/bin/env python3
"""
Network Inventory Example
------------------------
This script demonstrates how to collect and manage network device inventory
using the concepts covered in the documentation.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class NetworkDevice:
    """Represents a network device with API capabilities."""
    
    def __init__(self, hostname: str, device_type: str):
        self.hostname = hostname
        self.device_type = device_type
        self.auth = (
            os.getenv('NETWORK_USER', ''),
            os.getenv('NETWORK_PASSWORD', '')
        )
        self.base_url = f"https://{hostname}/api/v1"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for example
        
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make an API request to the device."""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                auth=self.auth,
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {self.hostname}: {str(e)}")
            return None
    
    def get_system_info(self) -> Optional[Dict]:
        """Get basic system information."""
        return self._make_request('GET', 'system')
    
    def get_interfaces(self) -> Optional[Dict]:
        """Get interface information."""
        return self._make_request('GET', 'interfaces')
    
    def get_inventory(self) -> Optional[Dict]:
        """Collect complete device inventory."""
        system_info = self.get_system_info()
        interfaces = self.get_interfaces()
        
        if system_info and interfaces:
            return {
                'hostname': self.hostname,
                'device_type': self.device_type,
                'system': system_info,
                'interfaces': interfaces,
                'collected_at': datetime.now().isoformat()
            }
        return None

class NetworkInventory:
    """Manages inventory collection for multiple devices."""
    
    def __init__(self, devices_file: str):
        self.devices_file = devices_file
        self.devices: List[NetworkDevice] = []
        self.load_devices()
    
    def load_devices(self):
        """Load device list from JSON file."""
        try:
            with open(self.devices_file, 'r') as f:
                devices_data = json.load(f)
                
            self.devices = [
                NetworkDevice(
                    hostname=device['hostname'],
                    device_type=device['type']
                )
                for device in devices_data
            ]
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load devices file: {str(e)}")
            self.devices = []
    
    def collect_inventory(self, output_file: str):
        """Collect inventory from all devices."""
        inventory = []
        
        for device in self.devices:
            logger.info(f"Collecting inventory from {device.hostname}")
            device_inventory = device.get_inventory()
            
            if device_inventory:
                inventory.append(device_inventory)
            else:
                logger.warning(f"Failed to collect inventory from {device.hostname}")
        
        # Save inventory to file
        try:
            with open(output_file, 'w') as f:
                json.dump(inventory, f, indent=2)
            logger.info(f"Inventory saved to {output_file}")
            
        except IOError as e:
            logger.error(f"Failed to save inventory: {str(e)}")

def main():
    """Main execution function."""
    # Example devices file structure:
    # [
    #     {"hostname": "switch1.example.com", "type": "cisco_ios"},
    #     {"hostname": "router1.example.com", "type": "cisco_ios_xe"}
    # ]
    
    devices_file = 'devices.json'
    output_file = f"network_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Create inventory manager and collect data
    inventory_manager = NetworkInventory(devices_file)
    inventory_manager.collect_inventory(output_file)

if __name__ == '__main__':
    # Suppress InsecureRequestWarning for example
    requests.packages.urllib3.disable_warnings()
    main()
