# Chapter 4: Deployment and DevOps

## Introduction

Think about opening a restaurant - you need to set up the kitchen, train staff, manage inventory, and handle daily operations. Similarly, deploying software requires setting up servers, configuring environments, monitoring performance, and maintaining systems. In this chapter, we'll learn how to deploy and maintain applications in production.

## 1. Deployment Basics

### The Restaurant Opening Metaphor

Think of deployment like opening a restaurant:
- Environment setup like kitchen setup
- Configuration like recipes and procedures
- Dependencies like ingredients and equipment
- Deployment like opening day
- Monitoring like customer feedback

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:pass@localhost/db
export SECRET_KEY=your-secret-key

# Initialize database
flask db upgrade

# Run application
gunicorn app:app
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db/app
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Hands-On Exercise: Deployment Script

Create deployment automation:
```python
# deploy.py
import os
import subprocess
import paramiko
import yaml
from typing import Dict, List
import logging

class Deployer:
    """Handles application deployment."""
    
    def __init__(self, config_path: str):
        """Initialize deployer with config."""
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
    
    def _load_config(self, path: str) -> Dict:
        """Load deployment configuration."""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def _setup_logging(self) -> logging.Logger:
        """Configure logging."""
        logger = logging.getLogger('deployer')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )
        logger.addHandler(handler)
        
        return logger
    
    def _check_dependencies(self) -> List[str]:
        """Check local dependencies."""
        missing = []
        for dep in self.config['dependencies']:
            try:
                subprocess.run(
                    [dep, '--version'],
                    capture_output=True,
                    check=True
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing.append(dep)
        return missing
    
    def _build_docker_image(self) -> str:
        """Build Docker image."""
        tag = f"{self.config['image']}:{self.config['version']}"
        
        self.logger.info(f"Building Docker image: {tag}")
        
        subprocess.run(
            ['docker', 'build', '-t', tag, '.'],
            check=True
        )
        
        return tag
    
    def _push_docker_image(self, tag: str) -> None:
        """Push Docker image to registry."""
        self.logger.info(f"Pushing image: {tag}")
        
        subprocess.run(
            ['docker', 'push', tag],
            check=True
        )
    
    def _connect_to_server(self) -> paramiko.SSHClient:
        """Connect to deployment server."""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )
        
        self.logger.info(
            f"Connecting to {self.config['server']['host']}"
        )
        
        client.connect(
            hostname=self.config['server']['host'],
            username=self.config['server']['user'],
            key_filename=self.config['server']['key_path']
        )
        
        return client
    
    def _run_remote_command(
        self,
        client: paramiko.SSHClient,
        command: str
    ) -> None:
        """Run command on remote server."""
        self.logger.info(f"Running: {command}")
        
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status != 0:
            error = stderr.read().decode()
            raise Exception(f"Command failed: {error}")
        
        return stdout.read().decode()
    
    def _update_application(
        self,
        client: paramiko.SSHClient,
        tag: str
    ) -> None:
        """Update application on server."""
        commands = [
            f"docker pull {tag}",
            "docker-compose down",
            f"export IMAGE_TAG={tag}",
            "docker-compose up -d"
        ]
        
        for cmd in commands:
            self._run_remote_command(client, cmd)
    
    def _run_health_check(
        self,
        client: paramiko.SSHClient
    ) -> bool:
        """Check if application is healthy."""
        try:
            response = self._run_remote_command(
                client,
                f"curl -f http://localhost:{self.config['port']}/health"
            )
            return response.strip() == '{"status":"healthy"}'
        except:
            return False
    
    def deploy(self) -> None:
        """Run deployment process."""
        try:
            # Check dependencies
            missing = self._check_dependencies()
            if missing:
                raise Exception(
                    f"Missing dependencies: {', '.join(missing)}"
                )
            
            # Build and push image
            tag = self._build_docker_image()
            self._push_docker_image(tag)
            
            # Connect to server
            client = self._connect_to_server()
            
            try:
                # Update application
                self._update_application(client, tag)
                
                # Health check
                if not self._run_health_check(client):
                    raise Exception("Health check failed")
                
                self.logger.info("Deployment successful!")
                
            finally:
                client.close()
                
        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            raise

# Example usage
if __name__ == '__main__':
    deployer = Deployer('deploy-config.yml')
    deployer.deploy()
```

