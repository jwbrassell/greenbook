# Funnel Charts with Chart.js and Flask

## Table of Contents
- [Funnel Charts with Chart.js and Flask](#funnel-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Interactive Conversion Funnel](#example-1:-interactive-conversion-funnel)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Multi-Channel Funnel](#example-2:-multi-channel-funnel)
    - [Flask Implementation](#flask-implementation)
    - [Stacked Funnel Configuration](#stacked-funnel-configuration)
  - [Example 3: Time-Based Funnel Analysis](#example-3:-time-based-funnel-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Time Analysis Configuration](#time-analysis-configuration)
  - [Working with Database Data](#working-with-database-data)



Funnel charts are effective for visualizing sequential processes where values typically decrease at each stage, such as sales pipelines or user conversion flows. While Chart.js doesn't have a built-in funnel chart type, we can create them using horizontal bar charts with custom styling.

## Basic Implementation

### Flask Route
```python
@app.route('/funnel-chart')
def funnel_chart():
    return render_template('funnel_chart.html')

@app.route('/api/funnel-data')
def funnel_data():
    # Example: Sales funnel data
    data = {
        'labels': ['Visitors', 'Leads', 'Qualified', 'Proposals', 'Sales'],
        'datasets': [{
            'data': [1000, 750, 500, 250, 100],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)'
            ],
            'borderColor': 'white',
            'borderWidth': 1,
            'percentages': []  # Will be calculated in JavaScript
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="funnelChart"></canvas>
</div>

<script>
// Calculate percentages for funnel steps
function calculatePercentages(data) {
    const total = data[0];
    return data.map(value => ((value / total) * 100).toFixed(1));
}

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/funnel-data')
        .then(response => response.json())
        .then(data => {
            // Calculate and store percentages
            data.datasets[0].percentages = calculatePercentages(data.datasets[0].data);
            
            const ctx = document.getElementById('funnelChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Sales Funnel Analysis'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw;
                                    const percentage = context.dataset.percentages[context.dataIndex];
                                    return `Count: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Interactive Conversion Funnel

This example shows how to create an interactive funnel chart with detailed conversion metrics.

### Flask Implementation
```python
@app.route('/api/conversion-funnel')
def conversion_funnel():
    data = {
        'labels': [
            'Website Visits',
            'Product Views',
            'Add to Cart',
            'Begin Checkout',
            'Purchase'
        ],
        'datasets': [{
            'data': [10000, 7500, 5000, 2500, 1000],
            'backgroundColor': generate_gradient_colors(5),
            'borderWidth': 1,
            'conversion_rates': []  # Will be calculated
        }]
    }
    return jsonify(data)

def generate_gradient_colors(steps):
    colors = []
    for i in range(steps):
        opacity = 0.9 - (i * 0.1)  # Decreasing opacity
        colors.append(f'rgba(75, 192, 192, {opacity})')
    return colors
```

### Advanced Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        indexAxis: 'y',
        responsive: true,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    afterLabel: function(context) {
                        const currentValue = context.raw;
                        const previousValue = context.dataIndex === 0 ? 
                            currentValue : 
                            context.dataset.data[context.dataIndex - 1];
                        const conversionRate = ((currentValue / previousValue) * 100).toFixed(1);
                        return `Step Conversion: ${conversionRate}%`;
                    }
                }
            }
        },
        onClick: (event, elements) => {
            if (elements.length > 0) {
                const index = elements[0].index;
                showStepDetails(index);
            }
        }
    }
};

