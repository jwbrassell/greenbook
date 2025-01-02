# Streaming Charts with Chart.js and Flask

## Table of Contents
- [Streaming Charts with Chart.js and Flask](#streaming-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Setup](#flask-setup)
- [Background thread for data generation](#background-thread-for-data-generation)
    - [HTML Template](#html-template)
  - [Example 1: Multi-Series Streaming](#example-1:-multi-series-streaming)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Anomaly Detection Stream](#example-2:-anomaly-detection-stream)
    - [Flask Implementation](#flask-implementation)
    - [Anomaly Visualization Configuration](#anomaly-visualization-configuration)
  - [Example 3: Performance Metrics Stream](#example-3:-performance-metrics-stream)
    - [Flask Implementation](#flask-implementation)
    - [Performance Monitoring Configuration](#performance-monitoring-configuration)
  - [Working with Database Data](#working-with-database-data)



Streaming charts enable real-time data visualization by continuously updating the chart as new data arrives. This guide demonstrates how to implement live-updating charts using Chart.js with Flask and WebSocket integration through Flask-SocketIO.

## Basic Implementation

### Flask Setup
```python
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import time
import random
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/streaming-chart')
def streaming_chart():
    return render_template('streaming_chart.html')

# Background thread for data generation
def background_thread():
    while True:
        value = random.randint(0, 100)
        timestamp = int(time.time() * 1000)  # milliseconds
        socketio.emit('data_update', {
            'value': value,
            'timestamp': timestamp
        })
        time.sleep(1)  # Update every second

@socketio.on('connect')
def handle_connect():
    # Start background thread on first connection
    Thread(target=background_thread, daemon=True).start()
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="streamingChart"></canvas>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('streamingChart').getContext('2d');
    const maxDataPoints = 50;  // Maximum number of points to display
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Real-time Data',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.4,
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Live Data Stream'
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            }
        }
    });
    
    // Connect to WebSocket
    const socket = io();
    
    socket.on('data_update', function(data) {
        // Add new data point
        chart.data.labels.push(data.timestamp);
        chart.data.datasets[0].data.push(data.value);
        
        // Remove old data points if exceeding maximum
        if (chart.data.labels.length > maxDataPoints) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }
        
        chart.update('quiet');  // Update chart with minimal animation
    });
});
</script>
```

## Example 1: Multi-Series Streaming

This example shows how to stream multiple data series simultaneously.

### Flask Implementation
```python
@app.route('/api/multi-stream')
def multi_stream():
    return render_template('multi_stream.html')

def generate_sensor_data():
    return {
        'temperature': random.uniform(20, 30),
        'humidity': random.uniform(40, 60),
        'pressure': random.uniform(980, 1020)
    }

def multi_sensor_thread():
    while True:
        data = generate_sensor_data()
        data['timestamp'] = int(time.time() * 1000)
        socketio.emit('sensor_update', data)
        time.sleep(1)

@socketio.on('start_monitoring')
def handle_monitoring():
    Thread(target=multi_sensor_thread, daemon=True).start()
```

### Advanced Configuration
```javascript
const config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Temperature (°C)',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                yAxisID: 'temperature'
            },
            {
                label: 'Humidity (%)',
                data: [],
                borderColor: 'rgb(54, 162, 235)',
                yAxisID: 'humidity'
            },
            {
                label: 'Pressure (hPa)',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                yAxisID: 'pressure'
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            temperature: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Temperature (°C)'
                }
            },
            humidity: {
                type: 'linear',
                position: 'right',
                title: {
                    display: true,
                    text: 'Humidity (%)'
                }
            },
            pressure: {
                type: 'linear',
                position: 'right',
                title: {
                    display: true,
                    text: 'Pressure (hPa)'
                },
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    }
};

socket.on('sensor_update', function(data) {
    const timestamp = data.timestamp;
    
    chart.data.labels.push(timestamp);
    chart.data.datasets[0].data.push(data.temperature);
    chart.data.datasets[1].data.push(data.humidity);
    chart.data.datasets[2].data.push(data.pressure);
    
    if (chart.data.labels.length > maxDataPoints) {
        chart.data.labels.shift();
        chart.data.datasets.forEach(dataset => dataset.data.shift());
    }
    
    chart.update('quiet');
});
```

## Example 2: Anomaly Detection Stream

This example demonstrates how to highlight anomalies in streaming data.

### Flask Implementation
```python
def generate_data_with_anomalies():
    base_value = 50
    noise = random.uniform(-5, 5)
    value = base_value + noise
    
    # Occasionally generate anomalies
    if random.random() < 0.1:  # 10% chance of anomaly
        value += random.choice([-20, 20])
    
    return value

def anomaly_detection_thread():
    while True:
        value = generate_data_with_anomalies()
        timestamp = int(time.time() * 1000)
        
        # Detect anomaly if value is outside normal range
        is_anomaly = abs(value - 50) > 15
        
        socketio.emit('anomaly_update', {
            'value': value,
            'timestamp': timestamp,
            'is_anomaly': is_anomaly
        })
        time.sleep(1)

@socketio.on('start_anomaly_detection')
def handle_anomaly_detection():
    Thread(target=anomaly_detection_thread, daemon=True).start()
```

### Anomaly Visualization Configuration
```javascript
const config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Sensor Data',
            data: [],
            borderColor: 'rgb(75, 192, 192)',
            pointBackgroundColor: [],
            pointRadius: [],
            pointHoverRadius: []
        }]
    },
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.raw;
                        const isAnomaly = context.dataset.pointBackgroundColor[context.dataIndex] === 'red';
                        return `Value: ${value}${isAnomaly ? ' (Anomaly)' : ''}`;
                    }
                }
            }
        }
    }
};

socket.on('anomaly_update', function(data) {
    chart.data.labels.push(data.timestamp);
    chart.data.datasets[0].data.push(data.value);
    
    // Set point styling based on anomaly status
    chart.data.datasets[0].pointBackgroundColor.push(
        data.is_anomaly ? 'red' : 'rgb(75, 192, 192)'
    );
    chart.data.datasets[0].pointRadius.push(
        data.is_anomaly ? 8 : 3
    );
    chart.data.datasets[0].pointHoverRadius.push(
        data.is_anomaly ? 10 : 5
    );
    
    if (chart.data.labels.length > maxDataPoints) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[0].pointBackgroundColor.shift();
        chart.data.datasets[0].pointRadius.shift();
        chart.data.datasets[0].pointHoverRadius.shift();
    }
    
    chart.update('quiet');
});
```

## Example 3: Performance Metrics Stream

This example shows how to stream system performance metrics with dynamic thresholds.

### Flask Implementation
```python
import psutil

def get_system_metrics():
    return {
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    }

def performance_thread():
    while True:
        metrics = get_system_metrics()
        metrics['timestamp'] = int(time.time() * 1000)
        
        # Calculate dynamic thresholds based on recent history
        socketio.emit('performance_update', metrics)
        time.sleep(2)

@socketio.on('start_performance_monitoring')
def handle_performance_monitoring():
    Thread(target=performance_thread, daemon=True).start()
```

### Performance Monitoring Configuration
```javascript
const config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'CPU Usage',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                fill: true,
                backgroundColor: 'rgba(255, 99, 132, 0.2)'
            },
            {
                label: 'Memory Usage',
                data: [],
                borderColor: 'rgb(54, 162, 235)',
                fill: true,
                backgroundColor: 'rgba(54, 162, 235, 0.2)'
            },
            {
                label: 'Disk Usage',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                fill: true,
                backgroundColor: 'rgba(75, 192, 192, 0.2)'
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'System Performance Metrics'
            }
        },
        scales: {
            y: {
                min: 0,
                max: 100,
                title: {
                    display: true,
                    text: 'Usage (%)'
                }
            }
        }
    }
};

// Add threshold lines plugin
const thresholdPlugin = {
    id: 'thresholds',
    beforeDraw: (chart) => {
        const {ctx, chartArea, scales} = chart;
        const warningY = scales.y.getPixelForValue(80);
        const criticalY = scales.y.getPixelForValue(90);
        
        ctx.save();
        
        // Draw warning threshold
        ctx.strokeStyle = 'rgba(255, 206, 86, 0.5)';
        ctx.beginPath();
        ctx.moveTo(chartArea.left, warningY);
        ctx.lineTo(chartArea.right, warningY);
        ctx.stroke();
        
        // Draw critical threshold
        ctx.strokeStyle = 'rgba(255, 99, 132, 0.5)';
        ctx.beginPath();
        ctx.moveTo(chartArea.left, criticalY);
        ctx.lineTo(chartArea.right, criticalY);
        ctx.stroke();
        
        ctx.restore();
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for historical data and streaming:

```python
class MetricHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric_type = db.Column(db.String(50))
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_recent_history(metric_type, minutes=5):
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        return MetricHistory.query\
            .filter(
                MetricHistory.metric_type == metric_type,
                MetricHistory.timestamp >= cutoff
            )\
            .order_by(MetricHistory.timestamp)\
            .all()

@app.route('/api/metric-history/<metric_type>')
def get_metric_history(metric_type):
    history = MetricHistory.get_recent_history(metric_type)
    return jsonify({
        'labels': [h.timestamp.isoformat() for h in history],
        'data': [h.value for h in history]
    })

def save_metric(metric_type, value):
    metric = MetricHistory(
        metric_type=metric_type,
        value=value
    )
    db.session.add(metric)
    db.session.commit()
```

This documentation provides three distinct examples of streaming charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask and WebSocket, from basic implementation to advanced features like anomaly detection and performance monitoring.
