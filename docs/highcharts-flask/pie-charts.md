# Pie Charts with Highcharts and Flask

## Table of Contents
- [Pie Charts with Highcharts and Flask](#pie-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Revenue Distribution](#example-1:-revenue-distribution)
  - [Example 2: Budget Allocation](#example-2:-budget-allocation)
  - [Example 3: Semi-Circle Chart](#example-3:-semi-circle-chart)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Pie Charts](#tips-for-working-with-pie-charts)



## Overview

Pie charts are ideal for showing proportional parts of a whole, where each slice represents a percentage of the total. They are particularly effective when you want to show composition and make part-to-whole relationships immediately visible. Pie charts can also be enhanced with features like donut style, semi-circle display, or drill-down capabilities.

## Basic Configuration

Here's how to create a basic pie chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/pie-chart')
def pie_chart():
    return render_template('pie-chart.html')

@app.route('/pie-data')
def pie_data():
    # Sample data for browser market share
    data = [
        {
            'name': 'Chrome',
            'y': 64.92
        },
        {
            'name': 'Safari',
            'y': 19.33
        },
        {
            'name': 'Firefox',
            'y': 3.89
        },
        {
            'name': 'Edge',
            'y': 3.57
        },
        {
            'name': 'Opera',
            'y': 2.03
        },
        {
            'name': 'Other',
            'y': 6.26
        }
    ]
    
    return jsonify(data)
```

```html
<!-- templates/pie-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="pie-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/pie-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('pie-container', {
                chart: {
                    type: 'pie'
                },
                title: {
                    text: 'Browser Market Share'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f}%'
                        }
                    }
                },
                series: [{
                    name: 'Market Share',
                    colorByPoint: true,
                    data: data
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Pie charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        pie: {
            allowPointSelect: true,    // Enable slice selection
            cursor: 'pointer',         // Cursor style on hover
            depth: 35,                 // 3D effect depth
            startAngle: 0,            // Starting angle
            endAngle: 360,           // Ending angle (for semi-circle)
            center: ['50%', '50%'],   // Center position
            size: '80%',              // Chart size
            innerSize: '0%',          // For donut charts
            showInLegend: true,       // Show legend
            dataLabels: {
                enabled: true,         // Show labels
                distance: 30,          // Label distance from edge
                format: '{point.name}: {point.percentage:.1f}%'
            },
            slicedOffset: 20         // Distance when slice is pulled out
        }
    }
});
```

## Example 1: Revenue Distribution

This example shows revenue distribution with drill-down capability:

```python
@app.route('/revenue-distribution')
def revenue_distribution():
    data = {
        'main': [
            {
                'name': 'Products',
                'y': 56.33,
                'drilldown': 'products'
            },
            {
                'name': 'Services',
                'y': 24.03,
                'drilldown': 'services'
            },
            {
                'name': 'Subscriptions',
                'y': 19.64,
                'drilldown': 'subscriptions'
            }
        ],
        'drilldown': {
            'products': {
                'name': 'Products',
                'data': [
                    ['Electronics', 20.12],
                    ['Clothing', 15.83],
                    ['Accessories', 12.24],
                    ['Home & Garden', 8.14]
                ]
            },
            'services': {
                'name': 'Services',
                'data': [
                    ['Consulting', 10.15],
                    ['Installation', 7.88],
                    ['Maintenance', 6.00]
                ]
            },
            'subscriptions': {
                'name': 'Subscriptions',
                'data': [
                    ['Premium', 8.54],
                    ['Standard', 7.20],
                    ['Basic', 3.90]
                ]
            }
        }
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="revenue-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/revenue-distribution')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('revenue-chart', {
                chart: {
                    type: 'pie'
                },
                title: {
                    text: 'Revenue Distribution'
                },
                subtitle: {
                    text: 'Click slices to view details'
                },
                plotOptions: {
                    series: {
                        dataLabels: {
                            enabled: true,
                            format: '{point.name}: {point.y:.1f}%'
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.1f}%</b> of total<br/>'
                },
                series: [{
                    name: 'Revenue Sources',
                    colorByPoint: true,
                    data: data.main
                }],
                drilldown: {
                    series: Object.entries(data.drilldown).map(([id, details]) => ({
                        id: id,
                        name: details.name,
                        data: details.data
                    }))
                }
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Budget Allocation

This example shows budget allocation with a donut chart style:

```python
@app.route('/budget-allocation')
def budget_allocation():
    data = [
        {
            'name': 'Development',
            'y': 35,
            'color': '#7cb5ec'
        },
        {
            'name': 'Marketing',
            'y': 25,
            'color': '#434348'
        },
        {
            'name': 'Operations',
            'y': 20,
            'color': '#90ed7d'
        },
        {
            'name': 'Support',
            'y': 15,
            'color': '#f7a35c'
        },
        {
            'name': 'Training',
            'y': 5,
            'color': '#8085e9'
        }
    ]
    
    total_budget = 1000000  # $1M total budget
    
    # Calculate absolute values
    for item in data:
        item['value'] = total_budget * (item['y'] / 100)
    
    return jsonify({
        'data': data,
        'total': total_budget
    })
```

```html
{% extends "base.html" %}

{% block content %}
<div id="budget-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/budget-allocation')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('budget-chart', {
                chart: {
                    type: 'pie'
                },
                title: {
                    text: 'Budget Allocation',
                    align: 'center',
                    verticalAlign: 'middle',
                    y: 0
                },
                subtitle: {
                    text: `Total: $${Highcharts.numberFormat(data.total, 0)}`,
                    align: 'center',
                    verticalAlign: 'middle',
                    y: 25
                },
                plotOptions: {
                    pie: {
                        innerSize: '50%',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>:<br>${point.value:,.0f}<br>({point.percentage:.1f}%)',
                            distance: 20,
                            filter: {
                                property: 'percentage',
                                operator: '>',
                                value: 4
                            }
                        },
                        showInLegend: true
                    }
                },
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
                series: [{
                    name: 'Budget',
                    data: data.data
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Semi-Circle Chart

This example shows a semi-circle chart for progress or gauge-like visualization:

```python
@app.route('/project-status')
def project_status():
    data = [
        {
            'name': 'Completed',
            'y': 65,
            'color': '#28a745'
        },
        {
            'name': 'In Progress',
            'y': 25,
            'color': '#ffc107'
        },
        {
            'name': 'Not Started',
            'y': 10,
            'color': '#dc3545'
        }
    ]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="status-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/project-status')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('status-chart', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: 0,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'Project<br>Status',
                    align: 'center',
                    verticalAlign: 'middle',
                    y: 60
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        dataLabels: {
                            enabled: true,
                            distance: -50,
                            style: {
                                fontWeight: 'bold',
                                color: 'white'
                            }
                        },
                        startAngle: -90,
                        endAngle: 90,
                        center: ['50%', '75%'],
                        size: '110%'
                    }
                },
                series: [{
                    type: 'pie',
                    name: 'Progress',
                    innerSize: '50%',
                    data: data
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate pie charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)

class ProjectTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/task-data')
def get_task_data():
    tasks = db.session.query(
        ProjectTask.status,
        db.func.sum(ProjectTask.hours).label('total_hours')
    ).group_by(
        ProjectTask.status
    ).all()
    
    # Calculate percentages
    total_hours = sum(task.total_hours for task in tasks)
    
    data = [{
        'name': task.status,
        'y': (task.total_hours / total_hours) * 100,
        'hours': task.total_hours
    } for task in tasks]
    
    return jsonify(data)
```

## Tips for Working with Pie Charts

1. Limit number of slices
2. Order slices meaningfully
3. Use clear colors
4. Consider data labels
5. Add useful tooltips
6. Use legends effectively
7. Consider donut style
8. Handle small segments
