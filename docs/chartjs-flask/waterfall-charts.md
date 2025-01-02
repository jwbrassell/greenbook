# Waterfall Charts with Chart.js and Flask

## Table of Contents
- [Waterfall Charts with Chart.js and Flask](#waterfall-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Financial Statement Analysis](#example-1:-financial-statement-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Project Resource Tracking](#example-2:-project-resource-tracking)
    - [Flask Implementation](#flask-implementation)
    - [Resource Tracking Configuration](#resource-tracking-configuration)
  - [Example 3: Inventory Analysis](#example-3:-inventory-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Inventory Analysis Configuration](#inventory-analysis-configuration)
  - [Working with Database Data](#working-with-database-data)



Waterfall charts are effective for visualizing the cumulative effect of sequential positive and negative values, commonly used for financial statements, inventory analysis, and project resource tracking. While Chart.js doesn't have a built-in waterfall chart type, we can create them using bar charts with custom configurations.

## Basic Implementation

### Flask Route
```python
@app.route('/waterfall-chart')
def waterfall_chart():
    return render_template('waterfall_chart.html')

@app.route('/api/waterfall-data')
def waterfall_data():
    # Example: Monthly profit/loss analysis
    data = {
        'labels': ['Start', 'Revenue', 'Expenses', 'Taxes', 'End'],
        'datasets': [{
            'label': 'Profit/Loss Analysis',
            'data': [1000, 500, -300, -100, None],  # End value calculated in JS
            'backgroundColor': [
                'rgba(75, 192, 192, 0.8)',  # Start (green)
                'rgba(54, 162, 235, 0.8)',  # Positive (blue)
                'rgba(255, 99, 132, 0.8)',  # Negative (red)
                'rgba(255, 99, 132, 0.8)',  # Negative (red)
                'rgba(75, 192, 192, 0.8)'   # End (green)
            ],
            'borderColor': 'white',
            'borderWidth': 1,
            'cumulative': []  # Will store running totals
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="waterfallChart"></canvas>
</div>

<script>
// Calculate cumulative values for waterfall chart
function calculateCumulative(data) {
    let cumulative = [];
    let runningTotal = data[0];  // Start value
    cumulative.push(runningTotal);
    
    for (let i = 1; i < data.length - 1; i++) {
        runningTotal += data[i];
        cumulative.push(runningTotal);
    }
    
    // Set final value
    data[data.length - 1] = runningTotal;
    cumulative.push(runningTotal);
    
    return cumulative;
}

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/waterfall-data')
        .then(response => response.json())
        .then(data => {
            // Calculate and store cumulative values
            data.datasets[0].cumulative = calculateCumulative(data.datasets[0].data);
            
            const ctx = document.getElementById('waterfallChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Monthly Profit/Loss Analysis'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw;
                                    const cumulative = context.dataset.cumulative[context.dataIndex];
                                    return [
                                        `Change: ${value >= 0 ? '+' : ''}${value}`,
                                        `Total: ${cumulative}`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Amount ($)'
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Financial Statement Analysis

This example shows how to create a detailed financial statement waterfall chart.

### Flask Implementation
```python
@app.route('/api/financial-waterfall')
def financial_waterfall():
    data = {
        'labels': [
            'Opening Balance',
            'Revenue',
            'Cost of Goods',
            'Operating Expenses',
            'Interest',
            'Taxes',
            'Net Income'
        ],
        'datasets': [{
            'data': [
                1000000,    # Opening Balance
                500000,     # Revenue
                -300000,    # Cost of Goods
                -150000,    # Operating Expenses
                -25000,     # Interest
                -75000,     # Taxes
                None        # Net Income (calculated)
            ],
            'backgroundColor': function(context) {
                const value = context.raw;
                if (context.dataIndex === 0 || 
                    context.dataIndex === context.dataset.data.length - 1) {
                    return 'rgba(75, 192, 192, 0.8)';  # Total bars
                }
                return value >= 0 ? 
                    'rgba(54, 162, 235, 0.8)' :  # Positive
                    'rgba(255, 99, 132, 0.8)';   # Negative
            },
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.raw;
                        const cumulative = context.dataset.cumulative[context.dataIndex];
                        const formattedValue = new Intl.NumberFormat('en-US', {
                            style: 'currency',
                            currency: 'USD'
                        }).format(Math.abs(value));
                        
                        return [
                            `${context.label}: ${value >= 0 ? '+' : '-'}${formattedValue}`,
                            `Running Total: ${new Intl.NumberFormat('en-US', {
                                style: 'currency',
                                currency: 'USD'
                            }).format(cumulative)}`
                        ];
                    }
                }
            }
        },
        scales: {
            y: {
                ticks: {
                    callback: function(value) {
                        return new Intl.NumberFormat('en-US', {
                            style: 'currency',
                            currency: 'USD',
                            minimumFractionDigits: 0,
                            maximumFractionDigits: 0
                        }).format(value);
                    }
                }
            }
        }
    }
};
```

## Example 2: Project Resource Tracking

This example demonstrates how to track project resources with a waterfall chart.

### Flask Implementation
```python
@app.route('/api/resource-waterfall')
def resource_waterfall():
    data = {
        'labels': [
            'Initial Budget',
            'Design Phase',
            'Development',
            'Testing',
            'Marketing',
            'Contingency',
            'Remaining'
        ],
        'datasets': [{
            'label': 'Project Resources',
            'data': [
                100000,     # Initial Budget
                -15000,     # Design
                -45000,     # Development
                -20000,     # Testing
                -10000,     # Marketing
                5000,       # Contingency returned
                None        # Remaining (calculated)
            ],
            'backgroundColor': generate_resource_colors(),
            'borderWidth': 1,
            'annotations': [
                {
                    'type': 'line',
                    'mode': 'horizontal',
                    'scaleID': 'y',
                    'value': 20000,
                    'borderColor': 'red',
                    'borderWidth': 2,
                    'label': {
                        'content': 'Minimum Reserve',
                        'enabled': true
                    }
                }
            ]
        }]
    }
    return jsonify(data)

def generate_resource_colors():
    return [
        'rgba(75, 192, 192, 0.8)',  # Initial (green)
        'rgba(255, 99, 132, 0.8)',  # Expenses (red)
        'rgba(255, 99, 132, 0.8)',
        'rgba(255, 99, 132, 0.8)',
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',  # Returns (blue)
        'rgba(75, 192, 192, 0.8)'   # Final (green)
    ]
```

### Resource Tracking Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            annotation: {
                annotations: chartData.datasets[0].annotations
            }
        },
        scales: {
            y: {
                grace: '10%'  // Add space for annotations
            }
        },
        onClick: (event, elements) => {
            if (elements.length > 0) {
                const index = elements[0].index;
                showResourceDetails(index);
            }
        }
    }
};

function showResourceDetails(index) {
    // Implement modal with detailed breakdown
    const resourceData = {
        category: data.labels[index],
        amount: data.datasets[0].data[index],
        total: data.datasets[0].cumulative[index]
    };
    console.log('Resource Details:', resourceData);
}
```

## Example 3: Inventory Analysis

This example shows how to analyze inventory changes with a waterfall chart.

### Flask Implementation
```python
@app.route('/api/inventory-waterfall')
def inventory_waterfall():
    data = {
        'labels': [
            'Opening Stock',
            'Purchases',
            'Sales',
            'Returns',
            'Adjustments',
            'Closing Stock'
        ],
        'datasets': [{
            'label': 'Inventory Changes',
            'data': [
                5000,   # Opening Stock
                2000,   # Purchases
                -3000,  # Sales
                500,    # Returns
                -200,   # Adjustments
                None    # Closing Stock (calculated)
            ],
            'backgroundColor': function(context) {
                const value = context.raw;
                if (context.dataIndex === 0 || 
                    context.dataIndex === context.dataset.data.length - 1) {
                    return 'rgba(153, 102, 255, 0.8)';  # Stock bars
                }
                return value >= 0 ? 
                    'rgba(54, 162, 235, 0.8)' :  # Additions
                    'rgba(255, 99, 132, 0.8)';   # Reductions
            },
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### Inventory Analysis Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.raw;
                        const cumulative = context.dataset.cumulative[context.dataIndex];
                        return [
                            `Change: ${value >= 0 ? '+' : ''}${value} units`,
                            `Total Stock: ${cumulative} units`
                        ];
                    }
                }
            }
        },
        scales: {
            y: {
                title: {
                    display: true,
                    text: 'Units'
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic waterfall charts:

```python
class TransactionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    transaction_type = db.Column(db.String(20))  # 'start', 'change', 'end'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_waterfall_data(start_date, end_date):
        transactions = TransactionData.query\
            .filter(TransactionData.timestamp.between(start_date, end_date))\
            .order_by(TransactionData.timestamp)\
            .all()
            
        # Group transactions by category
        categories = []
        data = []
        colors = []
        
        for tx in transactions:
            categories.append(tx.category)
            data.append(tx.amount)
            
            if tx.transaction_type == 'start' or tx.transaction_type == 'end':
                colors.append('rgba(75, 192, 192, 0.8)')
            else:
                colors.append(
                    'rgba(54, 162, 235, 0.8)' if tx.amount >= 0 
                    else 'rgba(255, 99, 132, 0.8)'
                )
        
        return {
            'labels': categories,
            'datasets': [{
                'data': data,
                'backgroundColor': colors,
                'borderWidth': 1
            }]
        }
```

This documentation provides three distinct examples of waterfall charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like resource tracking and inventory analysis.
