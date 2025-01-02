# Chart.js Deployment with Flask

## Table of Contents
- [Chart.js Deployment with Flask](#chartjs-deployment-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Deployment Setup](#basic-deployment-setup)
    - [Flask Application Structure](#flask-application-structure)
    - [Production Configuration](#production-configuration)
- [config.py](#configpy)
    - [WSGI Entry Point](#wsgi-entry-point)
- [wsgi.py](#wsgipy)
    - [Dockerfile](#dockerfile)
- [Set working directory](#set-working-directory)
- [Install system dependencies](#install-system-dependencies)
- [Install Python dependencies](#install-python-dependencies)
- [Copy application code](#copy-application-code)
- [Set environment variables](#set-environment-variables)
- [Expose port](#expose-port)
- [Run gunicorn](#run-gunicorn)
  - [Example 1: Production-Ready Chart Implementation](#example-1:-production-ready-chart-implementation)
    - [Flask Implementation](#flask-implementation)
    - [Production Chart Template](#production-chart-template)
  - [Example 2: Load Balancing and High Availability](#example-2:-load-balancing-and-high-availability)
    - [Nginx Configuration](#nginx-configuration)
- [/etc/nginx/conf.d/charts.conf](#/etc/nginx/confd/chartsconf)
    - [Supervisor Configuration](#supervisor-configuration)
  - [Example 3: Monitoring and Error Handling](#example-3:-monitoring-and-error-handling)
    - [Flask Error Handling](#flask-error-handling)
- [Usage in routes](#usage-in-routes)
  - [Working with Production Data](#working-with-production-data)



Deploying Chart.js visualizations with Flask requires careful consideration of performance, security, and reliability. This guide demonstrates how to prepare and deploy Chart.js applications effectively.

## Basic Deployment Setup

### Flask Application Structure
```
myapp/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── static/
│   │   ├── js/
│   │   │   ├── charts.js
│   │   │   └── chart.min.js
│   │   └── css/
│   │       └── styles.css
│   └── templates/
│       └── charts/
│           └── dashboard.html
├── config.py
├── requirements.txt
├── wsgi.py
└── Dockerfile
```

### Production Configuration
```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chart.js specific configurations
    CHART_DATA_CACHE_TIMEOUT = 300  # 5 minutes
    MAX_DATA_POINTS = 10000
    ENABLE_CHART_EXPORT = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Production-specific chart settings
    CHART_DATA_COMPRESSION = True
    CHART_CACHE_ENABLED = True
    
    # CDN settings for Chart.js
    CHARTJS_CDN = 'https://cdn.jsdelivr.net/npm/chart.js'
    CHARTJS_VERSION = '3.9.1'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    
    # Development-specific chart settings
    CHART_DATA_COMPRESSION = False
    CHART_CACHE_ENABLED = False
```

### WSGI Entry Point
```python
# wsgi.py
from app import create_app
from config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == '__main__':
    app.run()
```

### Dockerfile
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

## Example 1: Production-Ready Chart Implementation

This example demonstrates how to implement production-ready charts with caching and optimization.

### Flask Implementation
```python
from flask import current_app
from flask_caching import Cache
from werkzeug.contrib.cache import RedisCache

cache = Cache()

class ChartDataManager:
    def __init__(self, cache_timeout=300):
        self.cache_timeout = cache_timeout
        self.cache = RedisCache(
            host=current_app.config['REDIS_HOST'],
            port=current_app.config['REDIS_PORT']
        )
    
    def get_chart_data(self, chart_id, params=None):
        """Get chart data with caching"""
        cache_key = self._generate_cache_key(chart_id, params)
        
        # Try to get from cache
        data = self.cache.get(cache_key)
        if data is not None:
            return data
        
        # Generate new data
        data = self._generate_chart_data(chart_id, params)
        
        # Cache the result
        self.cache.set(cache_key, data, timeout=self.cache_timeout)
        
        return data
    
    def _generate_cache_key(self, chart_id, params):
        """Generate unique cache key"""
        if params:
            param_str = '_'.join(f"{k}:{v}" for k, v in sorted(params.items()))
            return f"chart_{chart_id}_{param_str}"
        return f"chart_{chart_id}"
    
    def _generate_chart_data(self, chart_id, params):
        """Generate chart data based on ID and parameters"""
        # Implement your data generation logic here
        pass

@app.route('/api/chart-data/<chart_id>')
@cache.cached(timeout=300)
def get_chart_data(chart_id):
    manager = ChartDataManager()
    data = manager.get_chart_data(
        chart_id,
        request.args.to_dict()
    )
    return jsonify(data)
```

### Production Chart Template
```html
{% extends "base.html" %}

{% block head %}
<!-- Load Chart.js from CDN with SRI hash -->
<script 
    src="{{ config.CHARTJS_CDN }}"
    integrity="sha384-..." 
    crossorigin="anonymous">
</script>

<!-- Load compressed application charts -->
<script src="{{ url_for('static', filename='js/charts.min.js') }}"></script>
{% endblock %}

{% block content %}
<div class="chart-container" 
     data-chart-id="{{ chart_id }}"
     data-api-url="{{ url_for('api.get_chart_data', chart_id=chart_id) }}">
    <canvas id="productionChart"></canvas>
    <div class="chart-loader" style="display: none;">Loading...</div>
    <div class="chart-error" style="display: none;">Error loading chart data</div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.chart-container');
    const loader = container.querySelector('.chart-loader');
    const error = container.querySelector('.chart-error');
    
    // Initialize with error handling and loading states
    initializeChart(container, loader, error).catch(err => {
        console.error('Chart initialization failed:', err);
        error.style.display = 'block';
    });
});
</script>
{% endblock %}
```

## Example 2: Load Balancing and High Availability

This example shows how to implement load balancing and high availability for chart data.

### Nginx Configuration
```nginx
# /etc/nginx/conf.d/charts.conf
upstream chart_servers {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 80;
    server_name charts.example.com;

    location / {
        proxy_pass http://chart_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSocket support for real-time charts
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Cache static Chart.js files
        location /static/ {
            expires 1y;
            add_header Cache-Control "public, no-transform";
        }
        
        # Cache chart data responses
        location /api/chart-data/ {
            proxy_cache chart_cache;
            proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
            proxy_cache_valid 200 5m;
            add_header X-Cache-Status $upstream_cache_status;
        }
    }
}
```

### Supervisor Configuration
```ini
; /etc/supervisor/conf.d/charts.conf
[program:charts]
command=/usr/local/bin/gunicorn wsgi:app -w 4 -b 127.0.0.1:%(process_num)s
process_name=charts_%(process_num)s
numprocs=3
numprocs_start=5000
directory=/path/to/your/app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/charts/%(program_name)s_stderr.log
stdout_logfile=/var/log/charts/%(program_name)s_stdout.log
```

## Example 3: Monitoring and Error Handling

This example demonstrates how to implement monitoring and error handling for production charts.

### Flask Error Handling
```python
from flask import jsonify, current_app
import sentry_sdk

sentry_sdk.init(dsn="your-sentry-dsn")

class ChartError(Exception):
    """Base class for chart-related errors"""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code

@app.errorhandler(ChartError)
def handle_chart_error(error):
    response = jsonify({
        'error': str(error),
        'status_code': error.status_code
    })
    response.status_code = error.status_code
    return response

class ChartMonitor:
    def __init__(self):
        self.metrics = {}
    
    def record_render_time(self, chart_id, duration):
        """Record chart rendering time"""
        if chart_id not in self.metrics:
            self.metrics[chart_id] = {
                'render_times': [],
                'error_count': 0
            }
        self.metrics[chart_id]['render_times'].append(duration)
    
    def record_error(self, chart_id, error):
        """Record chart error"""
        if chart_id not in self.metrics:
            self.metrics[chart_id] = {
                'render_times': [],
                'error_count': 0
            }
        self.metrics[chart_id]['error_count'] += 1
        
        # Log to Sentry if error rate is high
        if self.metrics[chart_id]['error_count'] > 10:
            sentry_sdk.capture_exception(error)
    
    def get_metrics(self, chart_id):
        """Get metrics for a specific chart"""
        if chart_id not in self.metrics:
            return None
        
        metrics = self.metrics[chart_id]
        render_times = metrics['render_times']
        
        return {
            'average_render_time': sum(render_times) / len(render_times),
            'error_rate': metrics['error_count'] / len(render_times),
            'total_renders': len(render_times)
        }

# Usage in routes
@app.route('/api/chart-data/<chart_id>')
def get_chart_data(chart_id):
    monitor = ChartMonitor()
    start_time = time.time()
    
    try:
        data = generate_chart_data(chart_id)
        duration = time.time() - start_time
        monitor.record_render_time(chart_id, duration)
        return jsonify(data)
    except Exception as e:
        monitor.record_error(chart_id, e)
        raise ChartError(str(e))
```

## Working with Production Data

Here's how to implement efficient data handling for production:

```python
class ProductionDataManager:
    def __init__(self):
        self.db = SQLAlchemy()
        self.cache = RedisCache()
    
    def get_chart_data(self, chart_id, params=None):
        """Get production chart data with caching and error handling"""
        try:
            # Try cache first
            cache_key = f"chart_{chart_id}"
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return cached_data
            
            # Query database
            data = self.db.session.execute(
                """
                SELECT date_trunc('hour', timestamp) as time,
                       avg(value) as value
                FROM measurements
                WHERE chart_id = :chart_id
                GROUP BY date_trunc('hour', timestamp)
                ORDER BY time DESC
                LIMIT 1000
                """,
                {'chart_id': chart_id}
            ).fetchall()
            
            # Format data for Chart.js
            formatted_data = {
                'labels': [row[0].isoformat() for row in data],
                'datasets': [{
                    'data': [float(row[1]) for row in data]
                }]
            }
            
            # Cache the result
            self.cache.set(cache_key, formatted_data, timeout=300)
            
            return formatted_data
            
        except Exception as e:
            current_app.logger.error(f"Error getting chart data: {e}")
            sentry_sdk.capture_exception(e)
            raise ChartError("Failed to retrieve chart data")
    
    def update_chart_data(self, chart_id, new_data):
        """Update chart data in production"""
        try:
            # Update database
            self.db.session.execute(
                """
                INSERT INTO measurements (chart_id, value, timestamp)
                VALUES (:chart_id, :value, :timestamp)
                """,
                {
                    'chart_id': chart_id,
                    'value': new_data['value'],
                    'timestamp': new_data['timestamp']
                }
            )
            self.db.session.commit()
            
            # Invalidate cache
            self.cache.delete(f"chart_{chart_id}")
            
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"Error updating chart data: {e}")
            sentry_sdk.capture_exception(e)
            raise ChartError("Failed to update chart data")
```

This documentation provides three distinct examples of Chart.js deployment with varying complexity and features. Each example demonstrates different aspects of deployment when integrated with Flask, from basic production setup to advanced features like load balancing and monitoring.
