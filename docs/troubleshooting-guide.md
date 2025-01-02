# Troubleshooting Guide: Console Logs, Flask Logs, and Browser Developer Tools

## Table of Contents
- [Troubleshooting Guide: Console Logs, Flask Logs, and Browser Developer Tools](#troubleshooting-guide:-console-logs,-flask-logs,-and-browser-developer-tools)
  - [JavaScript Console Logs](#javascript-console-logs)
    - [Basic Console Methods](#basic-console-methods)
    - [Advanced Console Techniques](#advanced-console-techniques)
  - [Flask Logging](#flask-logging)
    - [Basic Flask Logging Setup](#basic-flask-logging-setup)
- [Configure logging](#configure-logging)
    - [Advanced Flask Logging](#advanced-flask-logging)
  - [Browser Developer Tools](#browser-developer-tools)
    - [Network Tab](#network-tab)
    - [Console Tab](#console-tab)
    - [Elements Tab](#elements-tab)
    - [Application Tab](#application-tab)
    - [Performance Tab](#performance-tab)
    - [Memory Tab](#memory-tab)
  - [Best Practices](#best-practices)
  - [Common Debugging Scenarios](#common-debugging-scenarios)
  - [Troubleshooting Checklist](#troubleshooting-checklist)



## JavaScript Console Logs

### Basic Console Methods
```javascript
// Basic logging
console.log('Basic message');
console.info('Informational message');
console.warn('Warning message');
console.error('Error message');
console.debug('Debug message');

// Structured data logging
console.table([{ id: 1, name: 'Item 1' }, { id: 2, name: 'Item 2' }]);
console.dir(document.body, { depth: 2, colors: true });

// Grouping related logs
console.group('API Request');
console.log('Sending request...');
console.log('Response received');
console.groupEnd();

// Performance tracking
console.time('operation');
// ... some operations
console.timeEnd('operation');
```

### Advanced Console Techniques
1. **Conditional Logging**
   ```javascript
   // Only log in development
   if (process.env.NODE_ENV === 'development') {
       console.log('Debug info:', data);
   }
   ```

2. **Custom Console Styling**
   ```javascript
   console.log(
       '%cImportant Message', 
       'color: red; font-size: 20px; font-weight: bold;'
   );
   ```

3. **Stack Trace Logging**
   ```javascript
   console.trace('Tracking function calls');
   ```

## Flask Logging

### Basic Flask Logging Setup
```python
from flask import Flask
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

@app.route('/')
def index():
    app.logger.debug('Debug message')
    app.logger.info('Info message')
    app.logger.warning('Warning message')
    app.logger.error('Error message')
    return 'Hello World'
```

### Advanced Flask Logging
1. **Custom Log Formatters**
   ```python
   class RequestFormatter(logging.Formatter):
       def format(self, record):
           record.url = request.url
           record.remote_addr = request.remote_addr
           return super().format(record)
   ```

2. **Logging Different Levels to Different Files**
   ```python
   # Error logs
   error_handler = logging.FileHandler('error.log')
   error_handler.setLevel(logging.ERROR)
   
   # Info logs
   info_handler = logging.FileHandler('info.log')
   info_handler.setLevel(logging.INFO)
   ```

3. **Request Context Logging**
   ```python
   @app.before_request
   def log_request_info():
       app.logger.debug('Headers: %s', request.headers)
       app.logger.debug('Body: %s', request.get_data())
   ```

## Browser Developer Tools

### Network Tab
1. **Request Analysis**
   - Filter requests by type (XHR, JS, CSS, etc.)
   - Examine request/response headers
   - View timing information
   - Check payload data

2. **Network Conditions**
   - Simulate different network speeds
   - Test offline functionality
   - Disable cache for development

### Console Tab
1. **Error Monitoring**
   - JavaScript errors
   - Network request failures
   - Security warnings

2. **Network Request Debugging**
   ```javascript
   // Monitor all XHR requests
   const originalXHR = window.XMLHttpRequest;
   window.XMLHttpRequest = function () {
       const xhr = new originalXHR();
       xhr.addEventListener('load', function () {
           console.log('XHR Response:', this.responseText);
       });
       return xhr;
   };
   ```

### Elements Tab
1. **DOM Inspection**
   - View and modify HTML structure
   - Examine CSS styles
   - Check element properties
   - Monitor DOM events

2. **CSS Debugging**
   - Toggle CSS properties
   - Add new styles
   - Check computed styles
   - View CSS animations

### Application Tab
1. **Storage Inspection**
   - Local Storage
   - Session Storage
   - Cookies
   - Cache Storage
   - IndexedDB

2. **Service Worker Management**
   - Register/unregister service workers
   - Check service worker status
   - Clear service worker cache

### Performance Tab
1. **Performance Profiling**
   - Record page load
   - Analyze JavaScript execution
   - Check rendering performance
   - Memory usage monitoring

### Memory Tab
1. **Memory Management**
   - Take heap snapshots
   - Record allocation timelines
   - Find memory leaks
   - Compare snapshots

## Best Practices

1. **Structured Logging**
   - Use appropriate log levels
   - Include contextual information
   - Format logs consistently
   - Add timestamps

2. **Security Considerations**
   - Never log sensitive data
   - Remove debug logs in production
   - Sanitize user input in logs
   - Implement log rotation

3. **Performance Impact**
   - Use conditional logging
   - Avoid excessive logging
   - Implement log levels
   - Clean up old logs

4. **Debugging Workflow**
   1. Check browser console for JavaScript errors
   2. Examine network requests for API issues
   3. Review server logs for backend problems
   4. Use breakpoints for step-by-step debugging
   5. Profile performance if needed

## Common Debugging Scenarios

1. **API Integration Issues**
   ```javascript
   // Frontend logging
   fetch('/api/data')
       .then(response => {
           console.log('Response:', response);
           return response.json();
       })
       .catch(error => {
           console.error('API Error:', error);
       });
   
   # Backend logging
   @app.route('/api/data')
   def get_data():
       app.logger.info('API request received')
       try:
           # Process request
           app.logger.debug('Processing data')
       except Exception as e:
           app.logger.error('API error: %s', str(e))
           return jsonify({'error': str(e)}), 500
   ```

2. **Authentication Problems**
   ```javascript
   // Frontend
   console.log('Auth Token:', localStorage.getItem('token'));
   
   # Backend
   @app.before_request
   def log_auth():
       token = request.headers.get('Authorization')
       app.logger.debug('Auth token received: %s', token)
   ```

3. **Performance Issues**
   ```javascript
   // Frontend timing
   console.time('renderOperation');
   // ... rendering code
   console.timeEnd('renderOperation');
   
   # Backend timing
   import time
   
   start_time = time.time()
   # ... operation
   app.logger.debug('Operation took: %s seconds', time.time() - start_time)
   ```

## Troubleshooting Checklist

1. **Initial Investigation**
   - Check browser console for errors
   - Review network requests
   - Examine server logs
   - Verify environment variables

2. **Frontend Checks**
   - Console errors
   - Network requests
   - Local storage state
   - React/Vue devtools (if applicable)

3. **Backend Checks**
   - Application logs
   - Server status
   - Database connections
   - API endpoints

4. **Environment Checks**
   - Configuration files
   - Environment variables
   - Third-party services
   - Network connectivity
