# Mixed Charts with Chart.js and Flask

## Table of Contents
- [Mixed Charts with Chart.js and Flask](#mixed-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Sales Performance Dashboard](#example-1:-sales-performance-dashboard)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Website Analytics Dashboard](#example-2:-website-analytics-dashboard)
    - [Flask Implementation](#flask-implementation)
    - [Interactive Features Configuration](#interactive-features-configuration)
  - [Example 3: Financial Performance Overview](#example-3:-financial-performance-overview)
    - [Flask Implementation](#flask-implementation)
    - [Complex Configuration](#complex-configuration)
  - [Working with Database Data](#working-with-database-data)



Mixed charts combine different chart types in a single visualization, allowing you to represent different types of data in their most appropriate format. This is particularly useful when you need to compare metrics that are best shown in different ways, such as combining bars with lines.

## Basic Implementation

### Flask Route
```python
@app.route('/mixed-chart')
def mixed_chart():
    return render_template('mixed_chart.html')

@app.route('/api/mixed-data')
def mixed_data():
    # Example: Revenue (bar) and Profit Margin (line)
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [
            {
                'type': 'bar',
                'label': 'Revenue',
                'data': [50000, 60000, 55000, 65000, 75000, 80000],
                'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1,
                'yAxisID': 'y'
            },
            {
                'type': 'line',
                'label': 'Profit Margin (%)',
                'data': [15, 18, 16, 19, 22, 25],
                'borderColor': 'rgba(255, 99, 132, 1)',
                'tension': 0.4,
                'yAxisID': 'y1'
            }
        ]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="mixedChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/mixed-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('mixedChart').getContext('2d');
            new Chart(ctx, {
                type: 'scatter',  // Base type doesn't matter for mixed charts
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Revenue and Profit Margin Analysis'
                        },
                        legend: {
                            position: 'top',
                        }
                    },
                    scales: {
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            title: {
                                display: true,
                                text: 'Revenue ($)'
                            }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: {
                                display: true,
                                text: 'Profit Margin (%)'
                            },
                            grid: {
                                drawOnChartArea: false
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Sales Performance Dashboard

This example combines bar charts for sales volume with line charts for growth rate.

### Flask Implementation
```python
@app.route('/api/sales-performance')
def sales_performance():
    data = {
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'datasets': [
            {
                'type': 'bar',
                'label': 'Sales Volume',
                'data': [120000, 150000, 180000, 220000],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1,
                'yAxisID': 'y'
            },
            {
                'type': 'bar',
                'label': 'Target',
                'data': [130000, 160000, 190000, 230000],
                'backgroundColor': 'rgba(255, 206, 86, 0.5)',
                'borderColor': 'rgba(255, 206, 86, 1)',
                'borderWidth': 1,
                'yAxisID': 'y'
            },
            {
                'type': 'line',
                'label': 'Growth Rate',
                'data': [0, 25, 20, 22],
                'borderColor': 'rgba(255, 99, 132, 1)',
                'tension': 0.4,
                'yAxisID': 'y1'
            }
        ]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    data: chartData,
    options: {
        responsive: true,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            title: {
                display: true,
                text: 'Sales Performance Analysis'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.dataset.yAxisID === 'y') {
                            label += new Intl.NumberFormat('en-US', {
                                style: 'currency',
                                currency: 'USD'
                            }).format(context.raw);
                        } else {
                            label += context.raw + '%';
                        }
                        return label;
                    }
                }
            }
        },
        scales: {
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                    display: true,
                    text: 'Sales Volume ($)'
                },
                ticks: {
                    callback: function(value) {
                        return '$' + value.toLocaleString();
                    }
                }
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                title: {
                    display: true,
                    text: 'Growth Rate (%)'
                },
                ticks: {
                    callback: function(value) {
                        return value + '%';
                    }
                },
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    }
};
```

## Example 2: Website Analytics Dashboard

This example combines line charts for visitors with bar charts for conversion rates.

### Flask Implementation
```python
@app.route('/api/website-analytics')
def website_analytics():
    data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'datasets': [
            {
                'type': 'line',
                'label': 'Visitors',
                'data': [1500, 1800, 2000, 1900, 2200, 2800, 2500],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'tension': 0.4,
                'yAxisID': 'y'
            },
            {
                'type': 'bar',
                'label': 'Conversion Rate',
                'data': [2.5, 2.8, 3.2, 2.9, 3.5, 4.0, 3.8],
                'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'yAxisID': 'y1'
            }
        ]
    }
    return jsonify(data)
```

### Interactive Features Configuration
```javascript
const options = {
    responsive: true,
    interaction: {
        mode: 'index',
        intersect: false,
    },
    plugins: {
        legend: {
            position: 'top',
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    if (context.dataset.type === 'bar') {
                        return `Conversion Rate: ${context.raw}%`;
                    } else {
                        return `Visitors: ${context.raw.toLocaleString()}`;
                    }
                }
            }
        }
    },
    scales: {
        y: {
            type: 'linear',
            position: 'left',
            title: {
                display: true,
                text: 'Number of Visitors'
            },
            ticks: {
                callback: function(value) {
                    return value.toLocaleString();
                }
            }
        },
        y1: {
            type: 'linear',
            position: 'right',
            title: {
                display: true,
                text: 'Conversion Rate (%)'
            },
            ticks: {
                callback: function(value) {
                    return value + '%';
                }
            },
            grid: {
                drawOnChartArea: false
            }
        }
    }
};
```

## Example 3: Financial Performance Overview

This example combines multiple chart types to show comprehensive financial data.

### Flask Implementation
```python
@app.route('/api/financial-overview')
def financial_overview():
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [
            {
                'type': 'bar',
                'label': 'Revenue',
                'data': [300000, 350000, 320000, 380000, 400000, 450000],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                'yAxisID': 'y'
            },
            {
                'type': 'bar',
                'label': 'Expenses',
                'data': [250000, 285000, 275000, 295000, 310000, 340000],
                'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                'yAxisID': 'y'
            },
            {
                'type': 'line',
                'label': 'Profit Margin',
                'data': [16.7, 18.6, 14.1, 22.4, 22.5, 24.4],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'tension': 0.4,
                'yAxisID': 'y1'
            },
            {
                'type': 'bubble',
                'label': 'Market Size',
                'data': [
                    {'x': 0, 'y': 300000, 'r': 10},
                    {'x': 1, 'y': 350000, 'r': 12},
                    {'x': 2, 'y': 320000, 'r': 8},
                    {'x': 3, 'y': 380000, 'r': 15},
                    {'x': 4, 'y': 400000, 'r': 18},
                    {'x': 5, 'y': 450000, 'r': 20}
                ],
                'backgroundColor': 'rgba(153, 102, 255, 0.5)',
                'yAxisID': 'y'
            }
        ]
    }
    return jsonify(data)
