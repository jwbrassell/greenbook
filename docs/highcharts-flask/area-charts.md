# Area Charts with Highcharts and Flask

## Table of Contents
- [Area Charts with Highcharts and Flask](#area-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Revenue Breakdown](#example-1:-revenue-breakdown)
  - [Example 2: Resource Usage](#example-2:-resource-usage)
  - [Example 3: Market Share](#example-3:-market-share)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Area Charts](#tips-for-working-with-area-charts)



## Overview

Area charts are ideal for visualizing quantitative data over time where the area between the line and the axis is filled, making them particularly useful for showing cumulative totals, comparing volumes, or displaying parts of a whole. They effectively communicate both the individual values and their contribution to the total.

## Basic Configuration

Here's how to create a basic area chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/area-chart')
def area_chart():
    return render_template('area-chart.html')

@app.route('/area-data')
def area_data():
    # Generate sample data for website traffic over a week
    days = 7
    start_date = datetime.now() - timedelta(days=days)
    
    data = []
    for day in range(days):
        timestamp = start_date + timedelta(days=day)
        # Simulate daily traffic pattern
        visitors = 1000 + 500 * math.sin(day/7 * 2 * math.pi) + random.randint(-100, 100)
        data.append([
            int(timestamp.timestamp() * 1000),  # Highcharts uses milliseconds
            round(visitors)
        ])
    
    return jsonify(data)
```

```html
<!-- templates/area-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="area-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/area-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('area-container', {
                chart: {
                    type: 'area'
                },
                title: {
                    text: 'Website Traffic'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Date'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Visitors'
                    },
                    min: 0
                },
                tooltip: {
                    formatter: function() {
                        return Highcharts.dateFormat('%A, %b %e', this.x) + '<br>' +
                               '<b>Visitors: ' + Highcharts.numberFormat(this.y, 0) + '</b>';
                    }
                },
                plotOptions: {
                    area: {
                        fillOpacity: 0.5
                    }
                },
                series: [{
                    name: 'Daily Visitors',
                    data: data
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Area charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        area: {
            fillOpacity: 0.5,     // Opacity of the fill
            lineWidth: 1,         // Width of the line
            marker: {
                enabled: true,     // Show data points
                radius: 4,         // Point size
                symbol: 'circle'   // Point shape
            },
            stacking: null,       // 'normal' or 'percent' for stacked areas
            step: false,          // Connect points with steps
            threshold: null,      // Fill threshold
            fillColor: {
                linearGradient: {
                    x1: 0,
                    y1: 0,
                    x2: 0,
                    y2: 1
                },
                stops: [
                    [0, Highcharts.getOptions().colors[0]],
                    [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                ]
            }
        }
    }
});
```

## Example 1: Revenue Breakdown

This example shows revenue streams with stacked areas:

```python
@app.route('/revenue-data')
def revenue_data():
    months = 12
    start_date = datetime.now() - timedelta(days=months*30)
    
    data = {
        'product_sales': [],
        'services': [],
        'subscriptions': []
    }
    
    for month in range(months):
        timestamp = start_date + timedelta(days=month*30)
        ms_timestamp = int(timestamp.timestamp() * 1000)
        
        # Simulate different revenue streams with seasonal variations
        base = 1 + 0.2 * math.sin(month/12 * 2 * math.pi)  # Seasonal factor
        
        data['product_sales'].append([
            ms_timestamp,
            round(50000 * base + random.uniform(-5000, 5000))
        ])
        data['services'].append([
            ms_timestamp,
            round(30000 * base + random.uniform(-3000, 3000))
        ])
        data['subscriptions'].append([
            ms_timestamp,
            round(20000 * base + random.uniform(-2000, 2000))
        ])
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="revenue-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/revenue-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('revenue-chart', {
                chart: {
                    type: 'area'
                },
                title: {
                    text: 'Revenue Breakdown'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Date'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Revenue ($)'
                    },
                    labels: {
                        formatter: function() {
                            return '$' + this.value / 1000 + 'k';
                        }
                    }
                },
                tooltip: {
                    shared: true,
                    formatter: function() {
                        return this.points.reduce((s, point) => {
                            return s + '<br/>' + point.series.name + ': $' + 
                                   Highcharts.numberFormat(point.y, 0);
                        }, '<b>' + Highcharts.dateFormat('%B %Y', this.x) + '</b>');
                    }
                },
                plotOptions: {
                    area: {
                        stacking: 'normal',
                        marker: {
                            enabled: false
                        }
                    }
                },
                series: [{
                    name: 'Product Sales',
                    data: data.product_sales
                }, {
                    name: 'Services',
                    data: data.services
                }, {
                    name: 'Subscriptions',
                    data: data.subscriptions
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Resource Usage

This example shows system resource usage over time:

```python
@app.route('/resource-usage')
def resource_usage():
    hours = 24
    start_time = datetime.now() - timedelta(hours=hours)
    
    data = {
        'cpu': [],
        'memory': [],
        'disk': []
    }
    
    for hour in range(hours):
        timestamp = start_time + timedelta(hours=hour)
        ms_timestamp = int(timestamp.timestamp() * 1000)
        
        # Simulate resource usage patterns
        hour_factor = hour / 24  # Time of day factor
        
        data['cpu'].append([
            ms_timestamp,
            round(40 + 30 * math.sin(hour_factor * 2 * math.pi) + random.uniform(-5, 5))
        ])
        data['memory'].append([
            ms_timestamp,
            round(60 + 15 * math.sin(hour_factor * 2 * math.pi) + random.uniform(-3, 3))
        ])
        data['disk'].append([
            ms_timestamp,
            round(75 + 5 * math.sin(hour_factor * 2 * math.pi) + random.uniform(-2, 2))
        ])
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="resource-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/resource-usage')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('resource-chart', {
                chart: {
                    type: 'area'
                },
                title: {
                    text: 'System Resource Usage'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Time'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Usage (%)'
                    },
                    min: 0,
                    max: 100
                },
                tooltip: {
                    shared: true,
                    valueSuffix: '%'
                },
                plotOptions: {
                    area: {
                        fillOpacity: 0.3,
                        marker: {
                            enabled: false,
                            symbol: 'circle',
                            radius: 2,
                            states: {
                                hover: {
                                    enabled: true
                                }
                            }
                        }
                    }
                },
                series: [{
                    name: 'CPU',
                    data: data.cpu
                }, {
                    name: 'Memory',
                    data: data.memory
                }, {
                    name: 'Disk',
                    data: data.disk
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Market Share

This example shows market share evolution with percentage stacking:

```python
@app.route('/market-share')
def market_share():
    years = 5
    start_year = datetime.now().year - years
    
    data = {
        'company_a': [],
        'company_b': [],
        'company_c': [],
        'others': []
    }
    
    # Initial market shares
    shares = {
        'company_a': 35,
        'company_b': 30,
        'company_c': 20,
        'others': 15
    }
    
    for year in range(years + 1):
        timestamp = datetime(start_year + year, 1, 1)
        ms_timestamp = int(timestamp.timestamp() * 1000)
        
        # Simulate market share changes
        total = sum(shares.values())
        for company in shares:
            # Random market share changes
            change = random.uniform(-2, 2)
            shares[company] = max(5, min(50, shares[company] + change))
            
            data[company].append([
                ms_timestamp,
                shares[company]
            ])
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="market-share-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/market-share')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('market-share-chart', {
                chart: {
                    type: 'area'
                },
                title: {
                    text: 'Market Share Evolution'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Year'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Market Share'
                    },
                    labels: {
                        formatter: function() {
                            return this.value + '%';
                        }
                    }
                },
                tooltip: {
                    pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.percentage:.1f}%</b><br/>',
                    shared: true
                },
                plotOptions: {
                    area: {
                        stacking: 'percent',
                        lineColor: '#ffffff',
                        lineWidth: 1,
                        marker: {
                            lineWidth: 1,
                            lineColor: '#ffffff'
                        }
                    }
                },
                series: [{
                    name: 'Company A',
                    data: data.company_a
                }, {
                    name: 'Company B',
                    data: data.company_b
                }, {
                    name: 'Company C',
                    data: data.company_c
                }, {
                    name: 'Others',
                    data: data.others
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate area charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metrics.db'
db = SQLAlchemy(app)

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)

@app.route('/metric-data')
def get_metric_data():
    metrics = db.session.query(
        Metric.timestamp,
        Metric.category,
        db.func.sum(Metric.value).label('total')
    ).group_by(
        Metric.timestamp,
        Metric.category
    ).order_by(
        Metric.timestamp
    ).all()
    
    # Group by category
    series_data = {}
    for metric in metrics:
        if metric.category not in series_data:
            series_data[metric.category] = []
        series_data[metric.category].append([
            int(metric.timestamp.timestamp() * 1000),
            float(metric.total)
        ])
    
    return jsonify(series_data)
```

## Tips for Working with Area Charts

1. Choose appropriate stacking
2. Consider opacity levels
3. Use clear colors
4. Implement proper tooltips
5. Handle missing data
6. Consider gradients
7. Optimize performance
8. Use meaningful legends
