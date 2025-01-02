# Line Charts with Highcharts and Flask

## Table of Contents
- [Line Charts with Highcharts and Flask](#line-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Multi-Series Temperature Data](#example-1:-multi-series-temperature-data)
  - [Example 2: Stock Price with Moving Average](#example-2:-stock-price-with-moving-average)
  - [Example 3: Real-time Sensor Data](#example-3:-real-time-sensor-data)
- [Start the sensor simulation in a background thread](#start-the-sensor-simulation-in-a-background-thread)
  - [Database Integration Example](#database-integration-example)
  - [How It Works with Flask](#how-it-works-with-flask)
  - [Common Use Cases](#common-use-cases)
  - [Tips for Working with Line Charts](#tips-for-working-with-line-charts)



## Overview

Line charts are one of the most fundamental and widely used chart types in data visualization. They excel at showing trends over time, comparing multiple series of data, and visualizing continuous data sets. Highcharts provides extensive customization options for line charts, making them highly versatile for various use cases.

## Basic Configuration

Here's how to create a basic line chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

@app.route('/line-chart')
def line_chart():
    return render_template('line-chart.html')

@app.route('/line-data')
def line_data():
    # Generate sample data
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') 
             for x in range(10)]
    values = [random.randint(50, 100) for _ in range(10)]
    
    return jsonify({
        'dates': dates,
        'values': values
    })
```

```html
<!-- templates/line-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="line-chart-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/line-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('line-chart-container', {
                title: {
                    text: 'Basic Line Chart'
                },
                xAxis: {
                    categories: data.dates,
                    title: {
                        text: 'Date'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Values'
                    }
                },
                series: [{
                    name: 'Sample Data',
                    data: data.values
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Line charts in Highcharts offer many customization options:

```javascript
Highcharts.chart('container', {
    // Chart type-specific options
    plotOptions: {
        line: {
            lineWidth: 2,          // Width of the line
            marker: {
                enabled: true,     // Show points on the line
                radius: 4          // Size of the points
            },
            enableMouseTracking: true,  // Show tooltip on hover
            dashStyle: 'solid',    // Line style ('dash', 'dot', 'dashdot')
            step: false           // Step line ('left', 'center', 'right')
        }
    },
    
    // Tooltip customization
    tooltip: {
        crosshairs: true,
        shared: true,
        valueDecimals: 2
    },
    
    // Legend customization
    legend: {
        enabled: true,
        layout: 'horizontal',
        align: 'center',
        verticalAlign: 'bottom'
    }
});
```

## Example 1: Multi-Series Temperature Data

This example shows temperature data from multiple cities:

```python
@app.route('/temperature-data')
def temperature_data():
    # Simulated temperature data for different cities
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') 
             for x in range(7)]
    
    return jsonify({
        'dates': dates,
        'cities': {
            'New York': [random.uniform(15, 25) for _ in range(7)],
            'London': [random.uniform(10, 20) for _ in range(7)],
            'Tokyo': [random.uniform(20, 30) for _ in range(7)]
        }
    })
```

```html
{% extends "base.html" %}

{% block content %}
<div id="temperature-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/temperature-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('temperature-chart', {
                title: {
                    text: 'Weekly Temperature Comparison'
                },
                xAxis: {
                    categories: data.dates
                },
                yAxis: {
                    title: {
                        text: 'Temperature (°C)'
                    }
                },
                tooltip: {
                    crosshairs: true,
                    shared: true,
                    valueSuffix: '°C'
                },
                series: Object.entries(data.cities).map(([city, temps]) => ({
                    name: city,
                    data: temps
                }))
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Stock Price with Moving Average

This example demonstrates a stock price chart with a 5-day moving average:

```python
@app.route('/stock-data')
def stock_data():
    # Simulate stock price data
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') 
             for x in range(30)]
    prices = []
    last_price = 100
    
    for _ in range(30):
        change = random.uniform(-2, 2)
        last_price += change
        prices.append(round(last_price, 2))
    
    # Calculate 5-day moving average
    ma5 = []
    for i in range(len(prices)):
        if i < 4:
            ma5.append(None)
        else:
            ma5.append(sum(prices[i-4:i+1]) / 5)
    
    return jsonify({
        'dates': dates,
        'prices': prices,
        'ma5': ma5
    })
```

```html
{% extends "base.html" %}

{% block content %}
<div id="stock-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/stock-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('stock-chart', {
                title: {
                    text: 'Stock Price with Moving Average'
                },
                xAxis: {
                    categories: data.dates
                },
                yAxis: {
                    title: {
                        text: 'Price ($)'
                    }
                },
                tooltip: {
                    valuePrefix: '$'
                },
                series: [{
                    name: 'Stock Price',
                    data: data.prices
                }, {
                    name: '5-Day MA',
                    data: data.ma5,
                    dashStyle: 'shortdash',
                    marker: {
                        enabled: false
                    }
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Real-time Sensor Data

This example shows how to create a real-time updating line chart for sensor data:

```python
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

def generate_sensor_data():
    """Simulate sensor readings every second"""
    while True:
        reading = random.uniform(20, 30)  # Simulate temperature reading
        timestamp = datetime.now().strftime('%H:%M:%S')
        socketio.emit('sensor_update', {
            'timestamp': timestamp,
            'value': reading
        })
        time.sleep(1)

@app.route('/sensor-chart')
def sensor_chart():
    return render_template('sensor-chart.html')

# Start the sensor simulation in a background thread
sensor_thread = threading.Thread(target=generate_sensor_data)
sensor_thread.daemon = True
sensor_thread.start()
```

```html
{% extends "base.html" %}

{% block content %}
<div id="sensor-chart"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    
    const chart = Highcharts.chart('sensor-chart', {
        title: {
            text: 'Real-time Sensor Data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'Temperature (°C)'
            },
            plotLines: [{
                value: 25,
                color: 'red',
                dashStyle: 'shortdash',
                width: 2,
                label: {
                    text: 'Warning Threshold'
                }
            }]
        },
        series: [{
            name: 'Temperature',
            data: []
        }]
    });
    
    // Keep only last 20 points
    const MAX_POINTS = 20;
    
    socket.on('sensor_update', function(data) {
        const series = chart.series[0];
        const shift = series.data.length > MAX_POINTS;
        
        series.addPoint({
            x: new Date().getTime(),
            y: data.value
        }, true, shift);
    });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate the line chart with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db = SQLAlchemy(app)

class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Float, nullable=False)
    sensor_id = db.Column(db.String(50), nullable=False)

@app.route('/historical-data')
def get_historical_data():
    # Get last 100 readings for a specific sensor
    readings = SensorReading.query.filter_by(sensor_id='temp_sensor_1')\
        .order_by(SensorReading.timestamp.desc())\
        .limit(100).all()
    
    return jsonify({
        'timestamps': [r.timestamp.strftime('%Y-%m-%d %H:%M:%S') for r in readings],
        'values': [r.value for r in readings]
    })
```

## How It Works with Flask

1. The Flask route `/line-data` provides the data in JSON format
2. The template uses Jinja2 templating to extend the base template
3. JavaScript fetches the data and creates the Highcharts line chart
4. For real-time updates, Socket.IO enables push notifications
5. Database integration allows for persistent data storage and retrieval

## Common Use Cases

1. Time series data visualization
2. Financial data analysis
3. Temperature and sensor monitoring
4. Performance metrics tracking
5. Trend analysis and forecasting

## Tips for Working with Line Charts

1. Use appropriate data intervals for your x-axis
2. Consider using markers only at data points for clarity
3. Implement proper date formatting for time series data
4. Use tooltips to show detailed information
5. Consider implementing zoom and pan for large datasets
6. Use appropriate colors for multiple series
7. Add gridlines for better readability
8. Implement proper error handling for data loading
