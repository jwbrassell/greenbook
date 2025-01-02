# Financial Charts with Chart.js and Flask

## Table of Contents
- [Financial Charts with Chart.js and Flask](#financial-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Advanced Stock Analysis](#example-1:-advanced-stock-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Technical Analysis Indicators](#example-2:-technical-analysis-indicators)
    - [Flask Implementation](#flask-implementation)
    - [Technical Indicators Configuration](#technical-indicators-configuration)
  - [Example 3: Trading Volume Analysis](#example-3:-trading-volume-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Volume Analysis Configuration](#volume-analysis-configuration)
  - [Working with Database Data](#working-with-database-data)



Financial charts are specialized visualizations for displaying financial data such as stock prices, trading volumes, and market trends. While Chart.js doesn't have built-in financial chart types, we can create effective financial visualizations using custom configurations and plugins.

## Basic Implementation

### Flask Route
```python
@app.route('/financial-chart')
def financial_chart():
    return render_template('financial_chart.html')

@app.route('/api/stock-data')
def stock_data():
    # Example: Stock price data with OHLC values
    data = {
        'labels': [
            '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'
        ],
        'datasets': [{
            'label': 'Stock Price',
            'data': [
                {'o': 150.23, 'h': 155.45, 'l': 149.89, 'c': 153.25},
                {'o': 153.25, 'h': 157.89, 'l': 152.78, 'c': 156.78},
                {'o': 156.78, 'h': 158.95, 'l': 154.56, 'c': 155.67},
                {'o': 155.67, 'h': 159.23, 'l': 154.89, 'c': 158.45},
                {'o': 158.45, 'h': 162.45, 'l': 157.89, 'c': 161.23}
            ],
            'backgroundColor': function(context) {
                return context.raw.o > context.raw.c ? 
                    'rgba(255, 99, 132, 0.5)' : 
                    'rgba(75, 192, 192, 0.5)';
            },
            'borderColor': function(context) {
                return context.raw.o > context.raw.c ? 
                    'rgb(255, 99, 132)' : 
                    'rgb(75, 192, 192)';
            },
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="financialChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/stock-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('financialChart').getContext('2d');
            new Chart(ctx, {
                type: 'candlestick',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Stock Price Analysis'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return [
                                        `Open: $${context.raw.o.toFixed(2)}`,
                                        `High: $${context.raw.h.toFixed(2)}`,
                                        `Low: $${context.raw.l.toFixed(2)}`,
                                        `Close: $${context.raw.c.toFixed(2)}`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day'
                            },
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Price ($)'
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Advanced Stock Analysis

This example shows how to create a comprehensive stock analysis chart with volume data.

### Flask Implementation
```python
@app.route('/api/stock-analysis')
def stock_analysis():
    data = {
        'ohlc': {
            'labels': generate_dates(30),  # Last 30 days
            'datasets': [{
                'label': 'Stock Price',
                'data': generate_ohlc_data(30),
                'type': 'candlestick'
            }]
        },
        'volume': {
            'labels': generate_dates(30),
            'datasets': [{
                'label': 'Volume',
                'data': generate_volume_data(30),
                'type': 'bar',
                'backgroundColor': 'rgba(75, 192, 192, 0.3)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }]
        }
    }
    return jsonify(data)

def generate_ohlc_data(days):
    import random
    base_price = 100
    data = []
    for _ in range(days):
        open_price = base_price + random.uniform(-2, 2)
        high_price = open_price + random.uniform(0, 3)
        low_price = open_price - random.uniform(0, 3)
        close_price = random.uniform(low_price, high_price)
        base_price = close_price
        data.append({
            'o': open_price,
            'h': high_price,
            'l': low_price,
            'c': close_price
        })
    return data

def generate_volume_data(days):
    import random
    return [random.randint(100000, 1000000) for _ in range(days)]
```

### Advanced Configuration
```javascript
const config = {
    type: 'candlestick',
    data: chartData,
    options: {
        responsive: true,
        interaction: {
            mode: 'index',
            intersect: false,
        },
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
                        if (context.dataset.type === 'candlestick') {
                            return [
                                `Open: $${context.raw.o.toFixed(2)}`,
                                `High: $${context.raw.h.toFixed(2)}`,
                                `Low: $${context.raw.l.toFixed(2)}`,
                                `Close: $${context.raw.c.toFixed(2)}`
                            ];
                        } else {
                            return `Volume: ${context.raw.toLocaleString()}`;
                        }
                    }
                }
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day'
                }
            },
            y: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Price ($)'
                }
            },
            y2: {
                type: 'linear',
                position: 'right',
                title: {
                    display: true,
                    text: 'Volume'
                },
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    }
};
```

## Example 2: Technical Analysis Indicators

This example demonstrates how to add technical analysis indicators like moving averages.

### Flask Implementation
```python
@app.route('/api/technical-analysis')
def technical_analysis():
    data = {
        'labels': generate_dates(50),  # Last 50 days
        'datasets': [
            {
                'label': 'Stock Price',
                'data': generate_price_data(50),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'fill': false,
                'tension': 0.4
            },
            {
                'label': '20-day MA',
                'data': calculate_moving_average(20),
                'borderColor': 'rgba(255, 99, 132, 1)',
                'fill': false,
                'tension': 0.4
            },
            {
                'label': '50-day MA',
                'data': calculate_moving_average(50),
                'borderColor': 'rgba(54, 162, 235, 1)',
                'fill': false,
                'tension': 0.4
            }
        ]
    }
    return jsonify(data)

def calculate_moving_average(period):
    # Simulated moving average calculation
    prices = generate_price_data(50)
    ma = []
    for i in range(len(prices)):
        if i < period:
            ma.append(None)
        else:
            window = prices[i-period:i]
            ma.append(sum(window) / period)
    return ma
```

### Technical Indicators Configuration
```javascript
const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        tooltip: {
            mode: 'index',
            intersect: false
        }
    },
    scales: {
        x: {
            type: 'time',
            time: {
                unit: 'day'
            }
        },
        y: {
            title: {
                display: true,
                text: 'Price ($)'
            },
            ticks: {
                callback: function(value) {
                    return '$' + value.toFixed(2);
                }
            }
        }
    },
    interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
    }
};
```

## Example 3: Trading Volume Analysis

This example shows how to create a volume profile analysis chart.

### Flask Implementation
```python
@app.route('/api/volume-analysis')
def volume_analysis():
    data = {
        'labels': generate_dates(20),  # Last 20 days
        'datasets': [
            {
                'label': 'Price',
                'data': generate_price_data(20),
                'type': 'line',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'fill': false,
                'yAxisID': 'y'
            },
            {
                'label': 'Volume',
                'data': generate_volume_data(20),
                'type': 'bar',
                'backgroundColor': function(context) {
                    const price = context.chart.data.datasets[0].data[context.dataIndex];
                    const prevPrice = context.chart.data.datasets[0].data[context.dataIndex - 1];
                    return price > prevPrice ? 
                        'rgba(75, 192, 192, 0.5)' : 
                        'rgba(255, 99, 132, 0.5)';
                },
                'yAxisID': 'y1'
            }
        ]
    }
    return jsonify(data)
