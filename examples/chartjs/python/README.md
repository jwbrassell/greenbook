# ChartJS with Python/Flask Examples

This directory contains complete examples of ChartJS integration with Python/Flask.

## Examples Overview

1. Basic Charts
   - Line chart with real-time updates
   - Bar chart with database integration
   - Pie chart with dynamic data
   - Area chart with date-based data

2. Advanced Features
   - Mixed chart types
   - Custom animations
   - Interactive legends
   - Responsive layouts

3. Data Integration
   - SQLAlchemy integration
   - REST API endpoints
   - WebSocket real-time updates
   - CSV/JSON data import

4. Full Applications
   - Dashboard example
   - Analytics platform
   - Data visualization tool
   - Reporting system

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
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html
│   ├── pie_chart/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html
│   └── area_chart/
│       ├── app.py
│       ├── requirements.txt
│       └── templates/
│           └── index.html
├── advanced/
│   ├── mixed_charts/
│   ├── animations/
│   ├── interactions/
│   └── responsive/
├── integration/
│   ├── database_example/
│   ├── api_example/
│   ├── websocket_example/
│   └── data_import/
└── applications/
    ├── dashboard/
    ├── analytics/
    ├── visualization/
    └── reporting/
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

### Line Chart Example
```python
from flask import Flask, render_template, jsonify
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    data = {
        'labels': [datetime.now().strftime('%H:%M:%S')],
        'datasets': [{
            'label': 'Real-time Data',
            'data': [random.randint(0, 100)],
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.1
        }]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
```

### Bar Chart with Database
```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50))
    value = db.Column(db.Float)

@app.route('/')
def index():
    data = Data.query.all()
    labels = [d.label for d in data]
    values = [d.value for d in data]
    return render_template('index.html', labels=labels, values=values)
```

## Advanced Examples

### Mixed Chart Types
```python
@app.route('/mixed-data')
def get_mixed_data():
    return {
        'labels': ['Jan', 'Feb', 'Mar'],
        'datasets': [
            {
                'type': 'line',
                'label': 'Line Dataset',
                'data': [10, 20, 15]
            },
            {
                'type': 'bar',
                'label': 'Bar Dataset',
                'data': [12, 19, 17]
            }
        ]
    }
```

### Real-time Updates
```python
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

def background_task():
    while True:
        socketio.emit('data_update', {
            'value': random.randint(0, 100),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()
```

## Security Considerations

1. Input Validation:
```python
from flask import request
from werkzeug.exceptions import BadRequest

@app.route('/api/data', methods=['POST'])
def update_data():
    data = request.get_json()
    if not isinstance(data.get('value'), (int, float)):
        raise BadRequest("Invalid data format")
    # Process data
```

2. CSRF Protection:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'your-secret-key'
```

## Performance Optimization

1. Data Caching:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/chart-data')
@cache.cached(timeout=60)
def get_chart_data():
    # Expensive data processing
    return process_data()
```

2. Lazy Loading:
```javascript
// templates/index.html
document.addEventListener('DOMContentLoaded', function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadChart(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });

    document.querySelectorAll('.chart-container').forEach(chart => {
        observer.observe(chart);
    });
});
```

## Testing

1. Unit Tests:
```python
import unittest

class TestChartAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_data_format(self):
        response = self.client.get('/api/data')
        data = response.get_json()
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
```

2. Integration Tests:
```python
def test_database_integration():
    with app.app_context():
        # Add test data
        db.session.add(Data(label='Test', value=100))
        db.session.commit()
        
        # Verify data appears in chart
        response = self.client.get('/')
        self.assertIn('Test', response.data.decode())
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