```yaml
# deploy-config.yml
# Deployment configuration
version: '1.0.0'
image: 'myapp'
port: 5000

# Dependencies
dependencies:
  - docker
  - docker-compose
  - curl

# Server configuration
server:
  host: 'production.example.com'
  user: 'deploy'
  key_path: '~/.ssh/deploy_key'

# Application settings
env:
  FLASK_ENV: 'production'
  DATABASE_URL: 'postgresql://user:pass@db/app'
  
# Monitoring
health_check:
  endpoint: '/health'
  interval: 30
  timeout: 5
```

## 2. Monitoring and Logging

### The Health Monitoring Metaphor

Think of monitoring like health monitoring:
- Metrics like vital signs
- Logs like medical records
- Alerts like emergency notifications
- Dashboards like health charts
- Debugging like diagnosis

### Setting Up Monitoring

```python
# monitoring.py
from flask import Flask
from prometheus_client import Counter, Histogram
import time
import logging
from logging.handlers import RotatingFileHandler
import structlog

# Initialize Flask app
app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'request_count',
    'Number of requests received',
    ['endpoint']
)

REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

# Structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Request timing middleware
@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    # Update metrics
    REQUEST_COUNT.labels(
        endpoint=request.endpoint
    ).inc()
    
    REQUEST_LATENCY.labels(
        endpoint=request.endpoint
    ).observe(time.time() - request.start_time)
    
    # Log request
    logger.info(
        "request_processed",
        path=request.path,
        method=request.method,
        status=response.status_code,
        duration=time.time() - request.start_time,
        ip=request.remote_addr
    )
    
    return response

# Error logging
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(
        "unhandled_error",
        error=str(error),
        exc_info=True
    )
    return "Internal Server Error", 500

# Health check endpoint
@app.route('/health')
def health():
    return {'status': 'healthy'}
```

### Log Management

```python
# logging_config.py
import logging
import logging.config
import yaml

def setup_logging(
    default_path='logging.yml',
    default_level=logging.INFO,
    env_key='LOG_CONFIG'
):
    """Setup logging configuration."""
    path = default_path
    
    try:
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    except Exception as e:
        print(f'Error in logging config: {e}')
        logging.basicConfig(level=default_level)

```

```yaml
# logging.yml
version: 1
disable_existing_loggers: false

formatters:
  standard:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  json:
    class: pythonjsonlogger.jsonlogger.JsonFormatter
    format: '%(timestamp)s %(level)s %(name)s %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout

  file:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: json
    filename: app.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    encoding: utf8

  error_file:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: json
    filename: error.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    encoding: utf8

loggers:
  app:
    level: INFO
    handlers: [console, file, error_file]
    propagate: no

root:
  level: INFO
  handlers: [console]
```

### Hands-On Exercise: Monitoring System

