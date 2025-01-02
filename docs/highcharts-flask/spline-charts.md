# Spline Charts with Highcharts and Flask

## Table of Contents
- [Spline Charts with Highcharts and Flask](#spline-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Weather Forecast](#example-1:-weather-forecast)
  - [Example 2: Stock Price Analysis](#example-2:-stock-price-analysis)
  - [Example 3: Sensor Data Visualization](#example-3:-sensor-data-visualization)
- [Start the sensor data generator in a background thread](#start-the-sensor-data-generator-in-a-background-thread)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Spline Charts](#tips-for-working-with-spline-charts)



## Overview

Spline charts are a variation of line charts that use curved lines to connect data points, creating smooth transitions between values. They are particularly useful for visualizing continuous data where you want to emphasize gentle transitions and natural flow, such as temperature changes, market trends, or any time-series data where abrupt changes should be smoothed.

## Basic Configuration

Here's how to create a basic spline chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/spline-chart')
def spline_chart():
    return render_template('spline-chart.html')

@app.route('/spline-data')
def spline_data():
    # Generate sample temperature data for the past 24 hours
    hours = 24
    start_time = datetime.now() - timedelta(hours=hours)
    
    data = []
    for hour in range(hours):
        timestamp = start_time + timedelta(hours=hour)
        # Simulate temperature with a natural curve
        temperature = 20 + 5 * math.sin(hour/24 * 2 * math.pi)
        data.append([
            int(timestamp.timestamp() * 1000),  # Highcharts uses milliseconds
            round(temperature, 1)
        ])
    
    return jsonify(data)
```

```html
<!-- templates/spline-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="spline-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/spline-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('spline-container', {
                chart: {
                    type: 'spline'
                },
                title: {
                    text: 'Temperature Variation'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Time'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Temperature (°C)'
                    }
                },
                tooltip: {
                    formatter: function() {
                        return Highcharts.dateFormat('%H:%M', this.x) + '<br>' +
                               '<b>' + this.y + '°C</b>';
                    }
                },
                series: [{
                    name: 'Temperature',
                    data: data,
                    marker: {
                        enabled: true,
                        radius: 4
                    }
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Spline charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        spline: {
            lineWidth: 2,        // Line thickness
            marker: {
                enabled: true,   // Show data points
                radius: 4,       // Point size
                symbol: 'circle' // Point shape
            },
            states: {
                hover: {
                    lineWidth: 3 // Line thickness on hover
                }
            },
            connectNulls: true,  // Connect points across null values
            dashStyle: 'Solid',  // Line style
            step: false         // Use stepped line
        }
    }
});
```

## Example 1: Weather Forecast

This example shows a weather forecast with multiple data series:

```python
@app.route('/weather-forecast')
def weather_forecast():
    hours = 24
    start_time = datetime.now()
    
    # Generate sample weather data
    data = {
        'temperature': [],
        'humidity': [],
        'windSpeed': []
    }
    
    for hour in range(hours):
        timestamp = start_time + timedelta(hours=hour)
        ms_timestamp = int(timestamp.timestamp() * 1000)
        
        # Simulate weather patterns
        temp = 20 + 5 * math.sin(hour/24 * 2 * math.pi) + random.uniform(-1, 1)
        humidity = 60 + 20 * math.sin(hour/24 * 2 * math.pi + 1) + random.uniform(-5, 5)
        wind = 10 + 5 * math.sin(hour/12 * 2 * math.pi) + random.uniform(-2, 2)
        
        data['temperature'].append([ms_timestamp, round(temp, 1)])
        data['humidity'].append([ms_timestamp, round(humidity, 1)])
        data['windSpeed'].append([ms_timestamp, round(wind, 1)])
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="weather-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/weather-forecast')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('weather-chart', {
                chart: {
                    type: 'spline'
                },
                title: {
                    text: '24-Hour Weather Forecast'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Time'
                    }
                },
                yAxis: [{
                    title: {
                        text: 'Temperature (°C)',
                        style: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    }
                }, {
                    title: {
                        text: 'Humidity (%)',
                        style: {
                            color: Highcharts.getOptions().colors[1]
                        }
                    },
                    opposite: true
                }, {
                    title: {
                        text: 'Wind Speed (km/h)',
                        style: {
                            color: Highcharts.getOptions().colors[2]
                        }
                    },
                    opposite: true
                }],
                tooltip: {
                    shared: true,
                    crosshairs: true
                },
                series: [{
                    name: 'Temperature',
                    data: data.temperature,
                    yAxis: 0,
                    tooltip: {
                        valueSuffix: ' °C'
                    }
                }, {
                    name: 'Humidity',
                    data: data.humidity,
                    yAxis: 1,
                    tooltip: {
                        valueSuffix: ' %'
                    }
                }, {
                    name: 'Wind Speed',
                    data: data.windSpeed,
                    yAxis: 2,
                    tooltip: {
                        valueSuffix: ' km/h'
                    }
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Stock Price Analysis

This example shows stock price trends with technical indicators:

```python
@app.route('/stock-analysis')
def stock_analysis():
    days = 30
    start_date = datetime.now() - timedelta(days=days)
    
    data = {
        'price': [],
        'ma5': [],  # 5-day moving average
        'ma20': []  # 20-day moving average
    }
    
    # Generate sample stock data
    base_price = 100
    prices = []
    
    for day in range(days):
        date = start_date + timedelta(days=day)
        ms_timestamp = int(date.timestamp() * 1000)
        
        # Simulate price movement
        change = random.uniform(-2, 2)
        base_price *= (1 + change/100)
        prices.append(base_price)
        
        data['price'].append([ms_timestamp, round(base_price, 2)])
        
        # Calculate moving averages
        if day >= 4:  # 5-day MA
            ma5 = sum(prices[-5:]) / 5
            data['ma5'].append([ms_timestamp, round(ma5, 2)])
        
        if day >= 19:  # 20-day MA
            ma20 = sum(prices[-20:]) / 20
            data['ma20'].append([ms_timestamp, round(ma20, 2)])
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="stock-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/stock-analysis')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('stock-chart', {
                chart: {
                    type: 'spline'
                },
                title: {
                    text: 'Stock Price Analysis'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Date'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Price ($)'
                    }
                },
                tooltip: {
                    shared: true,
                    crosshairs: true,
                    valuePrefix: '$'
                },
                plotOptions: {
                    spline: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                series: [{
                    name: 'Price',
                    data: data.price,
                    zIndex: 1,
                    marker: {
                        fillColor: 'white',
                        lineWidth: 2,
                        lineColor: Highcharts.getOptions().colors[0]
                    }
                }, {
                    name: '5-Day MA',
                    data: data.ma5,
                    marker: {
                        enabled: false
                    }
                }, {
                    name: '20-Day MA',
                    data: data.ma20,
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

## Example 3: Sensor Data Visualization

This example shows real-time sensor data with WebSocket updates:

```python
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

def generate_sensor_data():
    """Simulate sensor readings"""
    while True:
        timestamp = int(time.time() * 1000)
        value = 50 + 10 * math.sin(time.time()/10) + random.uniform(-2, 2)
        socketio.emit('sensor_update', {
            'timestamp': timestamp,
            'value': round(value, 2)
        })
        time.sleep(1)

@app.route('/sensor-monitor')
def sensor_monitor():
    return render_template('sensor-monitor.html')

# Start the sensor data generator in a background thread
thread = threading.Thread(target=generate_sensor_data)
thread.daemon = True
thread.start()
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
        chart: {
            type: 'spline',
            animation: Highcharts.svg,
            events: {
                load: function() {
                    // Store reference to the series
                    const series = this.series[0];
                    
                    // Set up the updating
                    socket.on('sensor_update', function(data) {
                        series.addPoint([data.timestamp, data.value], true, 
                                      series.data.length > 50);
                    });
                }
            }
        },
        title: {
            text: 'Real-time Sensor Data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'Value'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function() {
                return '<b>' + Highcharts.dateFormat('%H:%M:%S', this.x) + '</b><br/>' +
                       '<b>Value:</b> ' + Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        series: [{
            name: 'Sensor Data',
            data: []
        }]
    });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate spline charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///measurements.db'
db = SQLAlchemy(app)

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)
    sensor_id = db.Column(db.String(50), nullable=False)

@app.route('/measurement-data')
def get_measurement_data():
    measurements = Measurement.query.order_by(Measurement.timestamp).all()
    
    data = [{
        'x': int(m.timestamp.timestamp() * 1000),
        'y': m.value
    } for m in measurements]
    
    return jsonify(data)
```

## Tips for Working with Spline Charts

1. Choose appropriate smoothing
2. Consider data density
3. Use clear markers
4. Implement proper tooltips
5. Handle missing data
6. Consider animation
7. Optimize performance
8. Use meaningful colors
