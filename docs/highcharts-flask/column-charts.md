# Column Charts with Highcharts and Flask

## Table of Contents
- [Column Charts with Highcharts and Flask](#column-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Sales Comparison](#example-1:-sales-comparison)
  - [Example 2: Stacked Analysis](#example-2:-stacked-analysis)
  - [Example 3: Performance Metrics](#example-3:-performance-metrics)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Column Charts](#tips-for-working-with-column-charts)



## Overview

Column charts are ideal for comparing values across different categories or showing data changes over time. They are particularly effective when you want to emphasize individual values and make direct comparisons between items. Column charts can be simple, stacked, or grouped to show different aspects of your data.

## Basic Configuration

Here's how to create a basic column chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/column-chart')
def column_chart():
    return render_template('column-chart.html')

@app.route('/column-data')
def column_data():
    # Sample monthly sales data
    data = [
        ['Jan', 4500],
        ['Feb', 5200],
        ['Mar', 6100],
        ['Apr', 4800],
        ['May', 5900],
        ['Jun', 7000],
        ['Jul', 6300],
        ['Aug', 5800],
        ['Sep', 6800],
        ['Oct', 7200],
        ['Nov', 6500],
        ['Dec', 7500]
    ]
    
    return jsonify(data)
```

```html
<!-- templates/column-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="column-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/column-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('column-container', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Monthly Sales'
                },
                xAxis: {
                    categories: data.map(item => item[0]),
                    crosshair: true
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Sales ($)'
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                               '<td style="padding:0"><b>${point.y:,.0f}</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0
                    }
                },
                series: [{
                    name: 'Sales',
                    data: data.map(item => item[1])
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Column charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        column: {
            pointPadding: 0.2,     // Space between columns
            groupPadding: 0.2,     // Space between column sets
            borderWidth: 0,        // Column border width
            borderRadius: 0,       // Column corner radius
            colorByPoint: false,   // Different color for each column
            grouping: true,       // Group columns
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

## Example 1: Sales Comparison

This example shows sales comparison across different product categories:

```python
@app.route('/sales-comparison')
def sales_comparison():
    data = {
        'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
        'series': [
            {
                'name': 'Electronics',
                'data': [43000, 48000, 52000, 59000]
            },
            {
                'name': 'Clothing',
                'data': [32000, 28000, 35000, 41000]
            },
            {
                'name': 'Accessories',
                'data': [18000, 21000, 24000, 28000]
            }
        ]
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="sales-comparison"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/sales-comparison')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('sales-comparison', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Quarterly Sales by Category'
                },
                xAxis: {
                    categories: data.categories,
                    crosshair: true
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Sales ($)'
                    },
                    labels: {
                        formatter: function() {
                            return '$' + this.value / 1000 + 'k';
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                               '<td style="padding:0"><b>${point.y:,.0f}</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0
                    }
                },
                series: data.series
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Stacked Analysis

This example shows expense breakdown with stacked columns:

```python
@app.route('/expense-breakdown')
def expense_breakdown():
    data = {
        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'expenses': [
            {
                'name': 'Fixed Costs',
                'data': [15000, 15000, 15000, 15000, 15000, 15000],
                'stack': 'expenses'
            },
            {
                'name': 'Variable Costs',
                'data': [12000, 13500, 11800, 14200, 13100, 15500],
                'stack': 'expenses'
            },
            {
                'name': 'Marketing',
                'data': [5000, 7000, 6500, 5800, 8000, 7500],
                'stack': 'expenses'
            },
            {
                'name': 'Other',
                'data': [3000, 2800, 3200, 2900, 3500, 3100],
                'stack': 'expenses'
            }
        ]
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="expense-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/expense-breakdown')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('expense-chart', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Monthly Expense Breakdown'
                },
                xAxis: {
                    categories: data.months
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Total Expenses ($)'
                    },
                    stackLabels: {
                        enabled: true,
                        format: '${total:,.0f}',
                        style: {
                            fontWeight: 'bold'
                        }
                    }
                },
                legend: {
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical'
                },
                tooltip: {
                    headerFormat: '<b>{point.x}</b><br/>',
                    pointFormat: '{series.name}: ${point.y:,.0f}<br/>Total: ${point.stackTotal:,.0f}'
                },
                plotOptions: {
                    column: {
                        stacking: 'normal',
                        dataLabels: {
                            enabled: false
                        }
                    }
                },
                series: data.expenses
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Performance Metrics

This example shows performance metrics with positive and negative values:

```python
@app.route('/performance-metrics')
def performance_metrics():
    data = {
        'metrics': ['Revenue', 'Costs', 'Profit', 'Growth', 'Satisfaction', 'Efficiency'],
        'current': [120, -85, 35, -5, 15, 10],
        'target': [100, -80, 20, 10, 10, 5]
    }
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="performance-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/performance-metrics')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('performance-chart', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Performance vs Target'
                },
                xAxis: {
                    categories: data.metrics,
                    crosshair: true
                },
                yAxis: {
                    title: {
                        text: 'Percentage (%)'
                    },
                    labels: {
                        format: '{value}%'
                    }
                },
                tooltip: {
                    shared: true,
                    valuePrefix: data.metrics.includes('Revenue') ? '$' : '',
                    valueSuffix: '%'
                },
                plotOptions: {
                    column: {
                        grouping: false,
                        shadow: false,
                        borderWidth: 0
                    }
                },
                series: [{
                    name: 'Target',
                    color: 'rgba(158,160,165,0.2)',
                    pointPadding: 0.3,
                    pointPlacement: -0.2,
                    data: data.target
                }, {
                    name: 'Current',
                    color: Highcharts.getOptions().colors[0],
                    pointPadding: 0.4,
                    pointPlacement: -0.2,
                    data: data.current
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate column charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'
db = SQLAlchemy(app)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

@app.route('/sales-data')
def get_sales_data():
    # Get monthly sales by category
    sales = db.session.query(
        db.func.strftime('%Y-%m', Sale.date).label('month'),
        Sale.category,
        db.func.sum(Sale.amount).label('total')
    ).group_by(
        'month',
        Sale.category
    ).order_by(
        'month'
    ).all()
    
    # Format data for chart
    months = sorted(list(set(s.month for s in sales)))
    categories = sorted(list(set(s.category for s in sales)))
    
    series = []
    for category in categories:
        series_data = []
        for month in months:
            sale = next((s for s in sales if s.month == month and s.category == category), None)
            series_data.append(float(sale.total) if sale else 0)
        
        series.append({
            'name': category,
            'data': series_data
        })
    
    return jsonify({
        'categories': months,
        'series': series
    })
```

## Tips for Working with Column Charts

1. Choose appropriate spacing
2. Consider stacking options
3. Use clear colors
4. Implement proper tooltips
5. Handle negative values
6. Add data labels when needed
7. Optimize for readability
8. Use meaningful legends
