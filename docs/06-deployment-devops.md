# Module 6: Deployment & DevOps

## Table of Contents
- [Module 6: Deployment & DevOps](#module-6:-deployment-&-devops)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Environment Configuration](#environment-configuration)
    - [Using Environment Variables](#using-environment-variables)
- [config.py](#configpy)
- [Example .env file](#example-env-file)
  - [Gunicorn Setup](#gunicorn-setup)
    - [Basic Configuration](#basic-configuration)
- [gunicorn.conf.py](#gunicornconfpy)
- [Start Gunicorn](#start-gunicorn)
    - [Systemd Service](#systemd-service)
- [/etc/systemd/system/flask-app.service](#/etc/systemd/system/flask-appservice)
  - [Docker Containerization](#docker-containerization)
    - [Dockerfile](#dockerfile)
    - [Docker Compose](#docker-compose)
  - [Nginx Configuration](#nginx-configuration)
    - [Basic Setup](#basic-setup)
- [/etc/nginx/sites-available/flask-app](#/etc/nginx/sites-available/flask-app)
    - [SSL Configuration](#ssl-configuration)
  - [CI/CD Pipeline](#ci/cd-pipeline)
    - [GitHub Actions](#github-actions)
  - [Monitoring & Logging](#monitoring-&-logging)
    - [Prometheus Metrics](#prometheus-metrics)
    - [ELK Stack Integration](#elk-stack-integration)
- [Usage](#usage)
  - [Backup Strategy](#backup-strategy)
    - [Database Backup](#database-backup)
  - [Exercise: Production Deployment](#exercise:-production-deployment)
- [!/bin/bash](#!/bin/bash)
- [deploy.sh](#deploysh)
- [Pull latest changes](#pull-latest-changes)
- [Update dependencies](#update-dependencies)
- [Run migrations](#run-migrations)
- [Restart services](#restart-services)
  - [Common Pitfalls](#common-pitfalls)
  - [Next Steps](#next-steps)
  - [Additional Resources](#additional-resources)



## Introduction

This module covers deploying Flask applications to production environments, focusing on best practices, server configuration, and monitoring. We'll explore how to move from a basic development setup to a production-ready deployment.

## Environment Configuration

### Using Environment Variables
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    REDIS_URL = os.getenv('REDIS_URL')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

# Example .env file
"""
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379/0
AWS_ACCESS_KEY=your-aws-key
AWS_SECRET_KEY=your-aws-secret
"""
```

## Gunicorn Setup

### Basic Configuration
```bash
# gunicorn.conf.py
workers = 4
bind = '0.0.0.0:8000'
worker_class = 'gevent'
keepalive = 60
timeout = 30
max_requests = 1000
max_requests_jitter = 50

# Start Gunicorn
gunicorn --config gunicorn.conf.py wsgi:app
```

### Systemd Service
```ini
# /etc/systemd/system/flask-app.service
[Unit]
Description=Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/flask-app
Environment="PATH=/var/www/flask-app/venv/bin"
ExecStart=/var/www/flask-app/venv/bin/gunicorn --config gunicorn.conf.py wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## Docker Containerization

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
  
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
    volumes:
      - db_data:/var/lib/mysql
  
  redis:
    image: redis:6
    volumes:
      - redis_data:/data

volumes:
  db_data:
  redis_data:
```

## Nginx Configuration

### Basic Setup
```nginx
# /etc/nginx/sites-available/flask-app
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/flask-app/static;
        expires 30d;
    }

    location /media {
        alias /var/www/flask-app/media;
        expires 30d;
    }
}
```

### SSL Configuration
```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # ... rest of configuration
}
```

## CI/CD Pipeline

### GitHub Actions
```yaml
name: Flask CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /var/www/flask-app
          git pull
          source venv/bin/activate
          pip install -r requirements.txt
          flask db upgrade
          sudo systemctl restart flask-app
```

## Monitoring & Logging

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram
from flask import request

REQUEST_COUNT = Counter(
    'flask_request_count',
    'App Request Count',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'Request latency',
    ['endpoint']
)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint,
        http_status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(
        endpoint=request.endpoint
    ).observe(request_latency)
    return response
```

### ELK Stack Integration
```python
import logging
from elasticsearch import Elasticsearch
from elasticsearch.handlers import ElasticsearchHandler

es = Elasticsearch(['http://elasticsearch:9200'])

handler = ElasticsearchHandler(
    es,
    'flask-logs',
    flush_frequency=1,
    es_additional_fields={'application': 'flask-app'}
)

logger = logging.getLogger('flask-app')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Usage
@app.route('/api/action')
def some_action():
    try:
        result = perform_action()
        logger.info('Action performed', extra={
            'action': 'some_action',
            'result': result
        })
        return jsonify(result)
    except Exception as e:
        logger.error('Action failed', extra={
            'action': 'some_action',
            'error': str(e)
        })
        return 'Error occurred', 500
```

## Backup Strategy

### Database Backup
```python
import subprocess
from datetime import datetime
import boto3

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_{timestamp}.sql'
    
    # Create backup
    subprocess.run([
        'mysqldump',
        '-u', os.getenv('DB_USER'),
        '-p' + os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME'),
        '>', backup_file
    ])
    
    # Upload to S3
    s3 = boto3.client('s3')
    s3.upload_file(
        backup_file,
        'backup-bucket',
        f'database/{backup_file}'
    )
```

## Exercise: Production Deployment

1. Set up a basic Flask application with the following structure:
```
flask-app/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── templates/
├── config.py
├── requirements.txt
├── wsgi.py
├── Dockerfile
└── docker-compose.yml
```

2. Create deployment scripts:
```bash
#!/bin/bash
# deploy.sh

# Pull latest changes
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
flask db upgrade

# Restart services
sudo systemctl restart flask-app
sudo systemctl restart nginx
```

## Common Pitfalls

1. **Security**
   - Expose sensitive configuration
   - Insufficient logging
   - Missing error handling
   - Insecure file permissions

2. **Performance**
   - Insufficient workers
   - Missing caching
   - Unoptimized database queries
   - Large static files

3. **Maintenance**
   - No backup strategy
   - Missing monitoring
   - Poor logging practices
   - Difficult rollback process

4. **Scaling**
   - Single point of failure
   - No load balancing
   - Resource constraints
   - Session management issues

## Next Steps

1. Complete the deployment exercise
2. Set up monitoring and logging
3. Implement backup strategy
4. Configure CI/CD pipeline
5. Review security best practices

## Additional Resources

- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
