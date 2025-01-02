# Split Line Charts with Chart.js and Flask

## Table of Contents
- [Split Line Charts with Chart.js and Flask](#split-line-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Multi-Segment Comparison](#example-1:-multi-segment-comparison)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Threshold-Based Splits](#example-2:-threshold-based-splits)
    - [Flask Implementation](#flask-implementation)
    - [Threshold Plugin Configuration](#threshold-plugin-configuration)
  - [Example 3: Time-Based Split Analysis](#example-3:-time-based-split-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Time Period Plugin Configuration](#time-period-plugin-configuration)
  - [Working with Database Data](#working-with-database-data)



Split line charts are useful for visualizing data with breaks or discontinuities, comparing data across different periods, or highlighting specific segments of data. While Chart.js doesn't have a built-in split line type, we can create them using custom configurations and plugins.

## Basic Implementation

### Flask Route
```python
@app.route('/split-line-chart')
def split_line_chart():
    return render_template('split_line_chart.html')

@app.route('/api/split-line-data')
def split_line_data():
    # Example: Sales data with seasonal breaks
    data = {
        'labels': [
            '2023-Q1', '2023-Q2', '2023-Q3', '2023-Q4',
            '2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4'
        ],
        'datasets': [{
            'label': 'Sales Performance',
            'data': [
                {'x': '2023-Q1', 'y': 100},
                {'x': '2023-Q2', 'y': 120},
                {'x': '2023-Q3', 'y': null},  # Break point
                {'x': '2023-Q4', 'y': 150},
                {'x': '2024-Q1', 'y': 160},
                {'x': '2024-Q2', 'y': 180},
                {'x': '2024-Q3', 'y': null},  # Break point
                {'x': '2024-Q4', 'y': 200}
            ],
            'borderColor': 'rgba(75, 192, 192, 1)',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'segment': {
                'borderDash': function(ctx) {
                    if (ctx.p0.skip || ctx.p1.skip) return [6, 6];
                    return undefined;
                }
            },
            'spanGaps': false
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="splitLineChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/split-line-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('splitLineChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Sales Performance with Seasonal Breaks'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    if (context.raw.y === null) return 'No Data';
                                    return `Sales: $${context.raw.y}k`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Sales ($k)'
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Multi-Segment Comparison

This example shows how to create a split line chart comparing different data segments with custom styling.

### Flask Implementation
```python
@app.route('/api/multi-segment-data')
def multi_segment_data():
    data = {
        'labels': generate_date_range(),  # Your date generation function
        'datasets': [
            {
                'label': 'Current Year',
                'data': generate_segment_data(),  # Your data generation function
                'borderColor': 'rgba(75, 192, 192, 1)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'segment': {
                    'borderColor': function(ctx) {
                        if (ctx.p0.parsed.y > ctx.p1.parsed.y) {
                            return 'rgba(255, 99, 132, 1)';  # Red for decreasing
                        }
                        return 'rgba(75, 192, 192, 1)';     # Green for increasing
                    },
                    'backgroundColor': function(ctx) {
                        if (ctx.p0.parsed.y > ctx.p1.parsed.y) {
                            return 'rgba(255, 99, 132, 0.2)';
                        }
                        return 'rgba(75, 192, 192, 0.2)';
                    }
                }
            }
        ]
    }
    return jsonify(data)

def generate_segment_data():
    # Example data generation with trends
    base_value = 100
    data = []
    for i in range(12):
        if i < 4:
            base_value += random.uniform(5, 10)
        elif i < 8:
            base_value -= random.uniform(2, 7)
        else:
            base_value += random.uniform(8, 15)
        data.append(base_value)
    return data
```

### Advanced Configuration
```javascript
const config = {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(context) {
                        const value = context.raw;
                        const prev = context.dataset.data[context.dataIndex - 1];
                        if (prev) {
                            const change = ((value - prev) / prev * 100).toFixed(1);
                            return `${context.dataset.label}: ${value} (${change}%)`;
                        }
                        return `${context.dataset.label}: ${value}`;
                    }
                }
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month'
                }
            },
            y: {
                beginAtZero: false
            }
        }
    }
};
```

## Example 2: Threshold-Based Splits

This example demonstrates how to create splits based on threshold values.

### Flask Implementation
```python
@app.route('/api/threshold-splits')
def threshold_splits():
    data = {
        'labels': list(range(24)),  # 24 hours
        'datasets': [{
            'label': 'Energy Usage',
            'data': generate_energy_data(),  # Your data generation function
            'borderColor': 'rgba(75, 192, 192, 1)',
            'segment': {
                'borderColor': function(ctx) {
                    const threshold = 75;
                    if (ctx.p0.parsed.y > threshold || ctx.p1.parsed.y > threshold) {
                        return 'rgba(255, 99, 132, 1)';  # Red for high usage
                    }
                    return 'rgba(75, 192, 192, 1)';     # Green for normal usage
                }
            },
            'thresholds': {
                'line': 75,  # Threshold value
                'color': 'rgba(255, 0, 0, 0.5)'
            }
        }]
    }
    return jsonify(data)