Create monitoring dashboard:
```python
# monitoring_system.py
import psutil
import time
import json
from datetime import datetime
from typing import Dict, List
import threading
import queue
import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Metric:
    """Represents a system metric."""
    name: str
    value: float
    timestamp: float
    labels: Dict[str, str]

class MetricCollector(ABC):
    """Base class for metric collectors."""
    
    @abstractmethod
    def collect(self) -> List[Metric]:
        """Collect metrics."""
        pass

class SystemMetrics(MetricCollector):
    """Collects system metrics."""
    
    def collect(self) -> List[Metric]:
        now = time.time()
        metrics = []
        
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics.append(Metric(
            name='system_cpu_usage',
            value=cpu_percent,
            timestamp=now,
            labels={'unit': 'percent'}
        ))
        
        # Memory metrics
        memory = psutil.virtual_memory()
        metrics.append(Metric(
            name='system_memory_usage',
            value=memory.percent,
            timestamp=now,
            labels={'unit': 'percent'}
        ))
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        metrics.append(Metric(
            name='system_disk_usage',
            value=disk.percent,
            timestamp=now,
            labels={'unit': 'percent'}
        ))
        
        return metrics

class ProcessMetrics(MetricCollector):
    """Collects process metrics."""
    
    def __init__(self, pid: int):
        self.process = psutil.Process(pid)
    
    def collect(self) -> List[Metric]:
        now = time.time()
        metrics = []
        
        # Process CPU
        cpu_percent = self.process.cpu_percent()
        metrics.append(Metric(
            name='process_cpu_usage',
            value=cpu_percent,
            timestamp=now,
            labels={'unit': 'percent'}
        ))
        
        # Process memory
        memory_info = self.process.memory_info()
        metrics.append(Metric(
            name='process_memory_usage',
            value=memory_info.rss / 1024 / 1024,  # MB
            timestamp=now,
            labels={'unit': 'megabytes'}
        ))
        
        return metrics

class MetricStorage:
    """Stores metrics in memory with retention."""
    
    def __init__(self, retention_hours: int = 24):
        self.retention_seconds = retention_hours * 3600
        self.metrics: Dict[str, List[Metric]] = {}
    
    def store(self, metric: Metric) -> None:
        """Store a metric."""
        if metric.name not in self.metrics:
            self.metrics[metric.name] = []
        
        self.metrics[metric.name].append(metric)
        self._cleanup()
    
    def _cleanup(self) -> None:
        """Remove old metrics."""
        now = time.time()
        for name in self.metrics:
            self.metrics[name] = [
                m for m in self.metrics[name]
                if now - m.timestamp < self.retention_seconds
            ]
    
    def get_metrics(
        self,
        name: str,
        start_time: float = None,
        end_time: float = None
    ) -> List[Metric]:
        """Get metrics for a given time range."""
        if name not in self.metrics:
            return []
        
        metrics = self.metrics[name]
        
        if start_time:
            metrics = [m for m in metrics if m.timestamp >= start_time]
        
        if end_time:
            metrics = [m for m in metrics if m.timestamp <= end_time]
        
        return metrics

class MetricCollectorThread(threading.Thread):
    """Thread that collects metrics periodically."""
    
    def __init__(
        self,
        collector: MetricCollector,
        interval: int,
        storage: MetricStorage
    ):
        super().__init__()
        self.collector = collector
        self.interval = interval
        self.storage = storage
        self.stop_event = threading.Event()
    
    def run(self) -> None:
        """Run metric collection."""
        while not self.stop_event.is_set():
            try:
                metrics = self.collector.collect()
                for metric in metrics:
                    self.storage.store(metric)
            except Exception as e:
                logging.error(f"Error collecting metrics: {e}")
            
            time.sleep(self.interval)
    
    def stop(self) -> None:
        """Stop metric collection."""
        self.stop_event.set()

class AlertRule:
    """Defines an alert rule."""
    
    def __init__(
        self,
        metric_name: str,
        threshold: float,
        window_seconds: int = 300,
        condition: str = '>',
        description: str = ''
    ):
        self.metric_name = metric_name
        self.threshold = threshold
        self.window_seconds = window_seconds
        self.condition = condition
        self.description = description
    
    def check(
        self,
        storage: MetricStorage
    ) -> bool:
        """Check if alert should be triggered."""
        now = time.time()
        start_time = now - self.window_seconds
        
        metrics = storage.get_metrics(
            self.metric_name,
            start_time,
            now
        )
        
        if not metrics:
            return False
        
        values = [m.value for m in metrics]
        avg_value = sum(values) / len(values)
        
        if self.condition == '>':
            return avg_value > self.threshold
        elif self.condition == '<':
            return avg_value < self.threshold
        elif self.condition == '>=':
            return avg_value >= self.threshold
        elif self.condition == '<=':
            return avg_value <= self.threshold
        else:
            return False

class AlertManager:
    """Manages alerts."""
    
    def __init__(self):
        self.rules: List[AlertRule] = []
        self.alerts: List[Dict] = []
    
    def add_rule(self, rule: AlertRule) -> None:
        """Add an alert rule."""
        self.rules.append(rule)
    
    def check_rules(self, storage: MetricStorage) -> None:
        """Check all rules and generate alerts."""
        for rule in self.rules:
            if rule.check(storage):
                self.alerts.append({
                    'rule': rule.metric_name,
                    'description': rule.description,
                    'timestamp': datetime.now().isoformat()
                })
    
    def get_alerts(
        self,
        start_time: str = None
    ) -> List[Dict]:
        """Get alerts after start_time."""
        if not start_time:
            return self.alerts
        
        return [
            alert for alert in self.alerts
            if alert['timestamp'] >= start_time
        ]

class MonitoringSystem:
    """Main monitoring system."""
    
    def __init__(self):
        self.storage = MetricStorage()
        self.alert_manager = AlertManager()
        self.collectors: List[MetricCollectorThread] = []
    
    def add_collector(
        self,
        collector: MetricCollector,
        interval: int
    ) -> None:
        """Add a metric collector."""
        thread = MetricCollectorThread(
            collector,
            interval,
            self.storage
        )
        self.collectors.append(thread)
    
    def add_alert_rule(self, rule: AlertRule) -> None:
        """Add an alert rule."""
        self.alert_manager.add_rule(rule)
    
    def start(self) -> None:
        """Start monitoring."""
        for collector in self.collectors:
            collector.start()
    
    def stop(self) -> None:
        """Stop monitoring."""
        for collector in self.collectors:
            collector.stop()
            collector.join()
    
    def get_metrics(
        self,
        name: str,
        start_time: float = None,
        end_time: float = None
    ) -> List[Dict]:
        """Get metrics as dictionary."""
        metrics = self.storage.get_metrics(
            name,
            start_time,
            end_time
        )
        
        return [
            {
                'name': m.name,
                'value': m.value,
                'timestamp': m.timestamp,
                'labels': m.labels
            }
            for m in metrics
        ]
    
    def get_alerts(self, start_time: str = None) -> List[Dict]:
        """Get alerts."""
        return self.alert_manager.get_alerts(start_time)

# Example usage
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create monitoring system
    monitor = MonitoringSystem()
    
    # Add collectors
    monitor.add_collector(SystemMetrics(), 60)  # Every minute
    monitor.add_collector(ProcessMetrics(os.getpid()), 60)
    
    # Add alert rules
    monitor.add_alert_rule(AlertRule(
        'system_cpu_usage',
        threshold=90,
        description='High CPU usage'
    ))
    
    monitor.add_alert_rule(AlertRule(
        'system_memory_usage',
        threshold=90,
        description='High memory usage'
    ))
    
    # Start monitoring
    try:
        monitor.start()
        
        # Keep running
        while True:
            # Check alerts
            monitor.alert_manager.check_rules(monitor.storage)
            
            # Print current metrics
            metrics = monitor.get_metrics('system_cpu_usage')
            if metrics:
                print(f"CPU Usage: {metrics[-1]['value']}%")
            
            # Print alerts
            alerts = monitor.get_alerts()
            if alerts:
                print("Alerts:", json.dumps(alerts, indent=2))
            
            time.sleep(60)
            
    except KeyboardInterrupt:
        monitor.stop()
```