```

### Volume Analysis Configuration
```javascript
const config = {
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        if (context.dataset.yAxisID === 'y') {
                            return `Price: $${context.raw.toFixed(2)}`;
                        } else {
                            return `Volume: ${context.raw.toLocaleString()}`;
                        }
                    }
                }
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day'
                }
            },
            y: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Price ($)'
                }
            },
            y1: {
                type: 'linear',
                position: 'right',
                title: {
                    display: true,
                    text: 'Volume'
                },
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic financial charts:

```python
class StockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    volume = db.Column(db.Integer)
    symbol = db.Column(db.String(10))

    @staticmethod
    def get_stock_data(symbol, start_date, end_date):
        stock_data = StockData.query\
            .filter(
                StockData.symbol == symbol,
                StockData.date.between(start_date, end_date)
            )\
            .order_by(StockData.date)\
            .all()
            
        return {
            'labels': [data.date.strftime('%Y-%m-%d') for data in stock_data],
            'datasets': [
                {
                    'label': f'{symbol} Price',
                    'data': [{
                        'o': data.open_price,
                        'h': data.high_price,
                        'l': data.low_price,
                        'c': data.close_price
                    } for data in stock_data],
                    'type': 'candlestick'
                },
                {
                    'label': 'Volume',
                    'data': [data.volume for data in stock_data],
                    'type': 'bar',
                    'yAxisID': 'y1'
                }
            ]
        }
```

This documentation provides three distinct examples of financial charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like technical indicators and volume analysis.
