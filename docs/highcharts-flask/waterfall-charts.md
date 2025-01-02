# Waterfall Charts with Highcharts and Flask

## Table of Contents
- [Waterfall Charts with Highcharts and Flask](#waterfall-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Monthly Budget Analysis](#example-1:-monthly-budget-analysis)
  - [Example 2: Project Cost Breakdown](#example-2:-project-cost-breakdown)
  - [Example 3: Sales Performance Analysis](#example-3:-sales-performance-analysis)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Waterfall Charts](#tips-for-working-with-waterfall-charts)



## Overview

Waterfall charts are ideal for visualizing the cumulative effect of sequential positive and negative values. They are particularly useful for financial data, showing how an initial value is affected by a series of intermediate positive or negative values, leading to a final value.

## Basic Configuration

Here's how to create a basic waterfall chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/waterfall-chart')
def waterfall_chart():
    return render_template('waterfall-chart.html')

@app.route('/waterfall-data')
def waterfall_data():
    # Sample financial data
    data = [
        {
            'name': 'Initial Balance',
            'y': 120000,
            'isSum': True
        },
        {
            'name': 'Revenue',
            'y': 50000
        },
        {
            'name': 'Operating Costs',
            'y': -30000
        },
        {
            'name': 'Tax',
            'y': -12000
        },
        {
            'name': 'Final Balance',
            'isIntermediateSum': True
        }
    ]
    
    return jsonify(data)
```

```html
<!-- templates/waterfall-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="waterfall-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/waterfall-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('waterfall-container', {
                chart: {
                    type: 'waterfall'
                },
                title: {
                    text: 'Financial Summary'
                },
                xAxis: {
                    type: 'category'
                },
                yAxis: {
                    title: {
                        text: 'USD'
                    },
                    labels: {
                        formatter: function() {
                            return '$' + this.value.toLocaleString();
                        }
                    }
                },
                tooltip: {
                    pointFormat: '<b>${point.y:,.0f}</b>'
                },
                plotOptions: {
                    waterfall: {
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return '$' + this.y.toLocaleString();
                            }
                        }
                    }
                },
                series: [{
                    upColor: Highcharts.getOptions().colors[2],
                    color: Highcharts.getOptions().colors[3],
                    data: data,
                    pointPadding: 0
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Waterfall charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        waterfall: {
            upColor: '#90ed7d',      // Color for positive values
            color: '#f7a35c',        // Color for negative values
            borderColor: '#333333',   // Border color
            borderWidth: 1,          // Border width
            dataLabels: {
                enabled: true,       // Show value labels
                style: {
                    fontWeight: 'bold'
                },
                position: 'center'   // Label position
            },
            pointPadding: 0,        // Space between columns
            lineWidth: 1            // Connector line width
        }
    }
});
```

## Example 1: Monthly Budget Analysis

This example shows a monthly budget breakdown:

```python
@app.route('/budget-analysis')
def budget_analysis():
    data = [
        {
            'name': 'Starting Balance',
            'y': 5000,
            'isSum': True,
            'color': '#7cb5ec'
        },
        {
            'name': 'Salary',
            'y': 4000,
            'color': '#90ed7d'
        },
        {
            'name': 'Rent',
            'y': -1500,
            'color': '#f45b5b'
        },
        {
            'name': 'Utilities',
            'y': -300,
            'color': '#f45b5b'
        },
        {
            'name': 'Groceries',
            'y': -600,
            'color': '#f45b5b'
        },
        {
            'name': 'Transportation',
            'y': -200,
            'color': '#f45b5b'
        },
        {
            'name': 'Entertainment',
            'y': -400,
            'color': '#f45b5b'
        },
        {
            'name': 'Savings',
            'isIntermediateSum': True,
            'color': '#434348'
        }
    ]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="budget-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/budget-analysis')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('budget-chart', {
                chart: {
                    type: 'waterfall'
                },
                title: {
                    text: 'Monthly Budget Analysis'
                },
                xAxis: {
                    type: 'category'
                },
                yAxis: {
                    title: {
                        text: 'Amount ($)'
                    },
                    labels: {
                        formatter: function() {
                            return '$' + this.value.toLocaleString();
                        }
                    }
                },
                tooltip: {
                    pointFormat: '<b>${point.y:,.2f}</b>'
                },
                plotOptions: {
                    waterfall: {
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return '$' + this.y.toLocaleString();
                            },
                            style: {
                                fontWeight: 'bold'
                            }
                        }
                    }
                },
                series: [{
                    data: data,
                    pointPadding: 0
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Project Cost Breakdown

This example shows a project's cost structure:

```python
@app.route('/project-costs')
def project_costs():
    data = [
        {
            'name': 'Total Budget',
            'y': 100000,
            'isSum': True
        },
        {
            'name': 'Planning Phase',
            'y': -15000,
            'description': 'Initial planning and design'
        },
        {
            'name': 'Development',
            'y': -45000,
            'description': 'Core development work'
        },
        {
            'name': 'Testing',
            'y': -12000,
            'description': 'QA and testing'
        },
        {
            'name': 'Deployment',
            'y': -8000,
            'description': 'System deployment'
        },
        {
            'name': 'Training',
            'y': -5000,
            'description': 'Staff training'
        },
        {
            'name': 'Remaining Budget',
            'isIntermediateSum': True,
            'description': 'Available for contingencies'
        }
    ]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="project-costs"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/project-costs')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('project-costs', {
                chart: {
                    type: 'waterfall'
                },
                title: {
                    text: 'Project Cost Breakdown'
                },
                xAxis: {
                    type: 'category'
                },
                yAxis: {
                    title: {
                        text: 'Cost ($)'
                    },
                    labels: {
                        formatter: function() {
                            return '$' + this.value.toLocaleString();
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        let tooltip = '<b>' + this.point.name + '</b><br>';
                        tooltip += 'Amount: $' + this.y.toLocaleString() + '<br>';
                        if (this.point.description) {
                            tooltip += this.point.description;
                        }
                        return tooltip;
                    }
                },
                plotOptions: {
                    waterfall: {
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return '$' + this.y.toLocaleString();
                            }
                        }
                    }
                },
                series: [{
                    data: data,
                    pointPadding: 0
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Sales Performance Analysis

This example shows a sales performance breakdown with multiple factors:

```python
@app.route('/sales-performance')
def sales_performance():
    data = [
        {
            'name': 'Previous Year',
            'y': 1000000,
            'isSum': True
        },
        {
            'name': 'New Customers',
            'y': 250000,
            'category': 'Growth'
        },
        {
            'name': 'Lost Customers',
            'y': -150000,
            'category': 'Loss'
        },
        {
            'name': 'Price Increases',
            'y': 100000,
            'category': 'Growth'
        },
        {
            'name': 'Discounts',
            'y': -75000,
            'category': 'Loss'
        },
        {
            'name': 'Market Expansion',
            'y': 200000,
            'category': 'Growth'
        },
        {
            'name': 'Current Year',
            'isIntermediateSum': True
        }
    ]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="sales-performance"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/sales-performance')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('sales-performance', {
                chart: {
                    type: 'waterfall'
                },
                title: {
                    text: 'Year-over-Year Sales Performance'
                },
                xAxis: {
                    type: 'category'
                },
                yAxis: {
                    title: {
                        text: 'Revenue ($)'
                    },
                    labels: {
                        formatter: function() {
                            return '$' + (this.value / 1000) + 'k';
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        let tooltip = '<b>' + this.point.name + '</b><br>';
                        tooltip += 'Amount: $' + this.y.toLocaleString() + '<br>';
                        if (this.point.category) {
                            tooltip += 'Category: ' + this.point.category;
                        }
                        return tooltip;
                    }
                },
                plotOptions: {
                    waterfall: {
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return '$' + (this.y / 1000) + 'k';
                            }
                        }
                    }
                },
                series: [{
                    data: data.map(point => ({
                        ...point,
                        color: point.category === 'Growth' ? '#90ed7d' :
                               point.category === 'Loss' ? '#f45b5b' :
                               point.isSum || point.isIntermediateSum ? '#7cb5ec' : undefined
                    })),
                    pointPadding: 0
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate waterfall charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial.db'
db = SQLAlchemy(app)

class FinancialEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    is_sum = db.Column(db.Boolean, default=False)
    is_intermediate_sum = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/financial-data')
def get_financial_data():
    entries = FinancialEntry.query.order_by(FinancialEntry.timestamp).all()
    
    data = [{
        'name': entry.name,
        'y': entry.amount,
        'category': entry.category,
        'isSum': entry.is_sum,
        'isIntermediateSum': entry.is_intermediate_sum,
        'description': entry.description
    } for entry in entries]
    
    return jsonify(data)
```

## Tips for Working with Waterfall Charts

1. Order points logically
2. Use clear labels
3. Choose meaningful colors
4. Include totals
5. Add informative tooltips
6. Consider data scale
7. Use appropriate spacing
8. Optimize readability
