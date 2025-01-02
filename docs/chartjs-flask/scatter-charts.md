# Scatter Charts with Chart.js and Flask

## Table of Contents
- [Scatter Charts with Chart.js and Flask](#scatter-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Multi-Dataset Performance Analysis](#example-1:-multi-dataset-performance-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
    - [Database Model](#database-model)
  - [Example 2: Temperature vs. Energy Usage](#example-2:-temperature-vs-energy-usage)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Regression Line](#advanced-regression-line)
  - [Example 3: Customer Behavior Analysis](#example-3:-customer-behavior-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Interactive Features Configuration](#interactive-features-configuration)
  - [Working with Database Data](#working-with-database-data)



Scatter charts are ideal for visualizing relationships between two variables and identifying patterns, correlations, or clusters in data. They're particularly useful for analyzing trends and outliers in datasets.

## Basic Implementation

### Flask Route
```python
@app.route('/scatter-chart')
def scatter_chart():
    return render_template('scatter_chart.html')

@app.route('/api/scatter-data')
def scatter_data():
    # Example: Student performance data (x: study hours, y: test scores)
    data = {
        'datasets': [{
            'label': 'Student Performance',
            'data': [
                {'x': 2, 'y': 65},
                {'x': 3, 'y': 75},
                {'x': 4, 'y': 82},
                {'x': 5, 'y': 85},
                {'x': 6, 'y': 90},
                {'x': 7, 'y': 95},
                {'x': 4.5, 'y': 88},
                {'x': 3.5, 'y': 78},
                {'x': 5.5, 'y': 92}
            ],
            'backgroundColor': 'rgba(75, 192, 192, 0.5)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'pointRadius': 6
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="scatterChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/scatter-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('scatterChart').getContext('2d');
            new Chart(ctx, {
                type: 'scatter',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Study Hours vs. Test Scores'
                        },
                        legend: {
                            position: 'top',
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Study Hours'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Test Score'
                            },
                            min: 0,
                            max: 100
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Multi-Dataset Performance Analysis

This example shows how to compare performance metrics across different groups.

### Flask Implementation
```python
@app.route('/api/performance-comparison')
def performance_comparison():
    data = {
        'datasets': [
            {
                'label': 'Group A',
                'data': [
                    {'x': 15, 'y': 85}, {'x': 25, 'y': 92}, {'x': 35, 'y': 89},
                    {'x': 45, 'y': 95}, {'x': 55, 'y': 88}, {'x': 65, 'y': 94}
                ],
                'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                'borderColor': 'rgba(255, 99, 132, 1)'
            },
            {
                'label': 'Group B',
                'data': [
                    {'x': 20, 'y': 82}, {'x': 30, 'y': 88}, {'x': 40, 'y': 85},
                    {'x': 50, 'y': 90}, {'x': 60, 'y': 87}, {'x': 70, 'y': 92}
                ],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                'borderColor': 'rgba(54, 162, 235, 1)'
            }
        ]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'scatter',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return [
                            `${context.dataset.label}`,
                            `Time: ${context.parsed.x} minutes`,
                            `Score: ${context.parsed.y}%`
                        ];
                    }
                }
            },
            zoom: {
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy'
                }
            }
        },
        scales: {
            x: {
                min: 0,
                max: 80,
                ticks: {
                    stepSize: 10
                }
            },
            y: {
                min: 60,
                max: 100,
                ticks: {
                    stepSize: 5
                }
            }
        }
    }
};
```

### Database Model
```python
class PerformanceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(50))
    time_taken = db.Column(db.Float)
    score = db.Column(db.Float)
    test_date = db.Column(db.DateTime)
    
    @staticmethod
    def get_group_performance():
        performances = PerformanceData.query\
            .order_by(PerformanceData.group, PerformanceData.test_date)\
            .all()
            
        datasets = {}
        for perf in performances:
            if perf.group not in datasets:
                datasets[perf.group] = {
                    'label': f'Group {perf.group}',
                    'data': [],
                    'backgroundColor': get_color_for_group(perf.group, 0.5),
                    'borderColor': get_color_for_group(perf.group, 1)
                }
            datasets[perf.group]['data'].append({
                'x': perf.time_taken,
                'y': perf.score
            })
            
        return {'datasets': list(datasets.values())}
