# HTML Security Considerations and Best Practices

## Overview

This guide covers HTML security considerations, common vulnerabilities, and best practices for securing web applications. We'll explore how HTML structure and attributes can affect security, and how to implement proper controls.

## Common Web Vulnerabilities

### Cross-Site Scripting (XSS)

#### Vulnerable HTML
```html
<!-- DON'T: Directly inserting user input -->
<div>
    Welcome, <?php echo $_GET['username']; ?>!
</div>

<!-- DON'T: Unsafe innerHTML usage -->
<script>
document.getElementById('content').innerHTML = userProvidedContent;
</script>
```

#### Secure Implementation
```html
<!-- DO: Proper escaping -->
<div>
    Welcome, <?php echo htmlspecialchars($_GET['username'], ENT_QUOTES, 'UTF-8'); ?>!
</div>

<!-- DO: Safe content insertion -->
<script>
const textNode = document.createTextNode(userProvidedContent);
document.getElementById('content').appendChild(textNode);
</script>
```

### Content Security Policy (CSP)

```html
<!-- Strict CSP Header -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'nonce-randomNonce123'; 
               style-src 'self' 'nonce-randomNonce123';
               img-src 'self' https:;
               connect-src 'self';">

<!-- Implementation with Nonce -->
<script nonce="randomNonce123">
    // Your trusted JavaScript code
</script>
```

### Python Security Headers Generator
```python
from typing import Dict

def generate_security_headers() -> Dict[str, str]:
    return {
        'Content-Security-Policy': "default-src 'self'",
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=()'
    }

# Usage with Flask
from flask import Flask, make_response

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    headers = generate_security_headers()
    for header, value in headers.items():
        response.headers[header] = value
    return response
```

## Form Security

### Secure Form Implementation
```html
<!-- CSRF Protection -->
<form method="POST" action="/api/data">
    <input type="hidden" name="csrf_token" value="<?php echo generate_csrf_token(); ?>">
    
    <!-- Input Validation -->
    <input type="text" 
           pattern="[A-Za-z0-9]+" 
           maxlength="50"
           required
           autocomplete="off">
    
    <!-- File Upload Security -->
    <input type="file" 
           accept=".pdf,.doc,.docx"
           onchange="validateFileType(this)">
</form>

<script>
function validateFileType(input) {
    const allowedTypes = ['application/pdf', 'application/msword', 
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const file = input.files[0];
    
    if (!allowedTypes.includes(file.type)) {
        input.value = '';
        alert('Invalid file type');
    }
}
</script>
```

### Python CSRF Protection
```python
import secrets
from functools import wraps
from flask import session, abort, request

def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def csrf_protected(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = session.get('csrf_token')
            if not token or token != request.form.get('csrf_token'):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function
```

## Iframe Security

### Secure Iframe Implementation
```html
<!-- Restrict iframe permissions -->
<iframe src="https://trusted-domain.com/widget"
        sandbox="allow-scripts allow-same-origin"
        referrerpolicy="no-referrer"
        loading="lazy"
        allow="camera 'none'; microphone 'none'; geolocation 'none'">
</iframe>
```

### Python Frame Protection
```python
from flask import Flask, Response

app = Flask(__name__)

@app.after_request
def frame_protection(response):
    if isinstance(response, Response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
    return response
```

## Link Security

### Secure External Links
```html
<!-- Safe external links -->
<a href="https://external-site.com" 
   rel="noopener noreferrer" 
   target="_blank">
    External Link
</a>

<script>
// Validate URLs before navigation
function validateUrl(url) {
    const allowedDomains = ['trusted-domain.com', 'safe-site.com'];
    try {
        const urlObj = new URL(url);
        return allowedDomains.includes(urlObj.hostname);
    } catch {
        return false;
    }
}
</script>
```

## Resource Loading Security

