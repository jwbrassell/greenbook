# Pyramid Charts with Highcharts and Flask

## Table of Contents
- [Pyramid Charts with Highcharts and Flask](#pyramid-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Marketing Funnel](#example-1:-marketing-funnel)
  - [Example 2: Organization Hierarchy](#example-2:-organization-hierarchy)
  - [Example 3: Customer Segmentation](#example-3:-customer-segmentation)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Pyramid Charts](#tips-for-working-with-pyramid-charts)



## Overview

Pyramid charts are ideal for visualizing hierarchical data in a pyramid shape, where each level represents a part of a whole, and levels are typically ordered by size. They are particularly useful for showing organizational structures, population demographics, or marketing funnels where the width of each level represents its value.

## Basic Configuration

Here's how to create a basic pyramid chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/pyramid-chart')
def pyramid_chart():
    return render_template('pyramid-chart.html')

@app.route('/pyramid-data')
def pyramid_data():
    # Sample demographic data
    data = [
        ['65+', 15],
        ['45-64', 30],
        ['25-44', 45],
        ['15-24', 25],
        ['0-14', 20]
    ]
    
    return jsonify(data)
```

```html
<!-- templates/pyramid-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="pyramid-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/pyramid-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('pyramid-container', {
                chart: {
                    type: 'pyramid'
                },
                title: {
                    text: 'Population Distribution'
                },
                plotOptions: {
                    pyramid: {
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b> ({point.y:,.0f})',
                            softConnector: true
                        },
                        width: '60%'
                    }
                },
                series: [{
                    name: 'Population',
                    data: data
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Pyramid charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        pyramid: {
            width: '60%',          // Width of the pyramid
            height: '80%',         // Height of the pyramid
            neckWidth: '30%',      // Width at the top
            neckHeight: '25%',     // Height of the top section
            reversed: false,       // Reverse the pyramid direction
            dataLabels: {
                enabled: true,     // Show data labels
                format: '{point.name}: {point.y}',
                softConnector: true // Use curved connector lines
            },
            center: ['50%', '50%'], // Position in the plot
            showInLegend: true    // Show in legend
        }
    }
});
```

## Example 1: Marketing Funnel

This example shows a marketing funnel with conversion rates:

```python
@app.route('/marketing-funnel')
def marketing_funnel():
    data = [
        {
            'name': 'Website Visits',
            'y': 15000,
            'description': 'Total unique visitors'
        },
        {
            'name': 'Product Views',
            'y': 12000,
            'description': 'Visitors who viewed products'
        },
        {
            'name': 'Add to Cart',
            'y': 8000,
            'description': 'Products added to cart'
        },
        {
            'name': 'Checkout',
            'y': 4000,
            'description': 'Started checkout process'
        },
        {
            'name': 'Purchase',
            'y': 2000,
            'description': 'Completed purchases'
        }
    ]
    
    # Calculate conversion rates
    for i in range(len(data)-1):
        current = data[i]['y']
        next_step = data[i+1]['y']
        conversion = (next_step / current) * 100
        data[i]['conversion'] = round(conversion, 1)
    
    data[-1]['conversion'] = 100
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="marketing-funnel"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/marketing-funnel')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('marketing-funnel', {
                chart: {
                    type: 'pyramid'
                },
                title: {
                    text: 'Marketing Funnel Analysis'
                },
                plotOptions: {
                    pyramid: {
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return '<b>' + this.point.name + '</b><br>' +
                                       'Count: ' + this.y.toLocaleString() + '<br>' +
                                       'Conversion: ' + this.point.conversion + '%';
                            },
                            style: {
                                fontWeight: 'normal',
                                fontSize: '11px'
                            }
                        },
                        width: '60%',
                        colorByPoint: true
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.point.name + '</b><br>' +
                               'Count: ' + this.y.toLocaleString() + '<br>' +
                               'Conversion: ' + this.point.conversion + '%<br>' +
                               'Description: ' + this.point.description;
                    }
                },
                series: [{
                    name: 'Marketing Funnel',
                    data: data
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Organization Hierarchy

This example shows an organizational structure with employee counts:

```python
@app.route('/org-hierarchy')
def org_hierarchy():
    data = [
        {
            'name': 'Executive',
            'y': 5,
            'description': 'C-level executives',
            'level': 'Top Management'
        },
        {
            'name': 'Senior Management',
            'y': 15,
            'description': 'Department heads',
            'level': 'Management'
        },
        {
            'name': 'Middle Management',
            'y': 45,
            'description': 'Team leaders',
            'level': 'Management'
        },
        {
            'name': 'Professional Staff',
            'y': 200,
            'description': 'Skilled professionals',
            'level': 'Staff'
        },
        {
            'name': 'Support Staff',
            'y': 350,
            'description': 'Support personnel',
            'level': 'Staff'
        }
    ]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="org-hierarchy"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/org-hierarchy')
        .then(response => response.json())
        .then(data => {
            const levelColors = {
                'Top Management': '#ff7f0e',
                'Management': '#2ca02c',
                'Staff': '#1f77b4'
            };
            
            Highcharts.chart('org-hierarchy', {
                chart: {
                    type: 'pyramid'
                },
                title: {
                    text: 'Organizational Structure'
                },
                plotOptions: {
                    pyramid: {
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return '<b>' + this.point.name + '</b><br>' +
                                       'Employees: ' + this.y;
                            }
                        },
                        width: '60%'
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.point.name + '</b><br>' +
                               'Employees: ' + this.y + '<br>' +
                               'Level: ' + this.point.level + '<br>' +
                               'Description: ' + this.point.description;
                    }
                },
                series: [{
                    name: 'Organization',
                    data: data.map(item => ({
                        name: item.name,
                        y: item.y,
                        level: item.level,
                        description: item.description,
                        color: levelColors[item.level]
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Customer Segmentation

This example shows customer segmentation by value:

```python
@app.route('/customer-segments')
def customer_segments():
    data = [
        {
            'name': 'Premium',
            'y': 100,
            'value': 500000,
            'avgSpend': 5000,
            'category': 'High Value'
        },
        {
            'name': 'Regular',
            'y': 500,
            'value': 1000000,
            'avgSpend': 2000,
            'category': 'Medium Value'
        },
        {
            'name': 'Occasional',
            'y': 2000,
            'value': 1500000,
            'avgSpend': 750,
            'category': 'Low Value'
        },
        {
            'name': 'One-time',
            'y': 5000,
            'value': 1000000,
            'avgSpend': 200,
            'category': 'Low Value'
        }
    ]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="customer-segments"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/customer-segments')
        .then(response => response.json())
        .then(data => {
            const categoryColors = {
                'High Value': '#2ca02c',
                'Medium Value': '#7cb5ec',
                'Low Value': '#90ed7d'
            };
            
            Highcharts.chart('customer-segments', {
                chart: {
                    type: 'pyramid'
                },
                title: {
                    text: 'Customer Segmentation'
                },
                plotOptions: {
                    pyramid: {
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return '<b>' + this.point.name + '</b><br>' +
                                       'Customers: ' + this.y.toLocaleString();
                            }
                        },
                        width: '60%'
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.point.name + ' Customers</b><br>' +
                               'Count: ' + this.y.toLocaleString() + '<br>' +
                               'Total Value: $' + this.point.value.toLocaleString() + '<br>' +
                               'Avg. Spend: $' + this.point.avgSpend.toLocaleString() + '<br>' +
                               'Category: ' + this.point.category;
                    }
                },
                series: [{
                    name: 'Customers',
                    data: data.map(item => ({
                        ...item,
                        color: categoryColors[item.category]
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate pyramid charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///segments.db'
db = SQLAlchemy(app)

class Segment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/segment-data')
def get_segment_data():
    segments = Segment.query.order_by(Segment.count.desc()).all()
    
    data = [{
        'name': segment.name,
        'y': segment.count,
        'value': segment.value,
        'category': segment.category,
        'description': segment.description
    } for segment in segments]
    
    return jsonify(data)
```

## Tips for Working with Pyramid Charts

1. Order levels logically
2. Use clear labels
3. Choose meaningful colors
4. Consider proportions
5. Add informative tooltips
6. Use appropriate width
7. Include relevant metrics
8. Optimize readability
