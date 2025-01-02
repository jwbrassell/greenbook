# Candlestick Charts with Chart.js and Flask

## Table of Contents
- [Candlestick Charts with Chart.js and Flask](#candlestick-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Advanced Stock Analysis with Volume](#example-1:-advanced-stock-analysis-with-volume)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Real-time Trading Data](#example-2:-real-time-trading-data)
    - [Flask Implementation with WebSocket](#flask-implementation-with-websocket)
    - [Real-time Chart Configuration](#real-time-chart-configuration)
  - [Example 3: Technical Analysis Indicators](#example-3:-technical-analysis-indicators)
    - [Flask Implementation](#flask-implementation)
    - [Technical Analysis Configuration](#technical-analysis-configuration)
  - [Working with Database Data](#working-with-database-data)



Candlestick charts are essential tools for financial data visualization, particularly for stock market analysis. They show the open, high, low, and close (OHLC) prices for a given time period. This guide demonstrates how to implement candlestick charts using Chart.js with Flask.

## Basic Implementation

### Flask Route
```python
@app.route('/candlestick-chart')
def candlestick_chart():
    return render_template('candlestick_chart.html')

@app.route('/api/candlestick-data')
def candlestick_data():
    # Example: Daily stock price data
    data = {
        'labels': [
            '2023-01-01', '2023-01-02', '2023-01-03', 
            '2023-01-04', '2023-01-05'
        ],
        'datasets': [{
            'label': 'Stock Price',
            'data': [
                {'t': '2023-01-01', 'o': 150.23, 'h': 155.45, 'l': 149.89, 'c': 153.25},
                {'t': '2023-01-02', 'o': 153.25, 'h': 157.89, 'l': 152.78, 'c': 156.78},
                {'t': '2023-01-03', 'o': 156.78, 'h': 158.95, 'l': 154.56, 'c': 155.67},
                {'t': '2023-01-04', 'o': 155.67, 'h': 159.23, 'l': 154.89, 'c': 158.45},
                {'t': '2023-01-05', 'o': 158.45, 'h': 162.45, 'l': 157.89, 'c': 161.23}
            ],
            'color': {
                'up': 'rgba(75, 192, 192, 1)',
                'down': 'rgba(255, 99, 132, 1)',
                'unchanged': 'rgba(54, 162, 235, 1)'
            }
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="candlestickChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/candlestick-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('candlestickChart').getContext('2d');
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

## Example 1: Advanced Stock Analysis with Volume

This example shows how to create a candlestick chart with volume bars and moving averages.

### Flask Implementation
```python
@app.route('/api/advanced-stock-data')
def advanced_stock_data():
    data = {
        'candlestick': {
            'label': 'Stock Price',
            'data': generate_ohlc_data(),  # Your data generation function
            'color': {
                'up': 'rgba(75, 192, 192, 1)',
                'down': 'rgba(255, 99, 132, 1)'
            }
        },
        'volume': {
            'label': 'Volume',
            'data': generate_volume_data(),  # Your volume data
            'backgroundColor': function(context) {
                const price = context.chart.data.datasets[0].data[context.dataIndex];
                return price.o <= price.c ? 
                    'rgba(75, 192, 192, 0.3)' : 
                    'rgba(255, 99, 132, 0.3)';
            }
        },
        'ma20': {
            'label': '20-day MA',
            'data': calculate_moving_average(20),  # 20-day moving average
            'borderColor': 'rgba(255, 159, 64, 1)',
            'type': 'line'
        }
    }
    return jsonify(data)

def generate_ohlc_data():
    # Simulated OHLC data generation
    base_price = 100
    data = []
    for i in range(30):  # 30 days of data
        open_price = base_price + random.uniform(-2, 2)
        high_price = open_price + random.uniform(0, 3)
        low_price = open_price - random.uniform(0, 3)
        close_price = random.uniform(low_price, high_price)
        date = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
        
        data.append({
            't': date,
            'o': open_price,
            'h': high_price,
            'l': low_price,
            'c': close_price
        })
        base_price = close_price
    
    return data
```

### Advanced Configuration
```javascript
const config = {
    type: 'candlestick',
    data: {
        datasets: [
            {
                type: 'candlestick',
                data: chartData.candlestick.data,
                color: chartData.candlestick.color,
                yAxisID: 'price'
            },
            {
                type: 'bar',
                data: chartData.volume.data,
                backgroundColor: chartData.volume.backgroundColor,
                yAxisID: 'volume'
            },
            {
                type: 'line',
                data: chartData.ma20.data,
                borderColor: chartData.ma20.borderColor,
                yAxisID: 'price'
            }
        ]
    },
    options: {
        scales: {
            price: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Price ($)'
                }
            },
            volume: {
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

## Example 2: Real-time Trading Data

This example demonstrates how to implement a real-time updating candlestick chart.

### Flask Implementation with WebSocket
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    # Send initial data
    emit('initial_data', get_historical_data())

def get_historical_data():
    # Fetch historical data from database
    return {
        'labels': [...],
        'datasets': [{
            'label': 'Real-time Trading',
            'data': [...],
            'color': {
                'up': 'rgba(75, 192, 192, 1)',
                'down': 'rgba(255, 99, 132, 1)'
            }
        }]
    }

@socketio.on('new_trade')
def handle_trade(trade_data):
    # Process new trade data and emit update
    updated_data = process_trade_data(trade_data)
    emit('trade_update', updated_data, broadcast=True)
```

### Real-time Chart Configuration
```javascript
const config = {
    type: 'candlestick',
    data: chartData,
    options: {
        responsive: true,
        animation: {
            duration: 0  // Disable animation for real-time updates
        },
        plugins: {
            streaming: {
                duration: 20000,  // Show last 20 seconds
                refresh: 1000,    // Refresh every second
                delay: 1000,      // Delay of 1 second
                onRefresh: function(chart) {
                    // Update logic here
                }
            }
        },
        scales: {
            x: {
                type: 'realtime',
                realtime: {
                    duration: 20000,
                    refresh: 1000,
                    delay: 1000,
                    onRefresh: function(chart) {
                        // Real-time update logic
                    }
                }
            }
        }
    }
};

// WebSocket connection
const socket = io();
socket.on('trade_update', function(data) {
    // Update chart with new data
    updateChart(data);
});
```

## Example 3: Technical Analysis Indicators

This example shows how to add technical analysis indicators to a candlestick chart.

### Flask Implementation
```python
@app.route('/api/technical-analysis')
def technical_analysis():
    data = {
        'ohlc': generate_ohlc_data(),
        'indicators': {
            'sma': calculate_sma(20),    # Simple Moving Average
            'ema': calculate_ema(20),    # Exponential Moving Average
            'bb': calculate_bollinger_bands(20, 2),  # Bollinger Bands
            'rsi': calculate_rsi(14)     # Relative Strength Index
        }
    }
    return jsonify(data)

def calculate_bollinger_bands(period, std_dev):
    prices = get_closing_prices()
    sma = calculate_sma(period)
    std = calculate_standard_deviation(period)
    
    upper_band = [sma[i] + (std[i] * std_dev) for i in range(len(sma))]
    lower_band = [sma[i] - (std[i] * std_dev) for i in range(len(sma))]
    
    return {
        'middle': sma,
        'upper': upper_band,
        'lower': lower_band
    }
```

### Technical Analysis Configuration
```javascript
const config = {
    type: 'candlestick',
    data: {
        datasets: [
            {
                type: 'candlestick',
                data: chartData.ohlc,
                yAxisID: 'price'
            },
            {
                type: 'line',
                label: 'SMA 20',
                data: chartData.indicators.sma,
                borderColor: 'rgba(255, 159, 64, 1)',
                yAxisID: 'price'
            },
            {
                type: 'line',
                label: 'EMA 20',
                data: chartData.indicators.ema,
                borderColor: 'rgba(153, 102, 255, 1)',
                yAxisID: 'price'
            },
            {
                type: 'line',
                label: 'RSI',
                data: chartData.indicators.rsi,
                borderColor: 'rgba(201, 203, 207, 1)',
                yAxisID: 'rsi'
            }
        ]
    },
    options: {
        scales: {
            price: {
                type: 'linear',
                position: 'left'
            },
            rsi: {
                type: 'linear',
                position: 'right',
                min: 0,
                max: 100,
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic candlestick charts:

```python
class StockPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime)
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    volume = db.Column(db.Integer)

    @staticmethod
    def get_ohlc_data(symbol, start_date, end_date):
        prices = StockPrice.query\
            .filter(
                StockPrice.symbol == symbol,
                StockPrice.timestamp.between(start_date, end_date)
            )\
            .order_by(StockPrice.timestamp)\
            .all()
            
        return {
            'labels': [p.timestamp.strftime('%Y-%m-%d') for p in prices],
            'datasets': [{
                'label': symbol,
                'data': [{
                    't': p.timestamp.strftime('%Y-%m-%d'),
                    'o': p.open_price,
                    'h': p.high_price,
                    'l': p.low_price,
                    'c': p.close_price
                } for p in prices],
                'color': {
                    'up': 'rgba(75, 192, 192, 1)',
                    'down': 'rgba(255, 99, 132, 1)'
                }
            }]
        }
```

This documentation provides three distinct examples of candlestick charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like technical analysis indicators and real-time updates.