```

### Threshold Plugin Configuration
```javascript
const thresholdPlugin = {
    id: 'thresholdPlugin',
    beforeDraw: (chart, args, options) => {
        const {ctx, chartArea, scales} = chart;
        
        chart.data.datasets.forEach(dataset => {
            if (!dataset.thresholds) return;
            
            const y = scales.y.getPixelForValue(dataset.thresholds.line);
            
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(chartArea.left, y);
            ctx.lineTo(chartArea.right, y);
            ctx.lineWidth = 1;
            ctx.strokeStyle = dataset.thresholds.color;
            ctx.setLineDash([5, 5]);
            ctx.stroke();
            ctx.restore();
        });
    }
};
```

## Example 3: Time-Based Split Analysis

This example shows how to analyze data with time-based splits and annotations.

### Flask Implementation
```python
@app.route('/api/time-splits')
def time_splits():
    data = {
        'labels': generate_hourly_labels(),  # 24-hour labels
        'datasets': [{
            'label': 'Network Traffic',
            'data': generate_traffic_data(),  # Your traffic data
            'borderColor': 'rgba(75, 192, 192, 1)',
            'fill': true,
            'segment': {
                'borderColor': function(ctx) {
                    const hour = parseInt(ctx.p0.parsed.x);
                    if (hour >= 9 && hour <= 17) {
                        return 'rgba(255, 99, 132, 1)';  # Business hours
                    }
                    return 'rgba(75, 192, 192, 1)';     # Off hours
                }
            },
            'periods': [
                {
                    'start': 9,
                    'end': 17,
                    'label': 'Business Hours',
                    'color': 'rgba(255, 99, 132, 0.1)'
                }
            ]
        }]
    }
    return jsonify(data)
```

### Time Period Plugin Configuration
```javascript
const timePeriodPlugin = {
    id: 'timePeriodPlugin',
    beforeDraw: (chart, args, options) => {
        const {ctx, chartArea, scales} = chart;
        
        chart.data.datasets.forEach(dataset => {
            if (!dataset.periods) return;
            
            dataset.periods.forEach(period => {
                const startX = scales.x.getPixelForValue(period.start);
                const endX = scales.x.getPixelForValue(period.end);
                
                // Draw period background
                ctx.save();
                ctx.fillStyle = period.color;
                ctx.fillRect(startX, chartArea.top, endX - startX, chartArea.height);
                
                // Draw period label
                ctx.textAlign = 'center';
                ctx.textBaseline = 'top';
                ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
                ctx.fillText(period.label, (startX + endX) / 2, chartArea.top + 10);
                ctx.restore();
            });
        });
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic split line charts:

```python
class TimeSeriesData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Float)
    category = db.Column(db.String(50))
    
    @staticmethod
    def get_split_data(start_date, end_date, split_threshold=None):
        data = TimeSeriesData.query\
            .filter(TimeSeriesData.timestamp.between(start_date, end_date))\
            .order_by(TimeSeriesData.timestamp)\
            .all()
            
        return {
            'labels': [d.timestamp.strftime('%Y-%m-%d %H:%M') for d in data],
            'datasets': [{
                'label': 'Time Series',
                'data': [d.value for d in data],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'segment': {
                    'borderColor': function(ctx) {
                        if (split_threshold and 
                            (ctx.p0.parsed.y > split_threshold or 
                             ctx.p1.parsed.y > split_threshold)):
                            return 'rgba(255, 99, 132, 1)';
                        return 'rgba(75, 192, 192, 1)';
                    }
                }
            }]
        }
```

This documentation provides three distinct examples of split line charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like threshold-based splits and time-based analysis.