function showStepDetails(stepIndex) {
    // Implement modal or sidebar with detailed metrics
    const stepData = {
        current: data.datasets[0].data[stepIndex],
        previous: stepIndex > 0 ? data.datasets[0].data[stepIndex - 1] : null,
        label: data.labels[stepIndex]
    };
    console.log('Step Details:', stepData);
}
```

## Example 2: Multi-Channel Funnel

This example demonstrates how to compare conversion funnels across different channels.

### Flask Implementation
```python
@app.route('/api/multi-channel-funnel')
def multi_channel_funnel():
    data = {
        'labels': ['Awareness', 'Interest', 'Consideration', 'Purchase'],
        'datasets': [
            {
                'label': 'Organic',
                'data': [5000, 3500, 2000, 800],
                'backgroundColor': 'rgba(75, 192, 192, 0.8)',
                'stack': 'stack0'
            },
            {
                'label': 'Paid',
                'data': [3000, 2000, 1200, 500],
                'backgroundColor': 'rgba(255, 99, 132, 0.8)',
                'stack': 'stack0'
            },
            {
                'label': 'Social',
                'data': [2000, 1500, 800, 300],
                'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                'stack': 'stack0'
            }
        ]
    }
    return jsonify(data)
```

### Stacked Funnel Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
            x: {
                stacked: true,
                beginAtZero: true
            },
            y: {
                stacked: true
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    afterFooter: function(tooltipItems) {
                        const total = tooltipItems.reduce((sum, item) => sum + item.raw, 0);
                        const previousTotal = tooltipItems[0].dataIndex === 0 ? total :
                            tooltipItems.reduce((sum, item) => 
                                sum + item.dataset.data[item.dataIndex - 1], 0);
                        const conversionRate = ((total / previousTotal) * 100).toFixed(1);
                        return `Total Conversion: ${conversionRate}%`;
                    }
                }
            }
        }
    }
};
```

## Example 3: Time-Based Funnel Analysis

This example shows how to analyze funnel performance over time.

### Flask Implementation
```python
@app.route('/api/time-funnel')
def time_funnel():
    import pandas as pd
    
    # Generate sample data for last 6 months
    months = pd.date_range(
        start=pd.Timestamp.now() - pd.DateOffset(months=5),
        end=pd.Timestamp.now(),
        freq='M'
    )
    
    data = {
        'labels': ['Discovery', 'Evaluation', 'Intent', 'Purchase'],
        'datasets': []
    }
    
    for month in months:
        month_name = month.strftime('%B %Y')
        base_value = random.randint(800, 1200)
        
        data['datasets'].append({
            'label': month_name,
            'data': [
                base_value,
                int(base_value * random.uniform(0.6, 0.8)),
                int(base_value * random.uniform(0.3, 0.5)),
                int(base_value * random.uniform(0.1, 0.2))
            ],
            'backgroundColor': generate_color_with_opacity(0.7),
            'borderWidth': 1
        })
    
    return jsonify(data)

def generate_color_with_opacity(opacity):
    r = random.randint(50, 200)
    g = random.randint(50, 200)
    b = random.randint(50, 200)
    return f'rgba({r}, {g}, {b}, {opacity})'
```

### Time Analysis Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        indexAxis: 'y',
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Funnel Performance Over Time'
            }
        },
        scales: {
            x: {
                stacked: false,
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Users'
                }
            },
            y: {
                stacked: false,
                title: {
                    display: true,
                    text: 'Funnel Stage'
                }
            }
        },
        interaction: {
            mode: 'index',
            intersect: false
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic funnel charts:

```python
class FunnelData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String(50))
    count = db.Column(db.Integer)
    channel = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_funnel_data(start_date, end_date, channels=None):
        query = FunnelData.query\
            .filter(FunnelData.timestamp.between(start_date, end_date))
            
        if channels:
            query = query.filter(FunnelData.channel.in_(channels))
            
        results = query.order_by(
            FunnelData.channel,
            FunnelData.stage
        ).all()
        
        # Organize data by channel
        channels_data = {}
        for result in results:
            if result.channel not in channels_data:
                channels_data[result.channel] = {
                    'label': result.channel,
                    'data': [],
                    'backgroundColor': generate_color_with_opacity(0.8)
                }
            channels_data[result.channel]['data'].append(result.count)
        
        return {
            'labels': ['Discovery', 'Evaluation', 'Intent', 'Purchase'],
            'datasets': list(channels_data.values())
        }
```

This documentation provides three distinct examples of funnel charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like multi-channel analysis and time-based comparisons.
