"""
Network Metrics Collectors
------------------------
Classes and functions for collecting metrics from network devices.
"""

import time
from typing import Dict, List, Optional
import requests
from requests.exceptions import RequestException
import psutil

class NetworkMetricsCollector:
    """Collects metrics from network devices."""
    
    def __init__(self, devices: List[str]):
        """Initialize collector with list of devices."""
        self.devices = devices
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for example
    
    def check_device_status(self, device: str) -> bool:
        """Check if device is accessible."""
        try:
            response = self.session.get(
                f"https://{device}/api/v1/system/status",
                timeout=5
            )
            return response.ok
        except RequestException:
            return False
    
    def collect_system_metrics(self, device: str) -> Dict:
        """Collect system metrics from device."""
        try:
            response = self.session.get(
                f"https://{device}/api/v1/system/metrics",
                timeout=10
            )
            if response.ok:
                data = response.json()
                return {
                    'cpu_percent': data.get('cpu_utilization', 0),
                    'memory_percent': data.get('memory_utilization', 0),
                    'uptime': data.get('uptime', 0),
                    'temperature': data.get('temperature', 0),
                    'timestamp': time.time()
                }
        except RequestException:
            pass
        
        # Return empty metrics if collection fails
        return {
            'cpu_percent': 0,
            'memory_percent': 0,
            'uptime': 0,
            'temperature': 0,
            'timestamp': time.time()
        }
    
    def collect_interface_metrics(self, device: str) -> Dict:
        """Collect interface metrics from device."""
        try:
            response = self.session.get(
                f"https://{device}/api/v1/interfaces/metrics",
                timeout=10
            )
            if response.ok:
                return response.json()
        except RequestException:
            pass
        
        return {}
    
    def collect_all_metrics(self) -> Dict:
        """Collect all metrics from all devices."""
        metrics = {}
        
        for device in self.devices:
            metrics[device] = {
                'status': self.check_device_status(device),
                'system': self.collect_system_metrics(device),
                'interfaces': self.collect_interface_metrics(device),
                'timestamp': time.time()
            }
        
        return metrics

class LocalSystemCollector:
    """Collects metrics from local system."""
    
    @staticmethod
    def get_cpu_metrics() -> Dict:
        """Get CPU usage metrics."""
        return {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
            'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
            'timestamp': time.time()
        }
    
    @staticmethod
    def get_memory_metrics() -> Dict:
        """Get memory usage metrics."""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free,
            'timestamp': time.time()
        }
    
    @staticmethod
    def get_network_metrics() -> Dict:
        """Get network interface metrics."""
        interfaces = {}
        
        for name, stats in psutil.net_io_counters(pernic=True).items():
            interfaces[name] = {
                'bytes_sent': stats.bytes_sent,
                'bytes_recv': stats.bytes_recv,
                'packets_sent': stats.packets_sent,
                'packets_recv': stats.packets_recv,
                'errors_in': stats.errin,
                'errors_out': stats.errout,
                'timestamp': time.time()
            }
        
        return interfaces
    
    @classmethod
    def collect_all_metrics(cls) -> Dict:
        """Collect all local system metrics."""
        return {
            'cpu': cls.get_cpu_metrics(),
            'memory': cls.get_memory_metrics(),
            'network': cls.get_network_metrics(),
            'timestamp': time.time()
        }

def get_collector(collector_type: str, **kwargs) -> object:
    """Factory function to get appropriate collector."""
    collectors = {
        'network': NetworkMetricsCollector,
        'local': LocalSystemCollector
    }
    
    if collector_type not in collectors:
        raise ValueError(f"Unknown collector type: {collector_type}")
    
    return collectors[collector_type](**kwargs)
