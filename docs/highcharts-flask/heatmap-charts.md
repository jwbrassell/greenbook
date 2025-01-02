# Heatmap Charts with Highcharts and Flask

## Table of Contents
- [Heatmap Charts with Highcharts and Flask](#heatmap-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Heatmap Charts](#tips-for-working-with-heatmap-charts)



## Overview

Heatmap charts display data in a grid format where values are represented by colors. They are particularly useful for visualizing patterns in large datasets, showing correlations between variables, or displaying data density across two dimensions.

## Basic Configuration

Here's how to create a basic heatmap chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/heatmap-chart')
def heatmap_chart():
    return render_template('heatmap-chart.html')

@app.route('/heatmap-data')
def heatmap_data():
    # Sample data: hourly activity over a week
    hours = list(range(24))
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Generate sample activity data
    data = []
    for day_idx, day in enumerate(days):
        for hour in hours:
            # Simulate higher activity during work hours
            base_activity = 30 if 9 <= hour <= 17 and day_idx < 5 else 10
            activity = base_activity + np.random.normal(0, 5)
            data.append([hour, day_idx, max(0, round(activity, 1))])
    
    return jsonify({
        'data': data,
        'hours': hours,
        'days': days
    })
```

```html
<!-- templates/heatmap-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="heatmap-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/heatmap-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('heatmap-container', {
                chart: {
                    type: 'heatmap'
                },
                title: {
                    text: 'Weekly Activity Heatmap'
                },
                xAxis: {
                    categories: data.hours,
                    title: 'Hour of Day'
                },
                yAxis: {
                    categories: data.days,
                    title: null
                },
                colorAxis: {
                    min: 0,
                    minColor: '#FFFFFF',
                    maxColor: '#7cb5ec'
                },
                legend: {
                    align: 'right',
                    layout: 'vertical',
                    margin: 0,
                    verticalAlign: 'middle',
                    symbolHeight: 280
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.series.yAxis.categories[this.point.y] + '</b> at ' +
                               this.series.xAxis.categories[this.point.x] + ':00<br>' +
                               '<b>Activity: </b>' + this.point.value;
                    }
                },
                series: [{
                    name: 'Activity Level',
                    borderWidth: 1,
                    data: data.data,
                    dataLabels: {
                        enabled: false
                    }
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate heatmap charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activity.db'
db = SQLAlchemy(app)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))

@app.route('/activity-data')
def get_activity_data():
    logs = ActivityLog.query.all()
    
    # Process data for heatmap
    data = []
    for log in logs:
        hour = log.timestamp.hour
        day = log.timestamp.weekday()
        data.append([hour, day, round(log.value, 1)])
    
    hours = list(range(24))
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    return jsonify({
        'data': data,
        'hours': hours,
        'days': days
    })
```

## Tips for Working with Heatmap Charts

1. Choose appropriate color scales
2. Consider data density
3. Use clear labels
4. Add informative tooltips
5. Handle missing data
6. Optimize cell sizes
7. Include legends
8. Consider accessibility