## 3. Maintenance

### The Car Maintenance Metaphor

Think of maintenance like car maintenance:
- Updates like oil changes
- Backups like spare parts
- Security like safety features
- Performance like tuning
- Documentation like service manual

### System Updates

```python
# update_system.py
import subprocess
import logging
from typing import List, Dict
import yaml
import os
from datetime import datetime

class SystemUpdater:
    """Handles system updates."""
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger('updater')
    
    def _load_config(self, path: str) -> Dict:
        """Load update configuration."""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def _backup_database(self) -> str:
        """Create database backup."""
        backup_dir = self.config['backup_dir']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{backup_dir}/db_backup_{timestamp}.sql"
        
        self.logger.info(f"Creating backup: {backup_file}")
        
        subprocess.run([
            'pg_dump',
            '-h', self.config['db_host'],
            '-U', self.config['db_user'],
            '-d', self.config['db_name'],
            '-f', backup_file
        ], check=True)
        
        return backup_file
    
    def _update_dependencies(self) -> None:
        """Update project dependencies."""
        self.logger.info("Updating dependencies")
        
        subprocess.run([
            'pip', 'install', '-r',
            'requirements.txt', '--upgrade'
        ], check=True)
    
    def _run_migrations(self) -> None:
        """Run database migrations."""
        self.logger.info("Running migrations")
        
        subprocess.run([
            'flask', 'db', 'upgrade'
        ], check=True)
    
    def _update_application(self) -> None:
        """Update application code."""
        self.logger.info("Updating application")
        
        # Pull latest code
        subprocess.run([
            'git', 'pull', 'origin', 'main'
        ], check=True)
        
        # Install dependencies
        self._update_dependencies()
        
        # Run migrations
        self._run_migrations()
        
        # Restart application
        subprocess.run([
            'supervisorctl', 'restart', 'app'
        ], check=True)
    
    def _verify_update(self) -> bool:
        """Verify update was successful."""
        self.logger.info("Verifying update")
        
        try:
            # Check application status
            response = subprocess.run([
                'curl', '-f',
                f"http://localhost:{self.config['port']}/health"
            ], capture_output=True, check=True)
            
            return response.stdout.decode().strip() == '{"status":"healthy"}'
            
        except subprocess.CalledProcessError:
            return False
    
    def _cleanup_old_backups(self) -> None:
        """Remove old backups."""
        backup_dir = self.config['backup_dir']
        max_backups = self.config['max_backups']
        
        backups = sorted([
            f for f in os.listdir(backup_dir)
            if f.startswith('db_backup_')
        ])
        
        if len(backups) > max_backups:
            for backup in backups[:-max_backups]:
                os.remove(os.path.join(backup_dir, backup))
    
    def update(self) -> bool:
        """Run system update."""
        try:
            # Create backup
            backup_file = self._backup_database()
            
            # Update application
            self._update_application()
            
            # Verify update
            if not self._verify_update():
                self.logger.error("Update verification failed")
                return False
            
            # Cleanup old backups
            self._cleanup_old_backups()
            
            self.logger.info("Update completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Update failed: {str(e)}")
            return False

# Example usage
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run update
    updater = SystemUpdater('update-config.yml')
    success = updater.update()
    
    if not success:
        exit(1)
```