```

## Example 2: Temperature vs. Energy Usage

This example demonstrates how to visualize the relationship between temperature and energy consumption.

### Flask Implementation
```python
@app.route('/api/energy-usage')
def energy_usage():
    data = {
        'datasets': [{
            'label': 'Energy Consumption',
            'data': [
                {'x': 15, 'y': 200}, {'x': 20, 'y': 250}, {'x': 25, 'y': 300},
                {'x': 30, 'y': 400}, {'x': 35, 'y': 500}, {'x': 40, 'y': 600}
            ],
            'backgroundColor': generate_color_gradient(6, 'rgba(75, 192, 192, 0.5)'),
            'pointRadius': 8,
            'pointHoverRadius': 12
        }]
    }
    return jsonify(data)
```

### Advanced Regression Line
```javascript
const options = {
    responsive: true,
    plugins: {
        annotation: {
            annotations: {
                line1: {
                    type: 'line',
                    scaleID: 'y',
                    value: calculateTrendline(data.datasets[0].data),
                    borderColor: 'rgba(255, 99, 132, 0.8)',
                    borderWidth: 2,
                    label: {
                        content: 'Trend Line',
                        enabled: true
                    }
                }
            }
        }
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'Temperature (°C)'
            }
        },
        y: {
            title: {
                display: true,
                text: 'Energy Usage (kWh)'
            }
        }
    }
};

function calculateTrendline(data) {
    // Simple linear regression calculation
    const xValues = data.map(point => point.x);
    const yValues = data.map(point => point.y);
    const n = xValues.length;
    
    const xMean = xValues.reduce((a, b) => a + b) / n;
    const yMean = yValues.reduce((a, b) => a + b) / n;
    
    const slope = xValues.reduce((sum, x, i) => {
        return sum + (x - xMean) * (yValues[i] - yMean);
    }, 0) / xValues.reduce((sum, x) => sum + Math.pow(x - xMean, 2), 0);
    
    const intercept = yMean - slope * xMean;
    
    return {
        slope: slope,
        intercept: intercept,
        fn: x => slope * x + intercept
    };
}
```

## Example 3: Customer Behavior Analysis

This example shows how to analyze customer behavior patterns using scatter plots.

### Flask Implementation
```python
@app.route('/api/customer-behavior')
def customer_behavior():
    data = {
        'datasets': [
            {
                'label': 'New Customers',
                'data': generate_customer_data(50, 'new'),
                'backgroundColor': 'rgba(255, 99, 132, 0.5)'
            },
            {
                'label': 'Returning Customers',
                'data': generate_customer_data(50, 'returning'),
                'backgroundColor': 'rgba(54, 162, 235, 0.5)'
            }
        ]
    }
    return jsonify(data)

def generate_customer_data(count, type):
    import random
    if type == 'new':
        return [{'x': random.uniform(10, 100), 
                'y': random.uniform(20, 150)} 
                for _ in range(count)]
    else:
        return [{'x': random.uniform(50, 200), 
                'y': random.uniform(50, 250)} 
                for _ in range(count)]
```

### Interactive Features Configuration
```javascript
const config = {
    type: 'scatter',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return [
                            `${context.dataset.label}`,
                            `Purchase Amount: $${context.parsed.x}`,
                            `Time Spent: ${context.parsed.y} minutes`
                        ];
                    }
                }
            },
            legend: {
                position: 'top'
            }
        },
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Purchase Amount ($)'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Time Spent on Site (minutes)'
                }
            }
        },
        onClick: (event, elements) => {
            if (elements.length > 0) {
                const element = elements[0];
                const datapoint = data.datasets[element.datasetIndex].data[element.index];
                analyzeCustomerSegment(datapoint);
            }
        }
    }
};

function analyzeCustomerSegment(datapoint) {
    // Custom analysis logic
    const segment = datapoint.x > 100 ? 'High Value' : 
                   datapoint.y > 100 ? 'Engaged' : 'Standard';
    console.log(`Customer Segment: ${segment}`);
}
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic scatter charts:

```python
class CustomerAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_type = db.Column(db.String(20))
    purchase_amount = db.Column(db.Float)
    time_spent = db.Column(db.Float)
    visit_date = db.Column(db.DateTime)

    @staticmethod
    def get_customer_behavior(start_date, end_date):
        customers = CustomerAnalytics.query\
            .filter(CustomerAnalytics.visit_date.between(start_date, end_date))\
            .all()
            
        datasets = {
            'new': {
                'label': 'New Customers',
                'data': [],
                'backgroundColor': 'rgba(255, 99, 132, 0.5)'
            },
            'returning': {
                'label': 'Returning Customers',
                'data': [],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)'
            }
        }
        
        for customer in customers:
            datasets[customer.customer_type]['data'].append({
                'x': customer.purchase_amount,
                'y': customer.time_spent
            })
            
        return {'datasets': list(datasets.values())}
```

This documentation provides three distinct examples of scatter charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like trend lines and interactive elements.
