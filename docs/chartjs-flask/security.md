# Chart.js Security with Flask

## Table of Contents
- [Chart.js Security with Flask](#chartjs-security-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Security Implementation](#basic-security-implementation)
    - [Flask Security Configuration](#flask-security-configuration)
- [Enable security headers](#enable-security-headers)
- [Secret key for data signing](#secret-key-for-data-signing)
    - [Secure Template Implementation](#secure-template-implementation)
  - [Example 1: Data Validation and Sanitization](#example-1:-data-validation-and-sanitization)
    - [Flask Implementation](#flask-implementation)
  - [Example 2: Access Control and Authentication](#example-2:-access-control-and-authentication)
    - [Flask Implementation](#flask-implementation)
  - [Example 3: XSS Prevention and Input Validation](#example-3:-xss-prevention-and-input-validation)
    - [Flask Implementation](#flask-implementation)
  - [Working with Sensitive Data](#working-with-sensitive-data)



Security is crucial when implementing Chart.js visualizations in a Flask application. This guide demonstrates how to implement security best practices and protect against common vulnerabilities.

## Basic Security Implementation

### Flask Security Configuration
```python
from flask import Flask, request, abort
from flask_talisman import Talisman
from functools import wraps
import hmac
import hashlib

app = Flask(__name__)

# Enable security headers
Talisman(app, 
    content_security_policy={
        'default-src': "'self'",
        'script-src': [
            "'self'",
            'cdn.jsdelivr.net',  # Chart.js CDN
            "'unsafe-inline'"    # For inline chart configurations
        ],
        'style-src': ["'self'", "'unsafe-inline'"],
        'img-src': ["'self'", 'data:', 'blob:']  # For chart exports
    }
)

# Secret key for data signing
CHART_DATA_SECRET = 'your-secret-key'

def sign_data(data):
    """Sign data to prevent tampering"""
    message = str(data).encode()
    signature = hmac.new(
        CHART_DATA_SECRET.encode(),
        message,
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature(data, signature):
    """Verify data signature"""
    expected_signature = sign_data(data)
    return hmac.compare_digest(signature, expected_signature)

def require_chart_access(f):
    """Decorator to check chart access permissions"""
    @wraps(f)
    def decorated_function(chart_id, *args, **kwargs):
        if not has_chart_access(chart_id):
            abort(403)
        return f(chart_id, *args, **kwargs)
    return decorated_function

@app.route('/api/chart-data/<chart_id>')
@require_chart_access
def get_chart_data(chart_id):
    data = generate_chart_data(chart_id)
    signature = sign_data(data)
    return jsonify({
        'data': data,
        'signature': signature
    })
```

### Secure Template Implementation
```html
{% extends "base.html" %}

{% block head %}
<!-- Load Chart.js from CDN with SRI hash -->
<script 
    src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"
    integrity="sha384-..." 
    crossorigin="anonymous">
</script>

<!-- Load secure chart initialization -->
<script src="{{ url_for('static', filename='js/secure-charts.js') }}"></script>
{% endblock %}

{% block content %}
<div class="chart-container"
     data-chart-id="{{ chart_id|escape }}"
     data-csrf-token="{{ csrf_token() }}">
    <canvas id="secureChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.chart-container');
    const chartId = container.dataset.chartId;
    const csrfToken = container.dataset.csrfToken;
    
    // Initialize chart with security measures
    initializeSecureChart(container, {
        chartId: chartId,
        csrfToken: csrfToken,
        verifySignature: true
    });
});
</script>
{% endblock %}
```

## Example 1: Data Validation and Sanitization

This example demonstrates how to implement proper data validation and sanitization.

### Flask Implementation
```python
from marshmallow import Schema, fields, validate
import bleach

class ChartDataSchema(Schema):
    """Schema for validating chart data"""
    labels = fields.List(fields.String(validate=validate.Length(max=100)))
    datasets = fields.List(fields.Dict(keys=fields.Str(), values=fields.Raw()))
    options = fields.Dict(keys=fields.Str(), values=fields.Raw())

class ChartSecurity:
    def __init__(self):
        self.schema = ChartDataSchema()
    
    def validate_data(self, data):
        """Validate chart data structure"""
        result = self.schema.load(data)
        return result
    
    def sanitize_labels(self, labels):
        """Sanitize chart labels"""
        return [bleach.clean(label) for label in labels]
    
    def sanitize_data(self, data):
        """Sanitize chart data"""
        if isinstance(data, (int, float)):
            return data
        if isinstance(data, str):
            return bleach.clean(data)
        if isinstance(data, list):
            return [self.sanitize_data(item) for item in data]
        if isinstance(data, dict):
            return {
                bleach.clean(k): self.sanitize_data(v)
                for k, v in data.items()
            }
        return data

@app.route('/api/chart-data/<chart_id>')
def get_chart_data(chart_id):
    security = ChartSecurity()
    
    # Get raw data
    raw_data = generate_chart_data(chart_id)
    
    try:
        # Validate data structure
        validated_data = security.validate_data(raw_data)
        
        # Sanitize data
        validated_data['labels'] = security.sanitize_labels(
            validated_data['labels']
        )
        for dataset in validated_data['datasets']:
            dataset['label'] = bleach.clean(dataset['label'])
            dataset['data'] = security.sanitize_data(dataset['data'])
        
        return jsonify(validated_data)
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
```

## Example 2: Access Control and Authentication

This example shows how to implement proper access control for charts.

### Flask Implementation
```python
from flask_login import login_required, current_user
from functools import wraps

class ChartPermission:
    def __init__(self, chart_id):
        self.chart_id = chart_id
    
    def can_view(self, user):
        """Check if user can view chart"""
        if user.is_admin:
            return True
            
        chart = Chart.query.get(self.chart_id)
        if not chart:
            return False
            
        return (
            chart.is_public or
            chart.owner_id == user.id or
            user.id in [u.id for u in chart.shared_with]
        )
    
    def can_edit(self, user):
        """Check if user can edit chart"""
        chart = Chart.query.get(self.chart_id)
        if not chart:
            return False
            
        return (
            user.is_admin or
            chart.owner_id == user.id
        )

def require_chart_permission(permission='view'):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(chart_id, *args, **kwargs):
            chart_permission = ChartPermission(chart_id)
            
            if permission == 'view' and not chart_permission.can_view(current_user):
                abort(403)
            elif permission == 'edit' and not chart_permission.can_edit(current_user):
                abort(403)
                
            return f(chart_id, *args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/chart-data/<chart_id>')
@require_chart_permission('view')
def get_chart_data(chart_id):
    return jsonify(generate_chart_data(chart_id))

@app.route('/api/chart-update/<chart_id>', methods=['POST'])
@require_chart_permission('edit')
def update_chart(chart_id):
    data = request.get_json()
    return jsonify(update_chart_data(chart_id, data))
```

## Example 3: XSS Prevention and Input Validation

This example demonstrates how to prevent XSS attacks and validate user input.

### Flask Implementation
```python
from html import escape
import re

class ChartInputValidator:
    def __init__(self):
        self.allowed_patterns = {
            'label': re.compile(r'^[\w\s-]{1,100}$'),
            'number': re.compile(r'^-?\d*\.?\d+$'),
            'date': re.compile(r'^\d{4}-\d{2}-\d{2}$')
        }
    
    def validate_label(self, label):
        """Validate chart label"""
        if not self.allowed_patterns['label'].match(label):
            raise ValueError(f"Invalid label format: {label}")
        return escape(label)
    
    def validate_data_point(self, value):
        """Validate chart data point"""
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            if not self.allowed_patterns['number'].match(value):
                raise ValueError(f"Invalid number format: {value}")
            return float(value)
        raise ValueError(f"Invalid data type: {type(value)}")
    
    def validate_date(self, date_str):
        """Validate date string"""
        if not self.allowed_patterns['date'].match(date_str):
            raise ValueError(f"Invalid date format: {date_str}")
        return date_str

class SecureChartRenderer:
    def __init__(self):
        self.validator = ChartInputValidator()
    
    def render_chart_config(self, data):
        """Render secure chart configuration"""
        # Validate and sanitize labels
        labels = [
            self.validator.validate_label(label)
            for label in data.get('labels', [])
        ]
        
        # Validate and sanitize datasets
        datasets = []
        for dataset in data.get('datasets', []):
            clean_dataset = {
                'label': self.validator.validate_label(dataset.get('label', '')),
                'data': [
                    self.validator.validate_data_point(value)
                    for value in dataset.get('data', [])
                ]
            }
            datasets.append(clean_dataset)
        
        return {
            'type': 'line',  # Only allow specific chart types
            'data': {
                'labels': labels,
                'datasets': datasets
            },
            'options': {
                'plugins': {
                    'tooltip': {
                        'callbacks': {
                            'label': 'function(context) { return context.raw; }'
                        }
                    }
                }
            }
        }

@app.route('/api/secure-chart/<chart_id>')
def get_secure_chart(chart_id):
    try:
        raw_data = get_chart_data(chart_id)
        renderer = SecureChartRenderer()
        config = renderer.render_chart_config(raw_data)
        return jsonify(config)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
```

## Working with Sensitive Data

Here's how to implement secure data handling for sensitive information:

```python
from cryptography.fernet import Fernet
import base64

class SecureDataManager:
    def __init__(self, encryption_key):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_data(self, data):
        """Encrypt sensitive chart data"""
        json_data = json.dumps(data)
        encrypted = self.fernet.encrypt(json_data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive chart data"""
        encrypted = base64.b64decode(encrypted_data)
        decrypted = self.fernet.decrypt(encrypted)
        return json.loads(decrypted)
    
    def mask_sensitive_values(self, data, threshold=1000):
        """Mask sensitive values in chart data"""
        if isinstance(data, (int, float)) and data > threshold:
            return '***'
        if isinstance(data, list):
            return [self.mask_sensitive_values(v, threshold) for v in data]
        if isinstance(data, dict):
            return {
                k: self.mask_sensitive_values(v, threshold)
                for k, v in data.items()
            }
        return data

class SecureChartData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.String(50))
    encrypted_data = db.Column(db.Text)
    access_level = db.Column(db.String(20))
    
    @classmethod
    def get_secure_data(cls, chart_id, user):
        """Get secure chart data based on user's access level"""
        record = cls.query.filter_by(chart_id=chart_id).first()
        if not record:
            return None
            
        manager = SecureDataManager(current_app.config['ENCRYPTION_KEY'])
        data = manager.decrypt_data(record.encrypted_data)
        
        # Apply data masking based on access level
        if user.access_level < record.access_level:
            data = manager.mask_sensitive_values(data)
            
        return data
```

This documentation provides three distinct examples of Chart.js security implementations with varying complexity and features. Each example demonstrates different aspects of security when integrated with Flask, from basic data validation to advanced features like encryption and access control.