```yaml
# update-config.yml
# Database settings
db_host: localhost
db_user: app_user
db_name: app_db

# Backup settings
backup_dir: /var/backups/app
max_backups: 5

# Application settings
port: 5000
```

### Hands-On Exercise: Maintenance Scripts

Create maintenance toolkit:
```python
# maintenance_toolkit.py
import os
import sys
import logging
import argparse
import subprocess
from typing import List, Dict
import psutil
import json
from datetime import datetime, timedelta

class MaintenanceToolkit:
    """System maintenance toolkit."""
    
    def __init__(self):
        self.logger = logging.getLogger('maintenance')
    
    def check_disk_space(self) -> Dict[str, float]:
        """Check disk space usage."""
        usage = {}
        for partition in psutil.disk_partitions():
            try:
                usage[partition.mountpoint] = psutil.disk_usage(
                    partition.mountpoint
                ).percent
            except:
                continue
        return usage
    
    def check_log_sizes(self, log_dir: str) -> Dict[str, int]:
        """Check log file sizes."""
        sizes = {}
        for file in os.listdir(log_dir):
            if file.endswith('.log'):
                path = os.path.join(log_dir, file)
                sizes[file] = os.path.getsize(path)
        return sizes
    
    def rotate_logs(self, log_dir: str) -> None:
        """Rotate log files."""
        for file in os.listdir(log_dir):
            if file.endswith('.log'):
                path = os.path.join(log_dir, file)
                if os.path.getsize(path) > 10 * 1024 * 1024:  # 10MB
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    new_path = f"{path}.{timestamp}"
                    os.rename(path, new_path)
    
    def cleanup_old_files(
        self,
        directory: str,
        days: int
    ) -> None:
        """Remove files older than specified days."""
        cutoff = datetime.now() - timedelta(days=days)
        
        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                if datetime.fromtimestamp(
                    os.path.getmtime(path)
                ) < cutoff:
                    os.remove(path)
    
    def check_service_status(
        self,
        services: List[str]
    ) -> Dict[str, bool]:
        """Check if services are running."""
        status = {}
        for service in services:
            try:
                subprocess.run(
                    ['systemctl', 'is-active', service],
                    check=True,
                    capture_output=True
                )
                status[service] = True
            except subprocess.CalledProcessError:
                status[service] = False
        return status
    
    def backup_database(
        self,
        host: str,
        user: str,
        database: str,
        backup_dir: str
    ) -> str:
        """Create database backup."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{backup_dir}/backup_{timestamp}.sql"
        
        subprocess.run([
            'pg_dump',
            '-h', host,
            '-U', user,
            '-d', database,
            '-f', backup_file
        ], check=True)
        
        return backup_file
    
    def verify_backups(
        self,
        backup_dir: str
    ) -> Dict[str, Dict]:
        """Verify backup files."""
        results = {}
        
        for file in os.listdir(backup_dir):
            if file.endswith('.sql'):
                path = os.path.join(backup_dir, file)
                size = os.path.getsize(path)
                mtime = datetime.fromtimestamp(
                    os.path.getmtime(path)
                )
                
                results[file] = {
                    'size': size,
                    'modified': mtime.isoformat(),
                    'valid': self._verify_backup(path)
                }
        
        return results
    
    def _verify_backup(self, path: str) -> bool:
        """Verify backup file integrity."""
        try:
            # Try to read backup file
            subprocess.run(
                ['pg_restore', '--list', path],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def check_ssl_certificates(
        self,
        domains: List[str]
    ) -> Dict[str, Dict]:
        """Check SSL certificate expiration."""
        results = {}
        
        for domain in domains:
            try:
                output = subprocess.run([
                    'openssl', 's_client', '-connect',
                    f"{domain}:443", '-servername',
                    domain
                ], capture_output=True, text=True, input='')
                
                cert_info = subprocess.run([
                    'openssl', 'x509', '-noout',
                    '-enddate', '-subject'
                ], capture_output=True, text=True,
                input=output.stdout)
                
                # Parse output
                end_date = None
                subject = None
                for line in cert_info.stdout.splitlines():
                    if line.startswith('notAfter='):
                        end_date = line.split('=')[1]
                    elif line.startswith('subject='):
                        subject = line.split('=')[1]
                
                results[domain] = {
                    'valid': True,
                    'expires': end_date,
                    'subject': subject
                }
                
            except subprocess.CalledProcessError:
                results[domain] = {
                    'valid': False,
                    'error': 'Failed to check certificate'
                }
        
        return results
    
    def run_security_updates(self) -> bool:
        """Run system security updates."""
        try:
            # Update package list
            subprocess.run(
                ['apt-get', 'update'],
                check=True
            )
            
            # Install security updates
            subprocess.run([
                'apt-get', 'upgrade',
                '-s', 'security'
            ], check=True)
            
            return True
            
        except subprocess.CalledProcessError:
            return False

# Example usage
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create toolkit
    toolkit = MaintenanceToolkit()
    
    # Check disk space
    disk_usage = toolkit.check_disk_space()
    print("Disk Usage:", json.dumps(disk_usage, indent=2))
    
    # Check log sizes
    log_sizes = toolkit.check_log_sizes('/var/log')
    print("Log Sizes:", json.dumps(log_sizes, indent=2))
    
    # Check services
    services = ['nginx', 'postgresql', 'redis']
    service_status = toolkit.check_service_status(services)
    print("Service Status:", json.dumps(service_status, indent=2))
    
    # Check SSL certificates
    domains = ['example.com', 'api.example.com']
    ssl_status = toolkit.check_ssl_certificates(domains)
    print("SSL Status:", json.dumps(ssl_status, indent=2))
```

