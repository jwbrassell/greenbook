"""
Alert Management
--------------
Classes and functions for managing network monitoring alerts.
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import smtplib
from email.message import EmailMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AlertManager:
    """Manages system alerts and notifications."""
    
    def __init__(self):
        """Initialize alert manager with default thresholds."""
        self.thresholds = {
            'cpu_usage': float(os.getenv('ALERT_CPU_THRESHOLD', 80)),
            'memory_usage': float(os.getenv('ALERT_MEMORY_THRESHOLD', 90)),
            'interface_errors': float(os.getenv('ALERT_ERROR_THRESHOLD', 100)),
            'temperature': float(os.getenv('ALERT_TEMP_THRESHOLD', 75))
        }
        
        self.notification_config = {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.example.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
            'smtp_user': os.getenv('SMTP_USER', ''),
            'smtp_password': os.getenv('SMTP_PASSWORD', ''),
            'from_address': os.getenv('ALERT_FROM_ADDRESS', 'alerts@network.com'),
            'to_addresses': os.getenv('ALERT_TO_ADDRESSES', '').split(',')
        }
        
        # Track active alerts to prevent duplicate notifications
        self.active_alerts = {}
    
    def check_thresholds(self, metrics: Dict) -> List[str]:
        """Check metrics against thresholds and return alerts."""
        alerts = []
        
        # Check CPU usage
        if metrics.get('cpu_percent', 0) > self.thresholds['cpu_usage']:
            alerts.append(
                f"High CPU usage: {metrics['cpu_percent']}% "
                f"(threshold: {self.thresholds['cpu_usage']}%)"
            )
        
        # Check memory usage
        if metrics.get('memory_percent', 0) > self.thresholds['memory_usage']:
            alerts.append(
                f"High memory usage: {metrics['memory_percent']}% "
                f"(threshold: {self.thresholds['memory_usage']}%)"
            )
        
        # Check temperature
        if metrics.get('temperature', 0) > self.thresholds['temperature']:
            alerts.append(
                f"High temperature: {metrics['temperature']}°C "
                f"(threshold: {self.thresholds['temperature']}°C)"
            )
        
        return alerts
    
    def check_interface_alerts(self, interface_metrics: Dict) -> List[str]:
        """Check interface metrics for alerts."""
        alerts = []
        
        for interface, metrics in interface_metrics.items():
            error_count = metrics.get('errors_in', 0) + metrics.get('errors_out', 0)
            
            if error_count > self.thresholds['interface_errors']:
                alerts.append(
                    f"High error count on {interface}: {error_count} errors "
                    f"(threshold: {self.thresholds['interface_errors']})"
                )
        
        return alerts
    
    def send_alert_email(self, subject: str, body: str):
        """Send alert email notification."""
        if not all([
            self.notification_config['smtp_server'],
            self.notification_config['smtp_user'],
            self.notification_config['smtp_password'],
            self.notification_config['to_addresses']
        ]):
            logger.warning("Email notification configuration incomplete")
            return
        
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = f"Network Alert: {subject}"
            msg['From'] = self.notification_config['from_address']
            msg['To'] = ', '.join(self.notification_config['to_addresses'])
            
            with smtplib.SMTP(
                self.notification_config['smtp_server'],
                self.notification_config['smtp_port']
            ) as server:
                server.starttls()
                server.login(
                    self.notification_config['smtp_user'],
                    self.notification_config['smtp_password']
                )
                server.send_message(msg)
            
            logger.info(f"Alert email sent: {subject}")
            
        except Exception as e:
            logger.error(f"Failed to send alert email: {str(e)}")
    
    def process_device_metrics(self, device: str, metrics: Dict):
        """Process metrics from a device and generate alerts."""
        current_alerts = []
        
        # Check system metrics
        if 'system' in metrics:
            system_alerts = self.check_thresholds(metrics['system'])
            current_alerts.extend(system_alerts)
        
        # Check interface metrics
        if 'interfaces' in metrics:
            interface_alerts = self.check_interface_alerts(metrics['interfaces'])
            current_alerts.extend(interface_alerts)
        
        # Process new alerts
        for alert in current_alerts:
            alert_key = f"{device}:{alert}"
            
            # Check if this is a new alert
            if alert_key not in self.active_alerts:
                self.active_alerts[alert_key] = datetime.now()
                
                # Send notification for new alert
                self.send_alert_email(
                    f"New Alert for {device}",
                    f"Alert: {alert}\nTime: {datetime.now()}\nDevice: {device}"
                )
        
        # Clear resolved alerts
        resolved_alerts = []
        for alert_key in self.active_alerts:
            if alert_key.startswith(f"{device}:"):
                alert_message = alert_key.split(':', 1)[1]
                if alert_message not in current_alerts:
                    resolved_alerts.append(alert_key)
        
        # Remove resolved alerts and send resolution notifications
        for alert_key in resolved_alerts:
            alert_time = self.active_alerts[alert_key]
            device, alert = alert_key.split(':', 1)
            
            self.send_alert_email(
                f"Alert Resolved for {device}",
                f"Resolved Alert: {alert}\n"
                f"Alert Time: {alert_time}\n"
                f"Resolution Time: {datetime.now()}\n"
                f"Device: {device}"
            )
            
            del self.active_alerts[alert_key]
    
    def get_active_alerts(self) -> List[Dict]:
        """Get list of currently active alerts."""
        return [
            {
                'device': key.split(':', 1)[0],
                'alert': key.split(':', 1)[1],
                'time': time.isoformat()
            }
            for key, time in self.active_alerts.items()
        ]
