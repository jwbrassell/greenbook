# Doughnut Charts with Chart.js and Flask

## Table of Contents
- [Doughnut Charts with Chart.js and Flask](#doughnut-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Interactive Revenue Distribution](#example-1:-interactive-revenue-distribution)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
    - [Database Model](#database-model)
  - [Example 2: Multi-Ring Market Share Analysis](#example-2:-multi-ring-market-share-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 3: Animated Customer Demographics](#example-3:-animated-customer-demographics)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Animation Configuration](#advanced-animation-configuration)
  - [Working with Database Data](#working-with-database-data)



Doughnut charts are perfect for displaying proportional data and part-to-whole relationships. They're particularly effective for showing percentage distributions and making comparisons between categories.

## Basic Implementation

### Flask Route
```python
@app.route('/doughnut-chart')
def doughnut_chart():
    return render_template('doughnut_chart.html')

@app.route('/api/doughnut-data')
def doughnut_data():
    # Example: Budget allocation data
    data = {
        'labels': ['Development', 'Marketing', 'Infrastructure', 'Support', 'Training'],
        'datasets': [{
            'data': [35, 25, 20, 15, 5],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)'
            ],
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="doughnutChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/doughnut-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('doughnutChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Budget Allocation'
                        },
                        legend: {
                            position: 'top',
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Interactive Revenue Distribution

This example shows an interactive doughnut chart displaying revenue distribution with custom tooltips and click handlers.

### Flask Implementation
```python
@app.route('/api/revenue-distribution')
def revenue_distribution():
    data = {
        'labels': ['Product Sales', 'Services', 'Subscriptions', 
                  'Consulting', 'Training'],
        'datasets': [{
            'data': [45, 25, 15, 10, 5],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)'
            ],
            'hoverOffset': 4
        }]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'doughnut',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    generateLabels: function(chart) {
                        // Custom legend labels with percentages
                        const data = chart.data;
                        const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
                        return data.labels.map((label, i) => ({
                            text: `${label}: ${Math.round(data.datasets[0].data[i] / total * 100)}%`,
                            fillStyle: data.datasets[0].backgroundColor[i],
                            hidden: false,
                            index: i
                        }));
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const value = context.raw;
                        const percentage = Math.round((value / total) * 100);
                        return `${context.label}: $${value}k (${percentage}%)`;
                    }
                }
            }
        }
    }
};
```

### Database Model
```python
class Revenue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    quarter = db.Column(db.String(2))
    year = db.Column(db.Integer)
    
    @staticmethod
    def get_distribution(year, quarter):
        revenues = Revenue.query\
            .filter_by(year=year, quarter=quarter)\
            .order_by(Revenue.amount.desc())\
            .all()
            
        return {
            'labels': [r.category for r in revenues],
            'datasets': [{
                'data': [r.amount for r in revenues],
                'backgroundColor': generate_colors(len(revenues)),
                'hoverOffset': 4
            }]
        }
```

## Example 2: Multi-Ring Market Share Analysis

This example demonstrates how to create a multi-ring doughnut chart for market share analysis.

### Flask Implementation
```python
@app.route('/api/market-share')
def market_share():
    data = {
        'labels': ['Company A', 'Company B', 'Company C', 'Others'],
        'datasets': [
            {
                'label': '2022',
                'data': [40, 30, 20, 10],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ],
                'weight': 0.5
            },
            {
                'label': '2023',
                'data': [35, 35, 25, 5],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)'
                ],
                'weight': 1
            }
        ]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'right',
        },
        title: {
            display: true,
            text: 'Market Share Comparison'
        }
    },
    cutout: '60%',
    radius: {
        '2022': '90%',
        '2023': '70%'
    }
};
```

## Example 3: Animated Customer Demographics

This example shows how to create an animated doughnut chart for customer demographics with custom animations and interactions.

### Flask Implementation
```python
@app.route('/api/demographics')
def demographics():
    data = {
        'labels': ['18-24', '25-34', '35-44', '45-54', '55+'],
        'datasets': [{
            'data': [15, 30, 25, 20, 10],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)'
            ],
            'hoverBackgroundColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ]
        }]
    }
    return jsonify(data)
```

### Advanced Animation Configuration
```javascript
const config = {
    type: 'doughnut',
    data: chartData,
    options: {
        animation: {
            animateRotate: true,
            animateScale: true,
            duration: 2000,
            easing: 'easeInOutQuart',
            onProgress: function(animation) {
                // Custom animation progress handling
            },
            onComplete: function() {
                // Animation complete callback
            }
        },
        hover: {
            mode: 'nearest',
            intersect: true,
            animationDuration: 400
        },
        plugins: {
            tooltip: {
                callbacks: {
                    afterLabel: function(context) {
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = Math.round((context.raw / total) * 100);
                        return `Represents ${percentage}% of total customers`;
                    }
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic doughnut charts:

```python
class CustomerDemographics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age_group = db.Column(db.String(20))
    count = db.Column(db.Integer)
    region = db.Column(db.String(50))
    year = db.Column(db.Integer)

    @staticmethod
    def get_age_distribution(region, year):
        demographics = CustomerDemographics.query\
            .filter_by(region=region, year=year)\
            .order_by(CustomerDemographics.age_group)\
            .all()
            
        return {
            'labels': [d.age_group for d in demographics],
            'datasets': [{
                'data': [d.count for d in demographics],
                'backgroundColor': generate_colors(len(demographics)),
                'hoverOffset': 4
            }]
        }
```

This documentation provides three distinct examples of doughnut charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like animations and interactive elements.
