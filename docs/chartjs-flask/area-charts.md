# Area Charts with Chart.js and Flask

## Table of Contents
- [Area Charts with Chart.js and Flask](#area-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Stacked Area Chart for Revenue Streams](#example-1:-stacked-area-chart-for-revenue-streams)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
    - [Database Model](#database-model)
  - [Example 2: User Engagement Metrics](#example-2:-user-engagement-metrics)
    - [Flask Implementation](#flask-implementation)
    - [Gradient Fill Configuration](#gradient-fill-configuration)
  - [Example 3: Multi-Area Comparison](#example-3:-multi-area-comparison)
    - [Flask Implementation](#flask-implementation)
    - [Interactive Features Configuration](#interactive-features-configuration)
  - [Working with Database Data](#working-with-database-data)



Area charts are excellent for visualizing trends over time while emphasizing the volume beneath the line. They're particularly effective for showing cumulative data, comparing volumes, and highlighting the magnitude of trends.

## Basic Implementation

### Flask Route
```python
@app.route('/area-chart')
def area_chart():
    return render_template('area_chart.html')

@app.route('/api/area-data')
def area_data():
    # Example: Monthly website traffic data
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Website Visitors',
            'data': [10000, 15000, 12000, 18000, 25000, 30000],
            'fill': true,
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'tension': 0.4
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="areaChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/area-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('areaChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',  // Area charts are line charts with fill
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Monthly Website Traffic'
                        },
                        legend: {
                            position: 'top',
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Visitors'
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Stacked Area Chart for Revenue Streams

This example shows how to create a stacked area chart to visualize multiple revenue streams over time.

### Flask Implementation
```python
@app.route('/api/revenue-streams')
def revenue_streams():
    data = {
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'datasets': [
            {
                'label': 'Product Sales',
                'data': [300, 450, 600, 400],
                'backgroundColor': 'rgba(255, 99, 132, 0.5)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'fill': true
            },
            {
                'label': 'Services',
                'data': [200, 300, 400, 350],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'fill': true
            },
            {
                'label': 'Subscriptions',
                'data': [100, 150, 200, 250],
                'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'fill': true
            }
        ]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Revenue Streams Analysis'
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(context) {
                        return `${context.dataset.label}: $${context.raw}k`;
                    }
                }
            }
        },
        hover: {
            mode: 'index',
            intersect: false
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Quarter'
                }
            },
            y: {
                stacked: true,
                title: {
                    display: true,
                    text: 'Revenue (thousands)'
                },
                ticks: {
                    callback: function(value) {
                        return '$' + value + 'k';
                    }
                }
            }
        }
    }
};
```

### Database Model
```python
class RevenueData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stream_type = db.Column(db.String(50))
    amount = db.Column(db.Float)
    quarter = db.Column(db.String(2))
    year = db.Column(db.Integer)
    
    @staticmethod
    def get_quarterly_revenue(year):
        revenues = RevenueData.query\
            .filter_by(year=year)\
            .order_by(RevenueData.stream_type, RevenueData.quarter)\
            .all()
            
        datasets = {}
        for rev in revenues:
            if rev.stream_type not in datasets:
                datasets[rev.stream_type] = {
                    'label': rev.stream_type,
                    'data': [],
                    'backgroundColor': get_color_for_stream(rev.stream_type, 0.5),
                    'borderColor': get_color_for_stream(rev.stream_type, 1),
                    'fill': true
                }
            datasets[rev.stream_type]['data'].append(rev.amount)
            
        return {
            'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
            'datasets': list(datasets.values())
        }
```

## Example 2: User Engagement Metrics

This example demonstrates how to visualize user engagement metrics with a gradient fill.

### Flask Implementation
```python
@app.route('/api/user-engagement')
def user_engagement():
    data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'datasets': [{
            'label': 'Active Users',
            'data': [1200, 1900, 2300, 2100, 2500, 3000, 2800],
            'fill': true,
            'backgroundColor': 'rgba(54, 162, 235, 0.5)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'tension': 0.4
        }]
    }
    return jsonify(data)
```

### Gradient Fill Configuration
```javascript
const config = {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            filler: {
                propagate: true
            }
        },
        elements: {
            line: {
                tension: 0.4
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    },
    plugins: [{
        beforeDraw: (chart) => {
            const ctx = chart.ctx;
            const gradient = ctx.createLinearGradient(0, 0, 0, chart.height);
            gradient.addColorStop(0, 'rgba(54, 162, 235, 0.5)');
            gradient.addColorStop(1, 'rgba(54, 162, 235, 0.0)');
            chart.data.datasets[0].backgroundColor = gradient;
        }
    }]
};
```

## Example 3: Multi-Area Comparison

This example shows how to create multiple semi-transparent area charts for comparison.

### Flask Implementation
```python
@app.route('/api/platform-usage')
def platform_usage():
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [
            {
                'label': 'Mobile',
                'data': [5000, 7000, 9000, 8500, 10000, 12000],
                'fill': true,
                'backgroundColor': 'rgba(255, 99, 132, 0.3)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'tension': 0.4
            },
            {
                'label': 'Desktop',
                'data': [8000, 9000, 8500, 9500, 11000, 10500],
                'fill': true,
                'backgroundColor': 'rgba(54, 162, 235, 0.3)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'tension': 0.4
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
        tooltip: {
            callbacks: {
                label: function(context) {
                    const label = context.dataset.label || '';
                    const value = context.parsed.y;
                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = ((value / total) * 100).toFixed(1);
                    return `${label}: ${value.toLocaleString()} (${percentage}%)`;
                }
            }
        }
    },
    scales: {
        x: {
            grid: {
                display: false
            }
        },
        y: {
            stacked: false,
            grid: {
                color: 'rgba(0, 0, 0, 0.1)'
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic area charts:

```python
class PlatformUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20))
    users = db.Column(db.Integer)
    date = db.Column(db.Date)

    @staticmethod
    def get_monthly_usage(start_date, end_date):
        usage = PlatformUsage.query\
            .filter(PlatformUsage.date.between(start_date, end_date))\
            .order_by(PlatformUsage.platform, PlatformUsage.date)\
            .all()
            
        datasets = {}
        labels = []
        
        for record in usage:
            month = record.date.strftime('%b %Y')
            if month not in labels:
                labels.append(month)
                
            if record.platform not in datasets:
                datasets[record.platform] = {
                    'label': record.platform,
                    'data': [],
                    'fill': true,
                    'backgroundColor': get_platform_color(record.platform, 0.3),
                    'borderColor': get_platform_color(record.platform, 1),
                    'tension': 0.4
                }
            datasets[record.platform]['data'].append(record.users)
            
        return {
            'labels': labels,
            'datasets': list(datasets.values())
        }
```

This documentation provides three distinct examples of area charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like gradient fills and interactive elements.
