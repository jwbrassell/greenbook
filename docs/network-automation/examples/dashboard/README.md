# Network Monitoring Dashboard

A Flask-based dashboard for real-time network monitoring and visualization. This example demonstrates how to implement network monitoring concepts covered in the documentation.

## Features

- Real-time device monitoring
- System metrics visualization
- Interface statistics tracking
- Alert management
- Email notifications
- Historical data tracking
- Interactive charts
- Responsive design

## Prerequisites

1. Python 3.7+
2. Network devices with API access
3. SMTP server for alerts (optional)
4. PostgreSQL database (optional, for historical data)

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```env
   # Flask Settings
   FLASK_APP=app.py
   FLASK_ENV=development
   FLASK_DEBUG=True
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000

   # Network Devices
   NETWORK_DEVICES=device1.example.com,device2.example.com
   NETWORK_USER=admin
   NETWORK_PASSWORD=your_secure_password

   # Alert Thresholds
   ALERT_CPU_THRESHOLD=80
   ALERT_MEMORY_THRESHOLD=90
   ALERT_ERROR_THRESHOLD=100
   ALERT_TEMP_THRESHOLD=75

   # Email Notifications
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USER=alerts@example.com
   SMTP_PASSWORD=your_smtp_password
   ALERT_FROM_ADDRESS=alerts@example.com
   ALERT_TO_ADDRESSES=admin1@example.com,admin2@example.com

   # Database (Optional)
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=network_monitoring
   DB_USER=postgres
   DB_PASSWORD=your_db_password
   ```

## Usage

1. Start the Flask application:
   ```bash
   flask run
   ```

2. Access the dashboard:
   - Open a web browser
   - Navigate to `http://localhost:5000`
   - The dashboard will automatically refresh every 60 seconds

## Components

### 1. Flask Application (`app.py`)
- Main web application
- API endpoints
- Route handlers
- Dashboard rendering

### 2. Metric Collectors (`collectors.py`)
- Network device monitoring
- System metrics collection
- Interface statistics
- Data aggregation

### 3. Alert Manager (`alerts.py`)
- Threshold monitoring
- Alert generation
- Email notifications
- Alert history tracking

### 4. Dashboard Template (`templates/index.html`)
- Real-time visualization
- Interactive charts
- Device status display
- Alert notifications

## API Endpoints

### Device Metrics
- `GET /api/metrics/current`: Get current metrics for all devices
- `GET /api/metrics/history`: Get historical metrics
- `GET /api/devices`: Get list of monitored devices
- `GET /api/interfaces/<device>`: Get interface metrics for a device

### Alerts
- `GET /api/alerts`: Get current active alerts
- `GET /api/config`: Get dashboard configuration

## Customization

### Adding New Metrics
1. Update `collectors.py` with new metric collection methods
2. Add new visualization in `templates/index.html`
3. Update API endpoints in `app.py`

### Modifying Alerts
1. Add new thresholds in `alerts.py`
2. Update alert checking logic
3. Modify notification templates

### Custom Visualizations
1. Add new Chart.js configurations
2. Create new API endpoints for data
3. Update dashboard layout

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8
isort .
```

### Adding New Features
1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit pull request

## Troubleshooting

### Common Issues

1. Connection Errors
   - Check network device accessibility
   - Verify API credentials
   - Confirm network settings

2. Visualization Issues
   - Check browser console for errors
   - Verify data format
   - Confirm Chart.js initialization

3. Alert Problems
   - Verify SMTP settings
   - Check alert thresholds
   - Monitor log files

## Security Considerations

1. Credential Management
   - Use environment variables
   - Rotate passwords regularly
   - Implement proper access control

2. API Security
   - Enable HTTPS
   - Implement authentication
   - Use rate limiting

3. Data Protection
   - Encrypt sensitive data
   - Implement secure sessions
   - Regular security audits

## Related Documentation
- [Network Automation Guide](../../README.md)
- [Working with APIs](../../02-working-with-apis.md)
- [Security Best Practices](../../03-security-best-practices.md)
- [Monitoring and Visualization](../../04-monitoring-and-visualization.md)
