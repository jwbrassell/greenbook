# Candlestick Charts with Highcharts and Flask

## Table of Contents
- [Candlestick Charts with Highcharts and Flask](#candlestick-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Candlestick Charts](#tips-for-working-with-candlestick-charts)



## Overview

Candlestick charts are essential for visualizing financial data, particularly stock price movements. Each candlestick represents four key price points for a given time period: open, high, low, and close. The body of the candlestick shows the open and close prices, while the wicks (shadows) show the high and low prices. Typically, green or white candlesticks indicate price increases (close > open), while red or black candlesticks indicate price decreases (close < open).

## Basic Configuration

Here's how to create a basic candlestick chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

@app.route('/candlestick-chart')
def candlestick_chart():
    return render_template('candlestick-chart.html')

@app.route('/candlestick-data')
def candlestick_data():
    # Generate sample stock data for the past 30 days
    days = 30
    start_date = datetime.now() - timedelta(days=days)
    
    data = []
    price = 100  # Starting price
    
    for day in range(days):
        date = start_date + timedelta(days=day)
        timestamp = int(date.timestamp() * 1000)
        
        # Generate OHLC data
        open_price = price
        high_price = open_price * (1 + random.uniform(0, 0.03))
        low_price = open_price * (1 - random.uniform(0, 0.03))
        close_price = random.uniform(low_price, high_price)
        
        data.append([
            timestamp,
            round(open_price, 2),
            round(high_price, 2),
            round(low_price, 2),
            round(close_price, 2)
        ])
        
        price = close_price
    
    return jsonify(data)
```

```html
<!-- templates/candlestick-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="candlestick-container" style="min-width: 310px; height: 500px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/candlestick-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.stockChart('candlestick-container', {
                rangeSelector: {
                    selected: 1
                },
                title: {
                    text: 'Stock Price'
                },
                yAxis: {
                    title: {
                        text: 'Price ($)'
                    }
                },
                series: [{
                    type: 'candlestick',
                    name: 'Stock Price',
                    data: data,
                    tooltip: {
                        valueDecimals: 2
                    }
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate candlestick charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
db = SQLAlchemy(app)

class StockPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

@app.route('/stock-data/<symbol>')
def get_stock_data(symbol):
    prices = StockPrice.query.filter_by(symbol=symbol).order_by(StockPrice.timestamp).all()
    
    data = [[
        int(price.timestamp.timestamp() * 1000),
        price.open_price,
        price.high_price,
        price.low_price,
        price.close_price
    ] for price in prices]
    
    return jsonify(data)
```

## Tips for Working with Candlestick Charts

1. Use appropriate time intervals
2. Include volume data when possible
3. Add technical indicators
4. Implement proper tooltips
5. Consider color schemes
6. Add range selectors
7. Include zoom capabilities
8. Optimize for performance
