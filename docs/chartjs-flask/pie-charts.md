# Pie Charts with Chart.js and Flask

## Table of Contents
- [Pie Charts with Chart.js and Flask](#pie-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Interactive Sales Distribution](#example-1:-interactive-sales-distribution)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
    - [Database Model](#database-model)
  - [Example 2: Expenditure Analysis](#example-2:-expenditure-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 3: Animated User Demographics](#example-3:-animated-user-demographics)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Animation Configuration](#advanced-animation-configuration)
  - [Working with Database Data](#working-with-database-data)



Pie charts are excellent for displaying proportional data in a simple, intuitive format. They're particularly effective for showing percentage distributions and making part-to-whole comparisons.

## Basic Implementation

### Flask Route
```python
@app.route('/pie-chart')
def pie_chart():
    return render_template('pie_chart.html')

@app.route('/api/pie-data')
def pie_data():
    # Example: Website traffic sources
    data = {
        'labels': ['Organic Search', 'Direct', 'Social Media', 'Email', 'Referral'],
        'datasets': [{
            'data': [45, 25, 15, 10, 5],
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
    <canvas id="pieChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/pie-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('pieChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Traffic Sources Distribution'
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

## Example 1: Interactive Sales Distribution

This example shows an interactive pie chart displaying sales distribution with custom tooltips and click events.

### Flask Implementation
```python
@app.route('/api/sales-distribution')
def sales_distribution():
    data = {
        'labels': ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports'],
        'datasets': [{
            'data': [35, 25, 20, 15, 5],
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
    type: 'pie',
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
class SalesCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    month = db.Column(db.String(20))
    year = db.Column(db.Integer)
    
    @staticmethod
    def get_distribution(year, month):
        sales = SalesCategory.query\
            .filter_by(year=year, month=month)\
            .order_by(SalesCategory.amount.desc())\
            .all()
            
        return {
            'labels': [s.category for s in sales],
            'datasets': [{
                'data': [s.amount for s in sales],
                'backgroundColor': generate_colors(len(sales)),
                'hoverOffset': 4
            }]
        }
```

## Example 2: Expenditure Analysis

This example demonstrates how to create a pie chart for analyzing expenditure patterns with custom interactions.

### Flask Implementation
```python
@app.route('/api/expenditure')
def expenditure():
    data = {
        'labels': ['Rent', 'Utilities', 'Salaries', 'Equipment', 'Marketing'],
        'datasets': [{
            'data': [30, 15, 35, 10, 10],
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

### Advanced Configuration
```javascript
const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'right',
        },
        tooltip: {
            callbacks: {
                afterLabel: function(context) {
                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = Math.round((context.raw / total) * 100);
                    return `${percentage}% of total expenditure`;
                }
            }
        }
    },
    onClick: (event, elements) => {
        if (elements.length > 0) {
            const segment = elements[0];
            const label = data.labels[segment.index];
            const value = data.datasets[0].data[segment.index];
            // Handle click event
            console.log(`Clicked on ${label}: ${value}`);
        }
    }
};
```

## Example 3: Animated User Demographics

This example shows how to create an animated pie chart for user demographics with custom animations and transitions.

### Flask Implementation
```python
@app.route('/api/user-demographics')
def user_demographics():
    data = {
        'labels': ['Mobile', 'Desktop', 'Tablet', 'Other'],
        'datasets': [{
            'data': [55, 30, 12, 3],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)'
            ],
            'hoverBackgroundColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ]
        }]
    }
    return jsonify(data)
```

### Advanced Animation Configuration
```javascript
const config = {
    type: 'pie',
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
                        return `${percentage}% of total users`;
                    }
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic pie charts:

```python
class UserDevice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(20))
    count = db.Column(db.Integer)
    month = db.Column(db.String(20))
    year = db.Column(db.Integer)

    @staticmethod
    def get_device_distribution(year, month):
        devices = UserDevice.query\
            .filter_by(year=year, month=month)\
            .order_by(UserDevice.count.desc())\
            .all()
            
        return {
            'labels': [d.device_type for d in devices],
            'datasets': [{
                'data': [d.count for d in devices],
                'backgroundColor': generate_colors(len(devices)),
                'hoverOffset': 4
            }]
        }
```

This documentation provides three distinct examples of pie charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like animations and interactive elements.
