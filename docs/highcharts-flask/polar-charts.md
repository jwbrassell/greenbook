# Polar Charts with Highcharts and Flask

## Table of Contents
- [Polar Charts with Highcharts and Flask](#polar-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Product Comparison](#example-1:-product-comparison)
  - [Example 2: Weather Patterns](#example-2:-weather-patterns)
  - [Example 3: Skill Assessment](#example-3:-skill-assessment)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Polar Charts](#tips-for-working-with-polar-charts)



## Overview

Polar charts (also known as radar or spider charts) are ideal for visualizing multivariate data in a circular format. They are particularly useful for comparing multiple variables or showing cyclic patterns, such as seasonal data, performance metrics, or data with angular components.

## Basic Configuration

Here's how to create a basic polar chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/polar-chart')
def polar_chart():
    return render_template('polar-chart.html')

@app.route('/polar-data')
def polar_data():
    # Sample performance metrics
    data = [
        ['Speed', 80],
        ['Reliability', 95],
        ['Comfort', 85],
        ['Safety', 90],
        ['Efficiency', 75],
        ['Cost', 70]
    ]
    
    return jsonify(data)
```

```html
<!-- templates/polar-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="polar-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/polar-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('polar-container', {
                chart: {
                    polar: true,
                    type: 'line'
                },
                title: {
                    text: 'Performance Metrics'
                },
                pane: {
                    size: '80%'
                },
                xAxis: {
                    categories: data.map(item => item[0]),
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },
                yAxis: {
                    gridLineInterpolation: 'polygon',
                    lineWidth: 0,
                    min: 0,
                    max: 100
                },
                tooltip: {
                    shared: true,
                    pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
                },
                series: [{
                    name: 'Score',
                    data: data.map(item => item[1]),
                    pointPlacement: 'on'
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Polar charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    chart: {
        polar: true,
        type: 'line'  // 'line', 'area', 'column', etc.
    },
    pane: {
        size: '80%',  // Chart size relative to container
        startAngle: 0, // Starting angle
        endAngle: 360 // Ending angle
    },
    xAxis: {
        tickmarkPlacement: 'on',
        lineWidth: 0,
        gridLineWidth: 1
    },
    yAxis: {
        gridLineInterpolation: 'polygon', // 'polygon' or 'circle'
        lineWidth: 0,
        min: 0,
        max: 100,
        tickInterval: 20
    },
    plotOptions: {
        series: {
            pointPlacement: 'on',
            showInLegend: true
        }
    }
});
```

## Example 1: Product Comparison

This example shows a comparison of multiple products across different attributes:

```python
@app.route('/product-comparison')
def product_comparison():
    # Sample product comparison data
    categories = ['Performance', 'Quality', 'Features', 'Price', 'Support', 'Usability']
    
    data = {
        'categories': categories,
        'products': [
            {
                'name': 'Product A',
                'data': [90, 85, 95, 70, 88, 92]
            },
            {
                'name': 'Product B',
                'data': [80, 95, 85, 90, 75, 88]
            },
            {
                'name': 'Product C',
                'data': [85, 80, 90, 85, 95, 78]
            }
        ]
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="comparison-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/product-comparison')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('comparison-chart', {
                chart: {
                    polar: true,
                    type: 'line'
                },
                title: {
                    text: 'Product Comparison'
                },
                pane: {
                    size: '80%'
                },
                xAxis: {
                    categories: data.categories,
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },
                yAxis: {
                    gridLineInterpolation: 'polygon',
                    lineWidth: 0,
                    min: 0,
                    max: 100,
                    tickInterval: 20
                },
                tooltip: {
                    shared: true,
                    pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
                },
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
                series: data.products.map(product => ({
                    name: product.name,
                    data: product.data,
                    pointPlacement: 'on'
                }))
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Weather Patterns

This example shows weather patterns over a 24-hour period:

```python
@app.route('/weather-patterns')
def weather_patterns():
    # Sample 24-hour weather data
    hours = [f'{i:02d}:00' for i in range(24)]
    
    data = {
        'hours': hours,
        'metrics': [
            {
                'name': 'Temperature (°C)',
                'data': [15, 14, 13, 12, 11, 10, 12, 14, 16, 18, 
                        20, 22, 23, 24, 24, 23, 22, 20, 19, 18, 
                        17, 16, 15, 14]
            },
            {
                'name': 'Humidity (%)',
                'data': [60, 62, 65, 68, 70, 72, 75, 73, 70, 65,
                        60, 55, 50, 48, 47, 48, 50, 52, 55, 57,
                        58, 59, 60, 61]
            }
        ]
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="weather-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/weather-patterns')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('weather-chart', {
                chart: {
                    polar: true
                },
                title: {
                    text: '24-Hour Weather Pattern'
                },
                pane: {
                    size: '80%'
                },
                xAxis: {
                    categories: data.hours,
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },
                yAxis: {
                    gridLineInterpolation: 'polygon',
                    lineWidth: 0,
                    min: 0
                },
                tooltip: {
                    shared: true,
                    formatter: function() {
                        return this.points.reduce((s, point) => {
                            return s + '<br/>' + point.series.name + ': <b>' + 
                                   point.y + (point.series.name.includes('Temperature') ? '°C' : '%') + '</b>';
                        }, '<b>' + this.x + '</b>');
                    }
                },
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
                series: data.metrics.map(metric => ({
                    name: metric.name,
                    data: metric.data,
                    pointPlacement: 'on',
                    type: 'line'
                }))
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Skill Assessment

This example shows a skill assessment radar chart:

```python
@app.route('/skill-assessment')
def skill_assessment():
    skills = [
        {
            'category': 'Technical',
            'skills': [
                {'name': 'Programming', 'level': 90},
                {'name': 'Database', 'level': 85},
                {'name': 'DevOps', 'level': 75},
                {'name': 'Security', 'level': 80}
            ]
        },
        {
            'category': 'Soft Skills',
            'skills': [
                {'name': 'Communication', 'level': 85},
                {'name': 'Leadership', 'level': 80},
                {'name': 'Teamwork', 'level': 95},
                {'name': 'Problem Solving', 'level': 90}
            ]
        }
    ]
    
    return jsonify(skills)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="skills-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/skill-assessment')
        .then(response => response.json())
        .then(data => {
            const allSkills = data.reduce((acc, category) => {
                return acc.concat(category.skills.map(skill => skill.name));
            }, []);
            
            const series = data.map(category => ({
                name: category.category,
                data: category.skills.map(skill => skill.level),
                pointPlacement: 'on'
            }));
            
            Highcharts.chart('skills-chart', {
                chart: {
                    polar: true,
                    type: 'area'
                },
                title: {
                    text: 'Skill Assessment'
                },
                pane: {
                    size: '80%'
                },
                xAxis: {
                    categories: allSkills,
                    tickmarkPlacement: 'on',
                    lineWidth: 0
                },
                yAxis: {
                    gridLineInterpolation: 'polygon',
                    lineWidth: 0,
                    min: 0,
                    max: 100,
                    tickInterval: 20
                },
                tooltip: {
                    shared: true,
                    pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y}%</b><br/>'
                },
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
                series: series,
                plotOptions: {
                    area: {
                        fillOpacity: 0.3
                    }
                }
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate polar charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metrics.db'
db = SQLAlchemy(app)

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/metric-data')
def get_metric_data():
    metrics = Metric.query.order_by(Metric.category, Metric.name).all()
    
    # Group metrics by category
    categories = {}
    for metric in metrics:
        if metric.category not in categories:
            categories[metric.category] = []
        categories[metric.category].append({
            'name': metric.name,
            'value': metric.value
        })
    
    # Format data for chart
    data = {
        'categories': list(set(m.name for m in metrics)),
        'series': [{
            'name': category,
            'data': [m['value'] for m in metrics]
        } for category, metrics in categories.items()]
    }
    
    return jsonify(data)
```

## Tips for Working with Polar Charts

1. Choose appropriate scales
2. Use clear categories
3. Consider data density
4. Implement proper tooltips
5. Use meaningful colors
6. Handle overlapping
7. Add proper legends
8. Optimize readability