```

### Complex Configuration
```javascript
const config = {
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Financial Performance Overview'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        if (context.dataset.type === 'bubble') {
                            return [
                                `Revenue: $${context.raw.y.toLocaleString()}`,
                                `Market Share: ${context.raw.r * 5}%`
                            ];
                        } else if (context.dataset.type === 'line') {
                            return `Profit Margin: ${context.raw}%`;
                        } else {
                            return `${context.dataset.label}: $${context.raw.toLocaleString()}`;
                        }
                    }
                }
            }
        },
        scales: {
            y: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Amount ($)'
                },
                ticks: {
                    callback: function(value) {
                        return '$' + (value / 1000).toLocaleString() + 'k';
                    }
                }
            },
            y1: {
                type: 'linear',
                position: 'right',
                title: {
                    display: true,
                    text: 'Profit Margin (%)'
                },
                ticks: {
                    callback: function(value) {
                        return value + '%';
                    }
                },
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic mixed charts:

```python
class FinancialMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    revenue = db.Column(db.Float)
    expenses = db.Column(db.Float)
    market_size = db.Column(db.Float)

    @staticmethod
    def get_financial_overview(start_date, end_date):
        metrics = FinancialMetrics.query\
            .filter(FinancialMetrics.date.between(start_date, end_date))\
            .order_by(FinancialMetrics.date)\
            .all()
            
        labels = [m.date.strftime('%b %Y') for m in metrics]
        revenue_data = [m.revenue for m in metrics]
        expenses_data = [m.expenses for m in metrics]
        profit_margins = [((r - e) / r * 100) for r, e in zip(revenue_data, expenses_data)]
        bubble_data = [{'x': i, 'y': r, 'r': m.market_size/1000000} 
                      for i, (r, m) in enumerate(zip(revenue_data, metrics))]
        
        return {
            'labels': labels,
            'datasets': [
                {
                    'type': 'bar',
                    'label': 'Revenue',
                    'data': revenue_data,
                    'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                    'yAxisID': 'y'
                },
                {
                    'type': 'bar',
                    'label': 'Expenses',
                    'data': expenses_data,
                    'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                    'yAxisID': 'y'
                },
                {
                    'type': 'line',
                    'label': 'Profit Margin',
                    'data': profit_margins,
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'tension': 0.4,
                    'yAxisID': 'y1'
                },
                {
                    'type': 'bubble',
                    'label': 'Market Size',
                    'data': bubble_data,
                    'backgroundColor': 'rgba(153, 102, 255, 0.5)',
                    'yAxisID': 'y'
                }
            ]
        }
```

This documentation provides three distinct examples of mixed charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like multiple axes and interactive elements.
