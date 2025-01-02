# Treemap Charts with Highcharts and Flask

## Table of Contents
- [Treemap Charts with Highcharts and Flask](#treemap-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Treemap Charts](#tips-for-working-with-treemap-charts)



## Overview

Treemap charts display hierarchical data using nested rectangles. The size of each rectangle represents a quantitative dimension of the data, while the hierarchical relationship is shown through nesting. They are particularly useful for visualizing hierarchical structures where size matters, such as disk usage, market share by sector, or organizational structures.

## Basic Configuration

Here's how to create a basic treemap chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/treemap-chart')
def treemap_chart():
    return render_template('treemap-chart.html')

@app.route('/treemap-data')
def treemap_data():
    # Sample data: market capitalization by sector
    data = [{
        'id': 'A',
        'name': 'Technology',
        'color': '#7cb5ec'
    }, {
        'id': 'B',
        'name': 'Finance',
        'color': '#434348'
    }, {
        'name': 'Software',
        'parent': 'A',
        'value': 150
    }, {
        'name': 'Hardware',
        'parent': 'A',
        'value': 120
    }, {
        'name': 'Services',
        'parent': 'A',
        'value': 90
    }, {
        'name': 'Banking',
        'parent': 'B',
        'value': 200
    }, {
        'name': 'Insurance',
        'parent': 'B',
        'value': 150
    }, {
        'name': 'Investment',
        'parent': 'B',
        'value': 125
    }]
    
    return jsonify(data)
```

```html
<!-- templates/treemap-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="treemap-container" style="min-width: 310px; height: 500px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/treemap-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('treemap-container', {
                series: [{
                    type: 'treemap',
                    layoutAlgorithm: 'squarified',
                    allowDrillToNode: true,
                    animationLimit: 1000,
                    levels: [{
                        level: 1,
                        dataLabels: {
                            enabled: true
                        },
                        borderWidth: 3
                    }],
                    data: data
                }],
                title: {
                    text: 'Market Share by Sector'
                },
                tooltip: {
                    pointFormat: '<b>{point.name}</b>: {point.value}'
                }
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate treemap charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

class MarketData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent = db.Column(db.String(100))
    value = db.Column(db.Float)
    color = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/market-data')
def get_market_data():
    entries = MarketData.query.all()
    
    data = [{
        'id': entry.id,
        'name': entry.name,
        'parent': entry.parent,
        'value': entry.value,
        'color': entry.color
    } for entry in entries]
    
    return jsonify(data)
```

## Tips for Working with Treemap Charts

1. Choose appropriate sizes
2. Use clear hierarchies
3. Implement proper tooltips
4. Consider color schemes
5. Add drill-down capabilities
6. Handle data updates
7. Optimize performance
8. Use meaningful labels
