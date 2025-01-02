# Bar Charts with Chart.js and Flask

## Table of Contents
- [Bar Charts with Chart.js and Flask](#bar-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Grouped Bar Chart](#example-1:-grouped-bar-chart)
    - [Flask Implementation](#flask-implementation)
    - [Database Model](#database-model)
  - [Example 2: Stacked Bar Chart](#example-2:-stacked-bar-chart)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 3: Horizontal Bar Chart with Animation](#example-3:-horizontal-bar-chart-with-animation)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Animation Configuration](#advanced-animation-configuration)
  - [Working with Database Data](#working-with-database-data)



Bar charts are excellent for comparing quantities across different categories. This guide demonstrates how to create various types of bar charts using Chart.js with Flask.

## Basic Implementation

### Flask Route
```python
@app.route('/bar-chart')
def bar_chart():
    return render_template('bar_chart.html')

@app.route('/api/bar-data')
def bar_data():
    # Example: Product sales data
    data = {
        'labels': ['Product A', 'Product B', 'Product C', 'Product D'],
        'datasets': [{
            'label': 'Sales Volume',
            'data': [120, 190, 300, 150],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)'
            ],
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="barChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/bar-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('barChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Product Sales Comparison'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Grouped Bar Chart

This example shows how to create a grouped bar chart comparing multiple metrics across categories.

### Flask Implementation
```python
@app.route('/api/grouped-bar-data')
def grouped_bar_data():
    data = {
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'datasets': [
            {
                'label': 'Revenue',
                'data': [300, 450, 600, 400],
                'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Expenses',
                'data': [200, 350, 500, 300],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Profit',
                'data': [100, 100, 100, 100],
                'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }
        ]
    }
    return jsonify(data)
```

### Database Model
```python
class FinancialMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quarter = db.Column(db.String(2))
    year = db.Column(db.Integer)
    revenue = db.Column(db.Float)
    expenses = db.Column(db.Float)
    profit = db.Column(db.Float)
    
    @staticmethod
    def get_quarterly_metrics(year):
        metrics = FinancialMetrics.query.filter_by(year=year).all()
        labels = [f'Q{m.quarter}' for m in metrics]
        
        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Revenue',
                    'data': [m.revenue for m in metrics],
                    'backgroundColor': 'rgba(255, 99, 132, 0.5)'
                },
                {
                    'label': 'Expenses',
                    'data': [m.expenses for m in metrics],
                    'backgroundColor': 'rgba(54, 162, 235, 0.5)'
                },
                {
                    'label': 'Profit',
                    'data': [m.profit for m in metrics],
                    'backgroundColor': 'rgba(75, 192, 192, 0.5)'
                }
            ]
        }
```

## Example 2: Stacked Bar Chart

This example demonstrates a stacked bar chart showing market share distribution.

### Flask Implementation
```python
@app.route('/api/stacked-bar-data')
def stacked_bar_data():
    data = {
        'labels': ['2019', '2020', '2021', '2022'],
        'datasets': [
            {
                'label': 'Product A',
                'data': [30, 35, 40, 45],
                'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                'stack': 'Stack 0'
            },
            {
                'label': 'Product B',
                'data': [40, 45, 35, 30],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                'stack': 'Stack 0'
            },
            {
                'label': 'Product C',
                'data': [30, 20, 25, 25],
                'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                'stack': 'Stack 0'
            }
        ]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const options = {
    responsive: true,
    scales: {
        x: {
            stacked: true,
        },
        y: {
            stacked: true,
            beginAtZero: true,
            max: 100,
            ticks: {
                callback: function(value) {
                    return value + '%';
                }
            }
        }
    },
    plugins: {
        tooltip: {
            callbacks: {
                label: function(context) {
                    return context.dataset.label + ': ' + context.parsed.y + '%';
                }
            }
        }
    }
};
```

## Example 3: Horizontal Bar Chart with Animation

This example shows how to create an animated horizontal bar chart for ranking visualization.

### Flask Implementation
```python
@app.route('/api/horizontal-bar-data')
def horizontal_bar_data():
    data = {
        'labels': ['Category A', 'Category B', 'Category C', 'Category D', 'Category E'],
        'datasets': [{
            'label': 'Performance Score',
            'data': [85, 72, 68, 92, 77],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)'
            ],
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### Advanced Animation Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        indexAxis: 'y',
        animation: {
            duration: 2000,
            easing: 'easeInOutQuart',
            from: {
                x: -1000
            },
            delay: function(context) {
                return context.dataIndex * 100;
            }
        },
        plugins: {
            legend: {
                position: 'right',
            },
            title: {
                display: true,
                text: 'Performance Rankings'
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic bar charts:

```python
class ProductPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    sales_amount = db.Column(db.Float)
    region = db.Column(db.String(50))
    year = db.Column(db.Integer)

    @staticmethod
    def get_regional_performance(year):
        products = ProductPerformance.query\
            .filter_by(year=year)\
            .order_by(ProductPerformance.sales_amount.desc())\
            .all()
        
        return {
            'labels': [p.product_name for p in products],
            'datasets': [{
                'label': 'Sales Performance',
                'data': [p.sales_amount for p in products],
                'backgroundColor': generate_colors(len(products)),
                'borderWidth': 1
            }]
        }
```

This documentation provides three distinct examples of bar charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like animations and stacked visualizations.
