# Network Monitoring and Visualization

## Table of Contents
1. [Introduction](#introduction)
2. [Data Collection](#data-collection)
3. [Visualization Tools](#visualization-tools)
4. [Real-time Monitoring](#real-time-monitoring)
5. [Dashboard Creation](#dashboard-creation)
6. [Alert Management](#alert-management)
7. [Best Practices](#best-practices)
8. [Examples](#examples)

## Introduction

Effective network monitoring and visualization are crucial for understanding network behavior, identifying issues, and making informed decisions. This guide covers how to collect, visualize, and monitor network data effectively.

### Why Monitor?
- Detect issues proactively
- Understand network patterns
- Track performance metrics
- Plan capacity effectively
- Validate configuration changes

## Data Collection

### Metrics to Monitor
1. Device Status
2. Interface Statistics
3. Bandwidth Utilization
4. Error Rates
5. Configuration Changes

### Collection Methods
```python
import time
from typing import Dict, List
import psutil
import requests

class NetworkMetricsCollector:
    def __init__(self, devices: List[str]):
        self.devices = devices
        self.metrics: Dict = {}
    
    def collect_interface_metrics(self, device: str) -> Dict:
        """Collect interface metrics from a device."""
        url = f"https://{device}/api/v1/interfaces/metrics"
        try:
            response = requests.get(url)
            return response.json()
        except requests.RequestException:
            return {}
    
    def collect_system_metrics(self, device: str) -> Dict:
        """Collect system metrics from a device."""
        metrics = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'timestamp': time.time()
        }
        return metrics
```

## Visualization Tools

### Flask Integration
```python
from flask import Flask, render_template
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    # Get network data
    data = collect_network_data()
    
    # Create visualization
    df = pd.DataFrame(data)
    fig = px.line(df, x='timestamp', y='utilization',
                  title='Network Utilization')
    
    return render_template('dashboard.html',
                         plot=fig.to_html())
```

### Chart Types
1. Line Charts
   - Bandwidth usage over time
   - Error rates
   - Latency trends

2. Bar Charts
   - Interface statistics
   - Protocol distribution
   - Error counts

3. Pie Charts
   - Traffic distribution
   - Protocol breakdown
   - Resource allocation

4. Heat Maps
   - Network congestion
   - Error patterns
   - Usage patterns

## Real-time Monitoring

### WebSocket Implementation
```python
import asyncio
import websockets
import json

class NetworkMonitor:
    def __init__(self):
        self.clients = set()
    
    async def register(self, websocket):
        """Register a new client."""
        self.clients.add(websocket)
    
    async def unregister(self, websocket):
        """Unregister a client."""
        self.clients.remove(websocket)
    
    async def send_updates(self, data: dict):
        """Send updates to all connected clients."""
        if not self.clients:
            return
        
        message = json.dumps(data)
        await asyncio.gather(
            *[client.send(message) for client in self.clients]
        )
```

### Real-time Updates
```javascript
// Client-side JavaScript
const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    updateDashboard(data);
};

function updateDashboard(data) {
    // Update charts and metrics
    Object.entries(data).forEach(([metric, value]) => {
        updateChart(metric, value);
    });
}
```

## Dashboard Creation

### Flask Dashboard Example
```python
from flask import Flask, jsonify
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)

@app.route('/api/metrics')
def get_metrics():
    """Get network metrics for dashboard."""
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    # Get metrics from database
    metrics = pd.read_sql_query(
        """
        SELECT timestamp, metric, value
        FROM network_metrics
        WHERE timestamp BETWEEN %s AND %s
        """,
        params=[start_time, end_time]
    )
    
    return jsonify(metrics.to_dict())
```

### Dashboard Components
1. Overview Panel
   - System status
   - Critical alerts
   - Key metrics

2. Detailed Views
   - Interface statistics
   - Protocol analysis
   - Error tracking

3. Historical Data
   - Trend analysis
   - Comparison views
   - Performance history

## Alert Management

### Alert Configuration
```python
class AlertManager:
    def __init__(self):
        self.thresholds = {
            'cpu_usage': 80,
            'memory_usage': 90,
            'error_rate': 0.01
        }
    
    def check_thresholds(self, metrics: Dict) -> List[str]:
        """Check metrics against thresholds."""
        alerts = []
        
        if metrics['cpu_usage'] > self.thresholds['cpu_usage']:
            alerts.append(f"High CPU usage: {metrics['cpu_usage']}%")
        
        if metrics['memory_usage'] > self.thresholds['memory_usage']:
            alerts.append(f"High memory usage: {metrics['memory_usage']}%")
        
        return alerts
```

### Alert Notification
```python
import smtplib
from email.message import EmailMessage

def send_alert(subject: str, body: str, recipients: List[str]):
    """Send alert email."""
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "alerts@network.com"
    msg['To'] = ", ".join(recipients)
    
    # Send email
    with smtplib.SMTP('smtp.network.com') as server:
        server.send_message(msg)
```

## Best Practices

### Data Collection
1. Collect only necessary metrics
2. Use appropriate sampling intervals
3. Implement data retention policies
4. Handle collection errors gracefully
5. Validate collected data

### Visualization
1. Choose appropriate chart types
2. Use consistent color schemes
3. Provide interactive features
4. Include context and legends
5. Optimize for performance

### Monitoring
1. Set meaningful thresholds
2. Implement trend analysis
3. Use correlation analysis
4. Monitor system health
5. Track configuration changes

## Examples

### Complete Dashboard Implementation
See the [examples/dashboard](../examples/dashboard/) directory for a complete implementation including:
- Data collection scripts
- Visualization templates
- Alert configuration
- Real-time updates
- Historical data management

## Related Resources
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Monitoring](https://prometheus.io/docs/introduction/overview/)
- [Flask Dashboard Tutorial](https://flask.palletsprojects.com/tutorial/)
- [Network Monitoring Best Practices](https://www.cisco.com/c/en/us/support/docs/availability/high-availability/15112-HAS-bestpractice.html)
