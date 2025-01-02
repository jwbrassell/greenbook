# Line Charts with Chart.js and Flask

## Table of Contents
- [Line Charts with Chart.js and Flask](#line-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Multi-Line Sales Comparison](#example-1:-multi-line-sales-comparison)
    - [Flask Implementation](#flask-implementation)
    - [Database Model](#database-model)
  - [Example 2: Interactive Temperature Monitoring](#example-2:-interactive-temperature-monitoring)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Chart Configuration](#advanced-chart-configuration)
  - [Example 3: Animated Financial Data](#example-3:-animated-financial-data)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Animation Configuration](#advanced-animation-configuration)
  - [Working with Database Data](#working-with-database-data)



Line charts are perfect for showing trends over time and comparing multiple data series. This guide shows how to create various line charts using Chart.js with Flask.

## Basic Implementation

### Flask Route
```python
@app.route('/line-chart')
def line_chart():
    return render_template('line_chart.html')

@app.route('/api/line-data')
def line_data():
    # Example: Fetch monthly sales data from database
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Monthly Sales',
            'data': [65, 59, 80, 81, 56, 55],
            'fill': false,
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.1
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="lineChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/line-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('lineChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Monthly Sales Data'
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

## Example 1: Multi-Line Sales Comparison

This example shows how to compare sales data across multiple product categories.

### Flask Implementation
```python
@app.route('/api/multi-line-data')
def multi_line_data():
    # In a real application, this would come from your database
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [
            {
                'label': 'Electronics',
                'data': [65, 59, 80, 81, 56, 55],
                'borderColor': 'rgb(75, 192, 192)',
                'fill': false
            },
            {
                'label': 'Clothing',
                'data': [28, 48, 40, 19, 86, 27],
                'borderColor': 'rgb(255, 99, 132)',
                'fill': false
            },
            {
                'label': 'Books',
                'data': [45, 25, 16, 36, 67, 18],
                'borderColor': 'rgb(153, 102, 255)',
                'fill': false
            }
        ]
    }
    return jsonify(data)
```

### Database Model
```python
class SalesData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    month = db.Column(db.String(20))
    amount = db.Column(db.Float)
    
    @staticmethod
    def get_sales_by_category():
        categories = ['Electronics', 'Clothing', 'Books']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        datasets = []
        
        for category in categories:
            sales = SalesData.query.filter_by(category=category).all()
            data = [s.amount for s in sales]
            datasets.append({
                'label': category,
                'data': data,
                'borderColor': get_color_for_category(category),
                'fill': False
            })
            
        return {'labels': months, 'datasets': datasets}
```

## Example 2: Interactive Temperature Monitoring

This example demonstrates an interactive line chart for temperature monitoring with tooltips and zoom capabilities.

### Flask Implementation
```python
@app.route('/api/temperature-data')
def temperature_data():
    # Simulated temperature data with timestamps
    data = {
        'labels': [datetime.now().strftime('%H:%M:%S') for _ in range(24)],
        'datasets': [{
            'label': 'Temperature (°C)',
            'data': [random.uniform(20, 30) for _ in range(24)],
            'borderColor': 'rgb(255, 99, 132)',
            'fill': true,
            'backgroundColor': 'rgba(255, 99, 132, 0.2)'
        }]
    }
    return jsonify(data)
```

### Advanced Chart Configuration
```javascript
const options = {
    responsive: true,
    plugins: {
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
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    return `Temperature: ${context.parsed.y.toFixed(1)}°C`;
                }
            }
        }
    },
    scales: {
        x: {
            type: 'time',
            time: {
                unit: 'hour'
            }
        },
        y: {
            beginAtZero: false
        }
    }
};
```

## Example 3: Animated Financial Data

This example shows how to create an animated line chart for financial data with custom animations and gradients.

### Flask Implementation
```python
@app.route('/api/financial-data')
def financial_data():
    data = {
        'labels': [f'Week {i}' for i in range(1, 53)],
        'datasets': [{
            'label': 'Stock Price',
            'data': generate_stock_data(),  # Your data generation function
            'borderColor': 'rgb(75, 192, 192)',
            'fill': true,
            'backgroundColor': create_gradient()  # Custom gradient
        }]
    }
    return jsonify(data)
```

### Advanced Animation Configuration
```javascript
const config = {
    type: 'line',
    data: chartData,
    options: {
        animation: {
            duration: 2000,
            easing: 'easeInOutQuart',
            onProgress: function(animation) {
                // Custom animation progress handling
            },
            onComplete: function() {
                // Animation complete callback
            }
        },
        plugins: {
            legend: {
                labels: {
                    font: {
                        size: 14
                    }
                }
            }
        },
        elements: {
            line: {
                tension: 0.4
            },
            point: {
                radius: 4,
                hoverRadius: 6
            }
        }
    }
};
```

## Working with Database Data

Here's how you might integrate this with a Flask-SQLAlchemy database:

```python
class TemperatureReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float)
    location = db.Column(db.String(100))

    @staticmethod
    def get_chart_data(location, hours=24):
        readings = TemperatureReading.query\
            .filter_by(location=location)\
            .order_by(TemperatureReading.timestamp.desc())\
            .limit(hours)\
            .all()
        
        return {
            'labels': [r.timestamp.strftime('%H:%M:%S') for r in readings],
            'datasets': [{
                'label': f'Temperature at {location}',
                'data': [r.temperature for r in readings],
                'borderColor': 'rgb(75, 192, 192)',
                'fill': false
            }]
        }
```

This documentation provides three distinct examples of line charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like animations and real-time updates.