## Practical Exercises

### 1. Deployment Pipeline
Build pipeline for:
1. Code deployment
2. Database migrations
3. Configuration management
4. Health checks
5. Rollback procedures

### 2. Monitoring Setup
Create monitoring for:
1. System metrics
2. Application logs
3. Error tracking
4. Performance metrics
5. Alert system

### 3. Maintenance Scripts
Implement scripts for:
1. Backup automation
2. Log rotation
3. Security updates
4. SSL renewal
5. Disk cleanup

## Review Questions

1. **Deployment**
   - How automate deployment?
   - When use containers?
   - Best practices for configuration?

2. **Monitoring**
   - How track metrics?
   - When set alerts?
   - Best practices for logging?

3. **Maintenance**
   - How handle updates?
   - When perform backups?
   - Best practices for security?

## Additional Resources

### Online Tools
- Deployment platforms
- Monitoring services
- Maintenance tools

### Further Reading
- DevOps practices
- System administration
- Cloud platforms

### Video Resources
- Deployment tutorials
- Monitoring guides
- Maintenance tips

## Next Steps

After mastering these concepts, you'll be ready to:
1. Deploy applications
2. Monitor systems
3. Maintain infrastructure

Remember: Good DevOps practices make operations smoother!

## Common Questions and Answers

Q: How often should I deploy?
A: Deploy as often as needed while maintaining stability.

Q: What metrics should I monitor?
A: Monitor system resources, application performance, and user experience.

Q: How often should I backup?
A: Regular backups based on data importance and change frequency.

## Glossary

- **Deployment**: Code release
- **Container**: Isolated environment
- **Monitoring**: System tracking
- **Logging**: Event recording
- **Metrics**: Performance measures
- **Alert**: Issue notification
- **Backup**: Data copy
- **Security**: Protection measures
- **Update**: System maintenance
- **DevOps**: Development operations

Remember: DevOps is about continuous improvement and automation!
