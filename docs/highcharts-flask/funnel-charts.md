# Funnel Charts with Highcharts and Flask

## Table of Contents
- [Funnel Charts with Highcharts and Flask](#funnel-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Marketing Funnel with Conversion Rates](#example-1:-marketing-funnel-with-conversion-rates)
  - [Example 2: Sales Pipeline](#example-2:-sales-pipeline)
  - [Example 3: Recruitment Pipeline](#example-3:-recruitment-pipeline)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Funnel Charts](#tips-for-working-with-funnel-charts)



## Overview

Funnel charts are ideal for visualizing stages in a process and showing the progressive reduction of data as it passes through different stages. They are particularly useful for sales pipelines, conversion funnels, and any process where you want to show how values decrease from one stage to the next.

## Basic Configuration

Here's how to create a basic funnel chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/funnel-chart')
def funnel_chart():
    return render_template('funnel-chart.html')

@app.route('/funnel-data')
def funnel_data():
    # Sample sales funnel data
    data = [
        ['Visits', 5000],
        ['Product View', 4000],
        ['Cart', 2000],
        ['Checkout', 1500],
        ['Purchase', 1000]
    ]
    
    return jsonify(data)
```

```html
<!-- templates/funnel-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="funnel-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/funnel-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('funnel-container', {
                chart: {
                    type: 'funnel'
                },
                title: {
                    text: 'Sales Funnel'
                },
                plotOptions: {
                    funnel: {
                        neckWidth: '30%',
                        neckHeight: '25%',
                        width: '70%',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.y:,.0f}',
                            softConnector: true
                        }
                    }
                },
                series: [{
                    name: 'Users',
                    data: data
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Funnel charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        funnel: {
            neckWidth: '30%',        // Width at the bottom
            neckHeight: '25%',       // Height of bottom section
            width: '70%',            // Width at the top
            height: '70%',           // Total height
            reversed: false,         // Direction of funnel
            dataLabels: {
                enabled: true,       // Show labels
                format: '{point.name}: {point.y}',
                softConnector: true, // Curved connector lines
                distance: 30        // Label distance
            },
            center: ['50%', '50%'], // Position in the plot
            showInLegend: true     // Show in legend
        }
    }
});
```

## Example 1: Marketing Funnel with Conversion Rates

This example shows a marketing funnel with conversion rates between stages:

```python
@app.route('/marketing-funnel')
def marketing_funnel():
    # Sample marketing funnel data
    stages = [
        {
            'name': 'Impressions',
            'value': 100000,
            'description': 'Total ad impressions'
        },
        {
            'name': 'Website Visits',
            'value': 20000,
            'description': 'Unique website visitors'
        },
        {
            'name': 'Lead Generation',
            'value': 5000,
            'description': 'Email signups'
        },
        {
            'name': 'Qualified Leads',
            'value': 2000,
            'description': 'Sales-ready leads'
        },
        {
            'name': 'Opportunities',
            'value': 1000,
            'description': 'Sales opportunities'
        },
        {
            'name': 'Closed Deals',
            'value': 500,
            'description': 'Successful conversions'
        }
    ]
    
    # Calculate conversion rates
    for i in range(len(stages)-1):
        conversion = (stages[i+1]['value'] / stages[i]['value']) * 100
        stages[i]['conversion'] = round(conversion, 1)
    stages[-1]['conversion'] = 100
    
    return jsonify(stages)
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
                    type: 'funnel'
                },
                title: {
                    text: 'Marketing Funnel Analysis'
                },
                plotOptions: {
                    funnel: {
                        neckWidth: '20%',
                        neckHeight: '15%',
                        width: '80%',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b><br>Count: {point.y:,.0f}<br>Conversion: {point.conversion}%',
                            softConnector: true,
                            connectorWidth: 2
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.point.name + '</b><br>' +
                               'Count: ' + Highcharts.numberFormat(this.y, 0) + '<br>' +
                               'Description: ' + this.point.description + '<br>' +
                               'Conversion: ' + this.point.conversion + '%';
                    }
                },
                series: [{
                    name: 'Marketing Funnel',
                    data: data.map(stage => ({
                        name: stage.name,
                        y: stage.value,
                        description: stage.description,
                        conversion: stage.conversion
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Sales Pipeline

This example shows a sales pipeline with revenue values:

```python
@app.route('/sales-pipeline')
def sales_pipeline():
    # Sample sales pipeline data
    data = [
        {
            'stage': 'Leads',
            'count': 1000,
            'value': 5000000,
            'probability': 20
        },
        {
            'stage': 'Qualification',
            'count': 500,
            'value': 3000000,
            'probability': 40
        },
        {
            'stage': 'Proposal',
            'count': 200,
            'value': 1500000,
            'probability': 60
        },
        {
            'stage': 'Negotiation',
            'count': 100,
            'value': 1000000,
            'probability': 80
        },
        {
            'stage': 'Closed Won',
            'count': 50,
            'value': 500000,
            'probability': 100
        }
    ]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="pipeline-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/sales-pipeline')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('pipeline-chart', {
                chart: {
                    type: 'funnel'
                },
                title: {
                    text: 'Sales Pipeline'
                },
                plotOptions: {
                    funnel: {
                        neckWidth: '25%',
                        neckHeight: '20%',
                        width: '75%',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.stage}</b><br>' +
                                   'Deals: {point.count}<br>' +
                                   'Value: ${point.value:,.0f}<br>' +
                                   'Probability: {point.probability}%',
                            softConnector: true
                        }
                    }
                },
                series: [{
                    name: 'Opportunities',
                    data: data.map(item => ({
                        name: item.stage,
                        stage: item.stage,
                        y: item.value,
                        count: item.count,
                        value: item.value,
                        probability: item.probability
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Recruitment Pipeline

This example shows a recruitment process funnel:

```python
@app.route('/recruitment-funnel')
def recruitment_funnel():
    # Sample recruitment pipeline data
    stages = [
        {
            'name': 'Applications',
            'count': 500,
            'details': {
                'online': 400,
                'referral': 100
            }
        },
        {
            'name': 'Resume Screening',
            'count': 200,
            'details': {
                'qualified': 150,
                'experience_match': 50
            }
        },
        {
            'name': 'Phone Interview',
            'count': 100,
            'details': {
                'technical_fit': 70,
                'cultural_fit': 30
            }
        },
        {
            'name': 'Technical Test',
            'count': 50,
            'details': {
                'passed': 40,
                'failed': 10
            }
        },
        {
            'name': 'Onsite Interview',
            'count': 30,
            'details': {
                'strong_yes': 15,
                'yes': 15
            }
        },
        {
            'name': 'Offer Extended',
            'count': 20,
            'details': {
                'accepted': 15,
                'negotiating': 5
            }
        }
    ]
    
    return jsonify(stages)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="recruitment-funnel"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/recruitment-funnel')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('recruitment-funnel', {
                chart: {
                    type: 'funnel'
                },
                title: {
                    text: 'Recruitment Pipeline'
                },
                plotOptions: {
                    funnel: {
                        neckWidth: '30%',
                        neckHeight: '25%',
                        width: '70%',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b><br>Candidates: {point.y}',
                            softConnector: true
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        let details = Object.entries(this.point.details)
                            .map(([key, value]) => 
                                key.charAt(0).toUpperCase() + 
                                key.slice(1).replace('_', ' ') + 
                                ': ' + value
                            ).join('<br>');
                        
                        return '<b>' + this.point.name + '</b><br>' +
                               'Total: ' + this.y + '<br><br>' +
                               'Breakdown:<br>' + details;
                    }
                },
                series: [{
                    name: 'Candidates',
                    data: data.map(stage => ({
                        name: stage.name,
                        y: stage.count,
                        details: stage.details
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate funnel charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pipeline.db'
db = SQLAlchemy(app)

class PipelineStage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    probability = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/pipeline-data')
def get_pipeline_data():
    stages = PipelineStage.query.order_by(PipelineStage.order).all()
    
    data = [{
        'name': stage.name,
        'y': stage.count,
        'value': stage.value,
        'probability': stage.probability
    } for stage in stages]
    
    return jsonify(data)
```

## Tips for Working with Funnel Charts

1. Order stages logically
2. Use clear stage names
3. Show conversion rates
4. Consider using tooltips
5. Choose appropriate widths
6. Use meaningful colors
7. Include relevant metrics
8. Optimize label placement
