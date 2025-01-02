# Interactive Charts with Chart.js and Flask

## Table of Contents
- [Interactive Charts with Chart.js and Flask](#interactive-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
    - [Details](#details)
  - [Example 1: Zoom and Pan Controls](#example-1:-zoom-and-pan-controls)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Interactive Legend and Data Selection](#example-2:-interactive-legend-and-data-selection)
    - [Flask Implementation](#flask-implementation)
    - [Interactive Legend Configuration](#interactive-legend-configuration)
  - [Example 3: Interactive Data Analysis](#example-3:-interactive-data-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Analysis Tools Configuration](#analysis-tools-configuration)
  - [Working with Database Data](#working-with-database-data)



Interactive charts enhance data visualization by allowing users to explore and interact with the data. This guide demonstrates how to implement various interactive features in Chart.js with Flask integration.

## Basic Implementation

### Flask Route
```python
@app.route('/interactive-chart')
def interactive_chart():
    return render_template('interactive_chart.html')

@app.route('/api/chart-data')
def chart_data():
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Sales',
            'data': [65, 59, 80, 81, 56, 55],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }
    return jsonify(data)

@app.route('/api/data-point/<int:index>')
def data_point_details(index):
    # Example: Return detailed information for a specific data point
    details = {
        'month': ['January', 'February', 'March', 'April', 'May', 'June'][index],
        'sales': [65, 59, 80, 81, 56, 55][index],
        'transactions': [120, 132, 145, 160, 123, 110][index],
        'average_value': [542, 447, 552, 506, 455, 500][index]
    }
    return jsonify(details)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="interactiveChart"></canvas>
</div>

<div id="detailsPanel" style="display: none; margin-top: 20px; padding: 10px; border: 1px solid #ddd;">
    <h3>Details</h3>
    <div id="detailsContent"></div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('interactiveChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Interactive Sales Chart'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `Sales: $${context.raw}`;
                                }
                            }
                        }
                    },
                    onClick: (event, elements) => {
                        if (elements.length > 0) {
                            const index = elements[0].index;
                            showDetails(index);
                        }
                    }
                }
            });
        });
});

function showDetails(index) {
    fetch(`/api/data-point/${index}`)
        .then(response => response.json())
        .then(details => {
            const content = `
                <p><strong>Month:</strong> ${details.month}</p>
                <p><strong>Sales:</strong> $${details.sales}</p>
                <p><strong>Transactions:</strong> ${details.transactions}</p>
                <p><strong>Average Value:</strong> $${details.average_value}</p>
            `;
            document.getElementById('detailsContent').innerHTML = content;
            document.getElementById('detailsPanel').style.display = 'block';
        });
}
</script>
```

## Example 1: Zoom and Pan Controls

This example demonstrates how to implement zoom and pan functionality for detailed data exploration.

### Flask Implementation
```python
@app.route('/api/detailed-data')
def detailed_data():
    # Generate 100 data points for demonstration
    import numpy as np
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.exp(-x/5) * 100
    
    data = {
        'labels': x.tolist(),
        'datasets': [{
            'label': 'Detailed Signal',
            'data': y.tolist(),
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.4,
            'fill': false
        }]
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
            zoom: {
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy',
                },
                pan: {
                    enabled: true,
                    mode: 'xy',
                }
            }
        },
        scales: {
            x: {
                min: 0,
                max: 10
            }
        }
    },
    plugins: [{
        id: 'controlPanel',
        beforeInit: (chart) => {
            // Add control buttons
            const container = chart.canvas.parentNode;
            container.insertAdjacentHTML('beforeend', `
                <div style="margin-top: 10px;">
                    <button onclick="resetZoom()">Reset Zoom</button>
                    <button onclick="zoomIn()">Zoom In</button>
                    <button onclick="zoomOut()">Zoom Out</button>
                </div>
            `);
        }
    }]
};

function resetZoom() {
    chart.resetZoom();
}

function zoomIn() {
    chart.zoom(1.1);
}

function zoomOut() {
    chart.zoom(0.9);
}
```

## Example 2: Interactive Legend and Data Selection

This example shows how to create an interactive legend that allows toggling datasets and selecting data ranges.

### Flask Implementation
```python
@app.route('/api/multi-series-data')
def multi_series_data():
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [
            {
                'label': 'Product A',
                'data': [65, 59, 80, 81, 56, 55],
                'borderColor': 'rgb(255, 99, 132)',
                'hidden': false
            },
            {
                'label': 'Product B',
                'data': [28, 48, 40, 19, 86, 27],
                'borderColor': 'rgb(54, 162, 235)',
                'hidden': false
            },
            {
                'label': 'Product C',
                'data': [45, 25, 16, 36, 67, 18],
                'borderColor': 'rgb(75, 192, 192)',
                'hidden': false
            }
        ]
    }
    return jsonify(data)
```

### Interactive Legend Configuration
```javascript
const config = {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                onClick: function(e, legendItem, legend) {
                    const index = legendItem.datasetIndex;
                    const ci = legend.chart;
                    
                    if (ci.isDatasetVisible(index)) {
                        ci.hide(index);
                        legendItem.hidden = true;
                    } else {
                        ci.show(index);
                        legendItem.hidden = false;
                    }
                    
                    updateSelectionSummary(ci);
                }
            }
        }
    }
};

function updateSelectionSummary(chart) {
    const visibleDatasets = chart.data.datasets.filter((d, i) => 
        chart.isDatasetVisible(i)
    );
    
    const summary = {
        count: visibleDatasets.length,
        total: visibleDatasets.reduce((sum, dataset) => 
            sum + dataset.data.reduce((a, b) => a + b, 0), 0
        )
    };
    
    document.getElementById('selectionSummary').innerHTML = `
        Showing ${summary.count} products
        Total: $${summary.total}
    `;
}
```

## Example 3: Interactive Data Analysis

This example demonstrates advanced interactivity with data analysis features.

### Flask Implementation
```python
@app.route('/api/analysis-data')
def analysis_data():
    data = {
        'labels': list(range(24)),  # 24 hours
        'datasets': [{
            'label': 'Hourly Sales',
            'data': generate_hourly_data(),
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }
    return jsonify(data)

@app.route('/api/analyze-range', methods=['POST'])
def analyze_range():
    data = request.json
    start_hour = data['start']
    end_hour = data['end']
    
    # Perform analysis on the selected range
    analysis = {
        'average': calculate_average(start_hour, end_hour),
        'peak': find_peak(start_hour, end_hour),
        'trend': calculate_trend(start_hour, end_hour)
    }
    return jsonify(analysis)
```

### Analysis Tools Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Hour'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Sales ($)'
                }
            }
        },
        onClick: function(event, elements) {
            if (elements.length > 0) {
                const element = elements[0];
                toggleSelection(element.index);
            }
        }
    }
};

let selectedRange = {start: null, end: null};

function toggleSelection(index) {
    if (selectedRange.start === null) {
        selectedRange.start = index;
    } else if (selectedRange.end === null) {
        selectedRange.end = index;
        if (selectedRange.end < selectedRange.start) {
            [selectedRange.start, selectedRange.end] = 
                [selectedRange.end, selectedRange.start];
        }
        analyzeRange();
    } else {
        selectedRange = {start: index, end: null};
    }
    
    highlightSelection();
}

function highlightSelection() {
    const datasets = chart.data.datasets;
    datasets[0].backgroundColor = datasets[0].data.map((_, i) => {
        if (selectedRange.start !== null && 
            selectedRange.end !== null && 
            i >= selectedRange.start && 
            i <= selectedRange.end) {
            return 'rgba(255, 99, 132, 0.2)';
        }
        return 'rgba(75, 192, 192, 0.2)';
    });
    chart.update();
}

function analyzeRange() {
    fetch('/api/analyze-range', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start: selectedRange.start,
            end: selectedRange.end
        })
    })
    .then(response => response.json())
    .then(analysis => {
        document.getElementById('analysisResults').innerHTML = `
            <h4>Analysis Results</h4>
            <p>Average: $${analysis.average}</p>
            <p>Peak: $${analysis.peak}</p>
            <p>Trend: ${analysis.trend}</p>
        `;
    });
}
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for interactive data analysis:

```python
class SalesData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    product = db.Column(db.String(50))
    
    @staticmethod
    def analyze_period(start_date, end_date, product=None):
        query = SalesData.query\
            .filter(SalesData.timestamp.between(start_date, end_date))
            
        if product:
            query = query.filter_by(product=product)
            
        data = query.all()
        
        return {
            'total': sum(d.amount for d in data),
            'average': sum(d.amount for d in data) / len(data) if data else 0,
            'count': len(data),
            'peak': max(d.amount for d in data) if data else 0,
            'trend': calculate_trend([d.amount for d in data])
        }

def calculate_trend(values):
    if len(values) < 2:
        return 'Insufficient data'
    
    slope = (values[-1] - values[0]) / len(values)
    if slope > 0:
        return 'Increasing'
    elif slope < 0:
        return 'Decreasing'
    return 'Stable'
```

This documentation provides three distinct examples of interactive charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic click interactions to advanced features like zoom/pan controls and data analysis tools.
