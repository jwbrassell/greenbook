# Bar Charts with Highcharts and Flask

## Table of Contents
- [Bar Charts with Highcharts and Flask](#bar-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Market Share Analysis](#example-1:-market-share-analysis)
  - [Example 2: Survey Results](#example-2:-survey-results)
  - [Example 3: Resource Allocation](#example-3:-resource-allocation)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Bar Charts](#tips-for-working-with-bar-charts)



## Overview

Bar charts are similar to column charts but with horizontal bars instead of vertical columns. They are particularly effective when dealing with longer category names, comparing many categories, or showing data that develops over longer time periods. Bar charts can also be stacked or grouped to show multiple data series.

## Basic Configuration

Here's how to create a basic bar chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/bar-chart')
def bar_chart():
    return render_template('bar-chart.html')

@app.route('/bar-data')
def bar_data():
    # Sample data for top programming languages
    data = [
        ['Python', 32.8],
        ['JavaScript', 24.3],
        ['Java', 21.5],
        ['C++', 18.7],
        ['C#', 17.4],
        ['PHP', 15.2],
        ['Ruby', 8.9],
        ['Swift', 8.1]
    ]
    
    return jsonify(data)
```

```html
<!-- templates/bar-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="bar-container" style="min-width: 310px; height: 500px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/bar-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('bar-container', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Programming Language Usage'
                },
                xAxis: {
                    categories: data.map(item => item[0]),
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Usage (%)',
                        align: 'high'
                    }
                },
                tooltip: {
                    valueSuffix: '%'
                },
                plotOptions: {
                    bar: {
                        dataLabels: {
                            enabled: true,
                            format: '{y}%'
                        }
                    }
                },
                series: [{
                    name: 'Usage',
                    data: data.map(item => item[1])
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Bar charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        bar: {
            pointPadding: 0.2,     // Space between bars
            groupPadding: 0.2,     // Space between bar sets
            borderWidth: 0,        // Bar border width
            borderRadius: 0,       // Bar corner radius
            colorByPoint: false,   // Different color for each bar
            grouping: true,       // Group bars
            stacking: null,       // null, 'normal', or 'percent'
            dataLabels: {
                enabled: false,    // Show value labels
                format: '{y}'     // Label format
            },
            states: {
                hover: {
                    brightness: 0.1 // Brightness change on hover
                }
            }
        }
    }
});
```

## Example 1: Market Share Analysis

This example shows market share comparison across different regions:

```python
@app.route('/market-share')
def market_share():
    data = {
        'regions': ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East'],
        'companies': [
            {
                'name': 'Company A',
                'data': [35, 28, 42, 25, 18]
            },
            {
                'name': 'Company B',
                'data': [25, 32, 28, 30, 22]
            },
            {
                'name': 'Company C',
                'data': [20, 25, 15, 28, 35]
            }
        ]
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="market-share"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/market-share')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('market-share', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Market Share by Region'
                },
                xAxis: {
                    categories: data.regions
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Market Share (%)'
                    }
                },
                legend: {
                    reversed: true
                },
                plotOptions: {
                    series: {
                        stacking: 'normal',
                        dataLabels: {
                            enabled: true,
                            format: '{y}%'
                        }
                    }
                },
                series: data.companies.map(company => ({
                    name: company.name,
                    data: company.data
                }))
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Survey Results

This example shows survey results with positive and negative responses:

```python
@app.route('/survey-results')
def survey_results():
    data = {
        'questions': [
            'Overall Satisfaction',
            'Product Quality',
            'Customer Service',
            'Value for Money',
            'Would Recommend',
            'Ease of Use'
        ],
        'responses': [
            {
                'name': 'Satisfied',
                'data': [75, 82, 68, 71, 80, 85]
            },
            {
                'name': 'Neutral',
                'data': [15, 10, 20, 18, 12, 8]
            },
            {
                'name': 'Dissatisfied',
                'data': [10, 8, 12, 11, 8, 7]
            }
        ]
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="survey-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/survey-results')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('survey-chart', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Customer Survey Results'
                },
                xAxis: {
                    categories: data.questions
                },
                yAxis: {
                    min: 0,
                    max: 100,
                    title: {
                        text: 'Responses (%)'
                    }
                },
                legend: {
                    reversed: true
                },
                plotOptions: {
                    series: {
                        stacking: 'percent',
                        dataLabels: {
                            enabled: true,
                            format: '{y}%'
                        }
                    }
                },
                series: data.responses.map(response => ({
                    name: response.name,
                    data: response.data,
                    color: response.name === 'Satisfied' ? '#28a745' :
                           response.name === 'Neutral' ? '#ffc107' : '#dc3545'
                }))
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Resource Allocation

This example shows resource allocation across different departments:

```python
@app.route('/resource-allocation')
def resource_allocation():
    data = {
        'departments': [
            'Research & Development',
            'Sales & Marketing',
            'Customer Support',
            'Human Resources',
            'IT Infrastructure',
            'Administration',
            'Operations'
        ],
        'resources': [
            {
                'name': 'Budget',
                'data': [250000, 180000, 120000, 80000, 150000, 90000, 200000]
            },
            {
                'name': 'Staff',
                'data': [45, 35, 25, 15, 20, 10, 40]
            }
        ]
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="resource-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/resource-allocation')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('resource-chart', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Departmental Resource Allocation'
                },
                xAxis: {
                    categories: data.departments
                },
                yAxis: [{
                    title: {
                        text: 'Budget ($)'
                    },
                    labels: {
                        format: '${value:,.0f}'
                    }
                }, {
                    title: {
                        text: 'Staff Count'
                    },
                    opposite: true
                }],
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.x + '</b><br/>' +
                               this.series.name + ': ' + 
                               (this.series.name === 'Budget' ? 
                                   '$' + Highcharts.numberFormat(this.y, 0) :
                                   this.y + ' employees');
                    }
                },
                plotOptions: {
                    bar: {
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return this.series.name === 'Budget' ?
                                    '$' + Highcharts.numberFormat(this.y, 0) :
                                    this.y;
                            }
                        }
                    }
                },
                series: [{
                    name: 'Budget',
                    data: data.resources[0].data,
                    yAxis: 0
                }, {
                    name: 'Staff',
                    data: data.resources[1].data,
                    yAxis: 1
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate bar charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resources.db'
db = SQLAlchemy(app)

class DepartmentResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/department-data')
def get_department_data():
    resources = db.session.query(
        DepartmentResource.department,
        DepartmentResource.resource_type,
        db.func.sum(DepartmentResource.value).label('total')
    ).group_by(
        DepartmentResource.department,
        DepartmentResource.resource_type
    ).all()
    
    # Format data for chart
    departments = sorted(list(set(r.department for r in resources)))
    resource_types = sorted(list(set(r.resource_type for r in resources)))
    
    series = []
    for resource_type in resource_types:
        series_data = []
        for department in departments:
            resource = next((r for r in resources 
                           if r.department == department and 
                           r.resource_type == resource_type), None)
            series_data.append(float(resource.total) if resource else 0)
        
        series.append({
            'name': resource_type,
            'data': series_data
        })
    
    return jsonify({
        'categories': departments,
        'series': series
    })
```

## Tips for Working with Bar Charts

1. Order bars meaningfully
2. Use appropriate spacing
3. Consider label placement
4. Implement clear tooltips
5. Handle long labels
6. Choose effective colors
7. Use stacking when appropriate
8. Optimize for readability
