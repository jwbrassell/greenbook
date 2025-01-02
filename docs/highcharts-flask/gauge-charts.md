# Gauge Charts with Highcharts and Flask

## Table of Contents
- [Gauge Charts with Highcharts and Flask](#gauge-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Gauge Charts](#tips-for-working-with-gauge-charts)



## Overview

Gauge charts (also known as dial charts or speedometer charts) are ideal for displaying single values within a defined range. They are particularly useful for showing metrics like performance indicators, progress towards goals, or any measurement that has minimum and maximum values.

## Basic Configuration

Here's how to create a basic gauge chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/gauge-chart')
def gauge_chart():
    return render_template('gauge-chart.html')

@app.route('/gauge-data')
def gauge_data():
    # Sample performance metric
    data = {
        'value': 72.8,
        'min': 0,
        'max': 100,
        'name': 'Performance Score'
    }
    
    return jsonify(data)
```

```html
<!-- templates/gauge-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="gauge-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/gauge-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('gauge-container', {
                chart: {
                    type: 'gauge'
                },
                title: {
                    text: data.name
                },
                pane: {
                    startAngle: -150,
                    endAngle: 150,
                    background: [{
                        backgroundColor: '#EEE',
                        borderWidth: 0,
                        outerRadius: '109%'
                    }]
                },
                yAxis: {
                    min: data.min,
                    max: data.max,
                    title: {
                        text: 'Score'
                    },
                    plotBands: [{
                        from: 0,
                        to: 60,
                        color: '#DF5353'  // red
                    }, {
                        from: 60,
                        to: 80,
                        color: '#DDDF0D'  // yellow
                    }, {
                        from: 80,
                        to: 100,
                        color: '#55BF3B'  // green
                    }]
                },
                series: [{
                    name: data.name,
                    data: [data.value],
                    tooltip: {
                        valueSuffix: ' points'
                    }
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate gauge charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metrics.db'
db = SQLAlchemy(app)

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    min_value = db.Column(db.Float, nullable=False)
    max_value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/metric/<metric_name>')
def get_metric(metric_name):
    metric = Metric.query.filter_by(name=metric_name).order_by(Metric.timestamp.desc()).first()
    
    if metric:
        data = {
            'value': metric.value,
            'min': metric.min_value,
            'max': metric.max_value,
            'name': metric.name
        }
        return jsonify(data)
    
    return jsonify({'error': 'Metric not found'}), 404
```

## Tips for Working with Gauge Charts

1. Choose appropriate ranges
2. Use meaningful colors
3. Add clear labels
4. Consider animations
5. Implement proper tooltips
6. Use consistent styling
7. Add reference markers
8. Optimize readability
