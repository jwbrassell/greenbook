#!/usr/bin/env python3
"""
Network Monitoring Dashboard
--------------------------
A Flask application that provides real-time network monitoring
and visualization capabilities.
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List

from flask import Flask, render_template, jsonify
import pandas as pd
from dotenv import load_dotenv

from collectors import NetworkMetricsCollector
from alerts import AlertManager

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize collectors and managers
collector = NetworkMetricsCollector(
    devices=os.getenv('NETWORK_DEVICES', '').split(',')
)
alert_manager = AlertManager()

@app.route('/')
def index():
    """Render main dashboard page."""
    return render_template(
        'index.html',
        title='Network Monitoring Dashboard'
    )

@app.route('/api/metrics/current')
def current_metrics():
    """Get current network metrics."""
    metrics = {}
    
    # Collect metrics from all devices
    for device in collector.devices:
        device_metrics = collector.collect_system_metrics(device)
        interface_metrics = collector.collect_interface_metrics(device)
        
        metrics[device] = {
            'system': device_metrics,
            'interfaces': interface_metrics,
            'timestamp': datetime.now().isoformat()
        }
    
    return jsonify(metrics)

@app.route('/api/metrics/history')
def historical_metrics():
    """Get historical network metrics."""
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    # Get metrics from database
    metrics = pd.read_sql_query(
        """
        SELECT timestamp, device, metric, value
        FROM network_metrics
        WHERE timestamp BETWEEN %s AND %s
        ORDER BY timestamp DESC
        """,
        params=[start_time, end_time]
    )
    
    return jsonify(metrics.to_dict())

@app.route('/api/alerts')
def get_alerts():
    """Get current alerts."""
    current_metrics = {}
    
    # Check each device for alerts
    alerts = []
    for device in collector.devices:
        metrics = collector.collect_system_metrics(device)
        device_alerts = alert_manager.check_thresholds(metrics)
        
        if device_alerts:
            alerts.extend([
                {
                    'device': device,
                    'alert': alert,
                    'timestamp': datetime.now().isoformat()
                }
                for alert in device_alerts
            ])
    
    return jsonify(alerts)

@app.route('/api/devices')
def get_devices():
    """Get list of monitored devices."""
    devices = []
    
    for device in collector.devices:
        status = 'up' if collector.check_device_status(device) else 'down'
        devices.append({
            'name': device,
            'status': status,
            'last_check': datetime.now().isoformat()
        })
    
    return jsonify(devices)

@app.route('/api/interfaces/<device>')
def get_interfaces(device):
    """Get interface information for a specific device."""
    interfaces = collector.collect_interface_metrics(device)
    return jsonify(interfaces)

@app.route('/api/config')
def get_config():
    """Get dashboard configuration."""
    config = {
        'refresh_interval': int(os.getenv('REFRESH_INTERVAL', 60)),
        'alert_thresholds': alert_manager.thresholds,
        'chart_defaults': {
            'timespan': '24h',
            'granularity': '5m'
        }
    }
    return jsonify(config)

if __name__ == '__main__':
    # Run the application
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )
