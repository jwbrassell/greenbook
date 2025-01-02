# Polar Area Charts with Chart.js and Flask

## Table of Contents
- [Polar Area Charts with Chart.js and Flask](#polar-area-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Resource Utilization Analysis](#example-1:-resource-utilization-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
    - [Database Model](#database-model)
  - [Example 2: Skill Assessment Visualization](#example-2:-skill-assessment-visualization)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Animation Configuration](#advanced-animation-configuration)
  - [Example 3: Performance Metrics Analysis](#example-3:-performance-metrics-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Interactive Features Configuration](#interactive-features-configuration)
  - [Working with Database Data](#working-with-database-data)



Polar area charts are unique visualizations that combine aspects of pie charts and radar charts. Each segment has an equal angle, but the radius varies based on the value, making them excellent for showing both proportion and magnitude simultaneously.

## Basic Implementation

### Flask Route
```python
@app.route('/polar-area-chart')
def polar_area_chart():
    return render_template('polar_area_chart.html')

@app.route('/api/polar-area-data')
def polar_area_data():
    # Example: Monthly project completion data
    data = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'datasets': [{
            'data': [11, 16, 7, 14, 12, 9],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 159, 64, 0.5)'
            ],
            'borderColor': [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 206, 86)',
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)',
                'rgb(255, 159, 64)'
            ],
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="polarAreaChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/polar-area-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('polarAreaChart').getContext('2d');
            new Chart(ctx, {
                type: 'polarArea',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Monthly Project Completion'
                        },
                        legend: {
                            position: 'right',
                        }
                    },
                    scales: {
                        r: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Resource Utilization Analysis

This example shows how to visualize resource utilization across different departments with custom tooltips.

### Flask Implementation
```python
@app.route('/api/resource-utilization')
def resource_utilization():
    data = {
        'labels': ['Development', 'Marketing', 'Sales', 'Support', 'HR', 'Operations'],
        'datasets': [{
            'data': [85, 65, 75, 45, 35, 55],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 159, 64, 0.5)'
            ],
            'borderWidth': 2
        }]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'polarArea',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'right',
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.raw;
                        return `Resource Usage: ${value}%`;
                    },
                    afterLabel: function(context) {
                        const maxValue = Math.max(...context.dataset.data);
                        if (context.raw === maxValue) {
                            return 'Highest utilization!';
                        }
                        return '';
                    }
                }
            }
        },
        scales: {
            r: {
                min: 0,
                max: 100,
                ticks: {
                    stepSize: 20,
                    callback: function(value) {
                        return value + '%';
                    }
                },
                pointLabels: {
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            }
        }
    }
};
```

### Database Model
```python
class ResourceUtilization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50))
    usage_percentage = db.Column(db.Float)
    month = db.Column(db.String(20))
    year = db.Column(db.Integer)
    
    @staticmethod
    def get_department_usage(year, month):
        usage = ResourceUtilization.query\
            .filter_by(year=year, month=month)\
            .order_by(ResourceUtilization.department)\
            .all()
            
        return {
            'labels': [u.department for u in usage],
            'datasets': [{
                'data': [u.usage_percentage for u in usage],
                'backgroundColor': generate_colors(len(usage), 0.5),
                'borderWidth': 2
            }]
        }
```

## Example 2: Skill Assessment Visualization

This example demonstrates how to create an interactive polar area chart for skill assessment visualization.

### Flask Implementation
```python
@app.route('/api/skill-assessment')
def skill_assessment():
    data = {
        'labels': ['Technical', 'Communication', 'Leadership', 
                  'Problem Solving', 'Teamwork', 'Innovation'],
        'datasets': [{
            'data': [90, 75, 85, 95, 80, 70],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 159, 64, 0.7)'
            ],
            'borderColor': 'rgba(255, 255, 255, 0.5)',
            'borderWidth': 2
        }]
    }
    return jsonify(data)
```

### Advanced Animation Configuration
```javascript
const config = {
    type: 'polarArea',
    data: chartData,
    options: {
        animation: {
            animateRotate: true,
            animateScale: true,
            duration: 2000,
            easing: 'easeInOutQuart'
        },
        scales: {
            r: {
                angleLines: {
                    display: true,
                    color: 'rgba(255, 255, 255, 0.2)'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.2)'
                },
                pointLabels: {
                    font: {
                        size: 14
                    }
                },
                ticks: {
                    backdropColor: 'rgba(0, 0, 0, 0.3)'
                }
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
        }
    }
};
```

## Example 3: Performance Metrics Analysis

This example shows how to create a polar area chart for analyzing performance metrics with custom interactions.

### Flask Implementation
```python
@app.route('/api/performance-metrics')
def performance_metrics():
    data = {
        'labels': ['Speed', 'Accuracy', 'Efficiency', 'Quality', 
                  'Reliability', 'Scalability'],
        'datasets': [{
            'data': [85, 92, 78, 95, 88, 82],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)'
            ],
            'borderWidth': 2,
            'hoverBackgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)'
            ]
        }]
    }
    return jsonify(data)
```

### Interactive Features Configuration
```javascript
const options = {
    responsive: true,
    plugins: {
        tooltip: {
            callbacks: {
                label: function(context) {
                    const value = context.raw;
                    const maxValue = Math.max(...context.dataset.data);
                    const performance = value >= 90 ? 'Excellent' :
                                      value >= 80 ? 'Good' :
                                      value >= 70 ? 'Average' : 'Needs Improvement';
                    return `${context.label}: ${value} (${performance})`;
                }
            }
        }
    },
    onClick: (event, elements) => {
        if (elements.length > 0) {
            const element = elements[0];
            const label = data.labels[element.index];
            const value = data.datasets[0].data[element.index];
            // Handle click event
            console.log(`Clicked on ${label}: ${value}`);
            // You could trigger a modal or update another chart here
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic polar area charts:

```python
class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(50))
    score = db.Column(db.Float)
    category = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_latest_metrics(category):
        metrics = PerformanceMetric.query\
            .filter_by(category=category)\
            .order_by(PerformanceMetric.timestamp.desc())\
            .limit(6)\
            .all()
            
        return {
            'labels': [m.metric_name for m in metrics],
            'datasets': [{
                'data': [m.score for m in metrics],
                'backgroundColor': generate_colors(len(metrics), 0.6),
                'borderWidth': 2
            }]
        }
```

This documentation provides three distinct examples of polar area charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like animations and interactive elements.