### Subresource Integrity
```html
<!-- Secure CDN usage -->
<link rel="stylesheet" 
      href="https://cdn.example.com/css/styles.css"
      integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
      crossorigin="anonymous">

<script src="https://cdn.example.com/js/script.js"
        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
        crossorigin="anonymous"></script>
```

### Python SRI Generator
```python
import hashlib
import base64
import requests

def generate_sri_hash(url: str) -> str:
    response = requests.get(url)
    content = response.content
    hash_obj = hashlib.sha384(content)
    sri_hash = base64.b64encode(hash_obj.digest()).decode('utf-8')
    return f"sha384-{sri_hash}"
```

## Security Monitoring

### Content Security Policy Reporting
```html
<meta http-equiv="Content-Security-Policy-Report-Only"
      content="default-src 'self';
               report-uri /csp-violation-report">

<script>
// CSP Violation Reporter
document.addEventListener('securitypolicyviolation', (e) => {
    const violation = {
        blockedURI: e.blockedURI,
        violatedDirective: e.violatedDirective,
        originalPolicy: e.originalPolicy,
        timestamp: new Date().toISOString()
    };
    
    fetch('/csp-violation-report', {
        method: 'POST',
        body: JSON.stringify(violation)
    });
});
</script>
```

### Python CSP Violation Handler
```python
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(filename='csp_violations.log', level=logging.INFO)

@app.route('/csp-violation-report', methods=['POST'])
def csp_report():
    violation = request.get_json()
    logging.info(f"CSP Violation: {violation}")
    return jsonify({'status': 'received'})
```

## Security Testing Tools

### Python Security Scanner
```python
import requests
from typing import List, Dict
from urllib.parse import urljoin

class SecurityScanner:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.vulnerabilities = []

    def scan_security_headers(self) -> List[Dict]:
        response = requests.get(self.base_url)
        headers = response.headers
        
        required_headers = {
            'Content-Security-Policy': 'Missing CSP',
            'X-Frame-Options': 'Missing X-Frame-Options',
            'X-Content-Type-Options': 'Missing X-Content-Type-Options'
        }
        
        for header, message in required_headers.items():
            if header not in headers:
                self.vulnerabilities.append({
                    'type': 'missing_header',
                    'header': header,
                    'message': message
                })
        
        return self.vulnerabilities

    def scan_for_mixed_content(self) -> List[Dict]:
        response = requests.get(self.base_url)
        content = response.text
        
        if 'http://' in content and self.base_url.startswith('https://'):
            self.vulnerabilities.append({
                'type': 'mixed_content',
                'message': 'Mixed content detected'
            })
        
        return self.vulnerabilities

# Usage
scanner = SecurityScanner('https://example.com')
vulnerabilities = scanner.scan_security_headers()
vulnerabilities.extend(scanner.scan_for_mixed_content())
```

## Practical Exercises

1. **Security Headers Audit**
   - Implement security headers
   - Test with SecurityHeaders.com
   - Validate CSP implementation

2. **XSS Prevention**
   - Implement input sanitization
   - Set up CSP
   - Test with XSS payloads

3. **CSRF Protection**
   - Implement CSRF tokens
   - Test form submission
   - Validate token handling

## Security Checklist

1. **Input Validation**
   - [ ] Sanitize all user input
   - [ ] Validate file uploads
   - [ ] Implement proper encoding

2. **Output Encoding**
   - [ ] HTML encode dynamic content
   - [ ] URL encode parameters
   - [ ] Sanitize JSON output

3. **Security Headers**
   - [ ] Implement CSP
   - [ ] Set X-Frame-Options
   - [ ] Configure HSTS

4. **Resource Loading**
   - [ ] Use SRI for external resources
   - [ ] Implement proper CORS policies
   - [ ] Secure cookie attributes

## Additional Resources

1. [OWASP HTML Security Guide](https://owasp.org/www-project-web-security-testing-guide/)
2. [Content Security Policy Reference](https://content-security-policy.com/)
3. [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
4. [HTML5 Security Cheatsheet](https://html5sec.org/)
