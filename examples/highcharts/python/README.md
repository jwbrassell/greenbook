# Highcharts with Python/Flask Examples

## Table of Contents
- [Highcharts with Python/Flask Examples](#highcharts-with-pythonflask-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Examples](#basic-examples)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Charts
   - Line charts with real-time updates
   - Bar charts with database integration
   - Pie charts with dynamic data
   - Area charts with time series

2. Advanced Features
   - Stock charts with technical indicators
   - 3D visualizations
   - Drilldown capabilities
   - Export functionality

3. Data Integration
   - SQLAlchemy integration
   - REST API endpoints
   - WebSocket real-time updates
   - CSV/JSON data import

4. Full Applications
   - Financial dashboard
   - Analytics platform
   - Stock market monitor
   - Data visualization tool

## Project Structure

```
python/
├── basic/
│   ├── line_chart/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html
│   ├── bar_chart/
│   ├── pie_chart/
│   └── area_chart/
├── advanced/
│   ├── stock_charts/
│   ├── 3d_charts/
│   ├── drilldown/
│   └── export/
├── integration/
│   ├── database/
│   ├── api/
│   ├── websocket/
│   └── data_import/
└── applications/
    ├── financial_dashboard/
    ├── analytics/
    ├── stock_monitor/
    └── visualization/
```

## Getting Started

1. Setup Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3. Run Example:
```bash
cd basic/line_chart
python app.py
```

## Basic Examples

### Real-time Line Chart
```python
from flask import Flask, render_template, jsonify
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'value': random.randint(0, 100)
    })

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Highcharts Example</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/data.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
</head>
<body>
    <div id="chart"></div>
    
    <script>
        const chart = Highcharts.chart('chart', {
            chart: {
                type: 'line',
                events: {
                    load: function() {
                        const series = this.series[0];
                        setInterval(() => {
                            fetch('/data')
                                .then(response => response.json())
                                .then(data => {
                                    series.addPoint([
                                        data.timestamp,
                                        data.value
                                    ], true, series.data.length > 20);
                                });
                        }, 1000);
                    }
                }
            },
            title: {
                text: 'Real-time Data'
            },
            xAxis: {
                type: 'category'
            },
            series: [{
                name: 'Value',
                data: []
            }]
        });
    </script>
</body>
</html>
```

### Database Integration
```python
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class StockPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/stock/<symbol>')
def get_stock_data(symbol):
    # Get last 30 days of data
    start_date = datetime.utcnow() - timedelta(days=30)
    prices = StockPrice.query.filter(
        StockPrice.symbol == symbol,
        StockPrice.timestamp >= start_date
    ).order_by(StockPrice.timestamp).all()
    
    return jsonify({
        'data': [[p.timestamp.strftime('%Y-%m-%d'), p.price] for p in prices]
    })
```

## Advanced Features

### Stock Chart with Technical Indicators
```python
@app.route('/stock/technical/<symbol>')
def get_technical_data(symbol):
    # Get OHLC data
    data = get_stock_data(symbol)
    
    # Calculate technical indicators
    sma = calculate_sma(data, period=20)
    bollinger = calculate_bollinger_bands(data, period=20)
    
    return jsonify({
        'ohlc': data,
        'indicators': {
            'sma': sma,
            'bollinger': bollinger
        }
    })
```

```javascript
// Stock chart configuration
Highcharts.stockChart('container', {
    rangeSelector: {
        selected: 1
    },
    title: {
        text: 'Stock Price'
    },
    yAxis: [{
        title: {
            text: 'Price'
        },
        height: '60%'
    }, {
        title: {
            text: 'Volume'
        },
        top: '65%',
        height: '35%',
        offset: 0
    }],
    series: [{
        type: 'candlestick',
        name: 'Stock Price',
        data: ohlc
    }, {
        type: 'column',
        name: 'Volume',
        data: volume,
        yAxis: 1
    }]
});
```

### 3D Visualization
```python
@app.route('/3d-data')
def get_3d_data():
    # Generate 3D surface data
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    
    return jsonify({
        'x': x.tolist(),
        'y': y.tolist(),
        'z': Z.tolist()
    })
```

## Security Considerations

1. Input Validation:
```python
from marshmallow import Schema, fields, validate

class ChartDataSchema(Schema):
    symbol = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

@app.route('/api/data', methods=['POST'])
def get_chart_data():
    schema = ChartDataSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Process validated data
    return get_data_for_chart(data)
```

2. Rate Limiting:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/realtime-data')
@limiter.limit("1 per second")
def get_realtime_data():
    return get_latest_data()
```

## Performance Optimization

1. Data Aggregation:
```python
def get_aggregated_data(symbol, interval):
    """Aggregate data based on time interval"""
    query = """
        SELECT 
            time_bucket(:interval, timestamp) AS bucket,
            AVG(price) as avg_price,
            MAX(price) as high,
            MIN(price) as low
        FROM stock_prices
        WHERE symbol = :symbol
        GROUP BY bucket
        ORDER BY bucket
    """
    return db.session.execute(query, {
        'interval': interval,
        'symbol': symbol
    }).fetchall()
```

2. Caching:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/historical/<symbol>')
@cache.memoize(timeout=300)
def get_historical_data(symbol):
    """Cache historical data for 5 minutes"""
    return fetch_historical_data(symbol)
```

## Testing

1. Unit Tests:
```python
import unittest

class HighchartsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_data_format(self):
        response = self.client.get('/api/data/AAPL')
        data = response.get_json()
        self.assertIn('data', data)
        self.assertTrue(len(data['data']) > 0)
```

2. Integration Tests:
```python
def test_realtime_updates():
    with app.test_client() as client:
        # Connect to WebSocket
        ws = client.websocket('/ws')
        
        # Send subscription message
        ws.send_json({'action': 'subscribe', 'symbol': 'AAPL'})
        
        # Verify data updates
        data = ws.receive_json()
        self.assertIn('price', data)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
