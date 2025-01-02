# Automation Scripts

## Table of Contents
- [Automation Scripts](#automation-scripts)
  - [Table of Contents](#table-of-contents)
          - [tags: automation, scheduling, deployment, maintenance, testing](#tags:-automation,-scheduling,-deployment,-maintenance,-testing)
  - [Task Scheduler](#task-scheduler)
          - [tags: scheduler, cron, tasks](#tags:-scheduler,-cron,-tasks)
- [Task Scheduler](#task-scheduler)
- [!/bin/bash](#!/bin/bash)
- [Task format in tasks.conf:](#task-format-in-tasksconf:)
- [[time] [command] [description]](#[time]-[command]-[description])
- [Example: "0 4 * * * /scripts/backup.sh Daily backup"](#example:-"0-4-*-*-*-/scripts/backupsh-daily-backup")
- [Task management functions](#task-management-functions)
  - [Process Automation](#process-automation)
          - [tags: process, automation, management](#tags:-process,-automation,-management)
- [Process Automation Manager](#process-automation-manager)
- [!/bin/bash](#!/bin/bash)
  - [System Maintenance](#system-maintenance)
          - [tags: maintenance, cleanup, updates](#tags:-maintenance,-cleanup,-updates)
- [System Maintenance Manager](#system-maintenance-manager)
- [!/bin/bash](#!/bin/bash)
- [Disk cleanup](#disk-cleanup)
- [Service maintenance](#service-maintenance)
  - [Deployment Automation](#deployment-automation)
          - [tags: deployment, automation, release](#tags:-deployment,-automation,-release)
- [Deployment Manager](#deployment-manager)
- [!/bin/bash](#!/bin/bash)
- [Rollback deployment](#rollback-deployment)
  - [Configuration Management](#configuration-management)
          - [tags: configuration, management, templates](#tags:-configuration,-management,-templates)
- [Configuration Manager](#configuration-manager)
- [!/bin/bash](#!/bin/bash)
  - [Automated Testing](#automated-testing)
          - [tags: testing, automation, quality](#tags:-testing,-automation,-quality)
- [Test Automation Manager](#test-automation-manager)
- [!/bin/bash](#!/bin/bash)
  - [Continuous Integration](#continuous-integration)
          - [tags: ci, automation, pipeline](#tags:-ci,-automation,-pipeline)
- [CI Pipeline Manager](#ci-pipeline-manager)
- [!/bin/bash](#!/bin/bash)
  - [See Also](#see-also)



###### tags: `automation`, `scheduling`, `deployment`, `maintenance`, `testing`

## Task Scheduler
###### tags: `scheduler`, `cron`, `tasks`

```bash
# Task Scheduler
#!/bin/bash
tasks_file="/etc/automation/tasks.conf"
log_file="/var/log/automation/scheduler.log"

# Task format in tasks.conf:
# [time] [command] [description]
# Example: "0 4 * * * /scripts/backup.sh Daily backup"

run_scheduled_tasks() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Loading scheduled tasks..." >> "$log_file"
    
    while IFS= read -r line; do
        [[ "$line" =~ ^#.*$ ]] && continue  # Skip comments
        
        schedule=$(echo "$line" | cut -d' ' -f1-5)
        command=$(echo "$line" | cut -d' ' -f6)
        description=$(echo "$line" | cut -d' ' -f7-)
        
        # Create cron job
        (crontab -l 2>/dev/null; echo "$schedule $command # $description") | crontab -
        
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Added task: $description" >> "$log_file"
    done < "$tasks_file"
}

# Task management functions
add_task() {
    local schedule="$1"
    local command="$2"
    local description="$3"
    
    echo "$schedule $command $description" >> "$tasks_file"
    run_scheduled_tasks
}

remove_task() {
    local command="$1"
    sed -i "\|$command|d" "$tasks_file"
    run_scheduled_tasks
}

list_tasks() {
    echo "=== Scheduled Tasks ===" >> "$log_file"
    crontab -l | grep -v '^#' >> "$log_file"
}
```

## Process Automation
###### tags: `process`, `automation`, `management`

```bash
# Process Automation Manager
#!/bin/bash
processes_file="/etc/automation/processes.conf"
pid_dir="/var/run/automation"
log_file="/var/log/automation/processes.log"

start_process() {
    local name="$1"
    local command="$2"
    local restart="$3"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting process: $name" >> "$log_file"
    
    # Start process
    $command &
    local pid=$!
    echo $pid > "$pid_dir/$name.pid"
    
    # Monitor and restart if needed
    if [ "$restart" = "true" ]; then
        while true; do
            if ! kill -0 $pid 2>/dev/null; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Process $name died, restarting..." >> "$log_file"
                $command &
                pid=$!
                echo $pid > "$pid_dir/$name.pid"
            fi
            sleep 60
        done &
    fi
}

stop_process() {
    local name="$1"
    local pid_file="$pid_dir/$name.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        kill $pid
        rm "$pid_file"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stopped process: $name" >> "$log_file"
    fi
}

check_process() {
    local name="$1"
    local pid_file="$pid_dir/$name.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 $pid 2>/dev/null; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Process $name is running (PID: $pid)" >> "$log_file"
            return 0
        fi
    fi
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Process $name is not running" >> "$log_file"
    return 1
}
```

## System Maintenance
###### tags: `maintenance`, `cleanup`, `updates`

```bash
# System Maintenance Manager
#!/bin/bash
maintenance_config="/etc/automation/maintenance.conf"
report_file="/var/log/automation/maintenance.log"

perform_maintenance() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting system maintenance..." >> "$report_file"
    
    # Clean old logs
    echo "Cleaning old logs..." >> "$report_file"
    find /var/log -type f -name "*.log" -mtime +30 -delete
    
    # Clean package cache
    echo "Cleaning package cache..." >> "$report_file"
    if command -v apt-get &>/dev/null; then
        apt-get clean
        apt-get autoremove -y
    elif command -v yum &>/dev/null; then
        yum clean all
    fi
    
    # Clean temp files
    echo "Cleaning temporary files..." >> "$report_file"
    find /tmp -type f -atime +7 -delete
    
    # Update system
    echo "Updating system packages..." >> "$report_file"
    if command -v apt-get &>/dev/null; then
        apt-get update && apt-get upgrade -y
    elif command -v yum &>/dev/null; then
        yum update -y
    fi
    
    # Check disk space
    echo "Checking disk space..." >> "$report_file"
    df -h >> "$report_file"
    
    # Check system health
    echo "Checking system health..." >> "$report_file"
    echo "Uptime: $(uptime)" >> "$report_file"
    echo "Memory usage: $(free -h)" >> "$report_file"
    
    # Send report
    mail -s "System Maintenance Report" admin@example.com < "$report_file"
}

# Disk cleanup
cleanup_disk() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting disk cleanup..." >> "$report_file"
    
    # Find and remove large files
    find / -type f -size +100M -exec ls -lh {} \; >> "$report_file"
    
    # Remove old backups
    find /backup -type f -mtime +30 -delete
    
    # Clean user caches
    find /home -type f -name ".cache" -exec rm -rf {} \;
}

# Service maintenance
maintain_services() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Maintaining services..." >> "$report_file"
    
    # Restart services if needed
    for service in nginx mysql redis-server; do
        systemctl is-active --quiet $service || systemctl restart $service
    done
    
    # Check service logs
    journalctl --since "24 hours ago" --priority=err >> "$report_file"
}
```

## Deployment Automation
###### tags: `deployment`, `automation`, `release`

```bash
# Deployment Manager
#!/bin/bash
deploy_config="/etc/automation/deploy.conf"
deploy_log="/var/log/automation/deploy.log"

deploy_application() {
    local app_name="$1"
    local repo_url="$2"
    local branch="$3"
    local deploy_dir="$4"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting deployment of $app_name..." >> "$deploy_log"
    
    # Backup current version
    if [ -d "$deploy_dir" ]; then
        tar czf "$deploy_dir.backup.tar.gz" "$deploy_dir"
    fi
    
    # Clone/update repository
    if [ -d "$deploy_dir/.git" ]; then
        cd "$deploy_dir" && git pull origin "$branch"
    else
        git clone -b "$branch" "$repo_url" "$deploy_dir"
    fi
    
    # Install dependencies
    if [ -f "$deploy_dir/package.json" ]; then
        cd "$deploy_dir" && npm install
    elif [ -f "$deploy_dir/requirements.txt" ]; then
        cd "$deploy_dir" && pip install -r requirements.txt
    fi
    
    # Build application
    if [ -f "$deploy_dir/package.json" ]; then
        cd "$deploy_dir" && npm run build
    fi
    
    # Restart service
    systemctl restart "$app_name"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deployment of $app_name completed" >> "$deploy_log"
}

# Rollback deployment
rollback_deployment() {
    local app_name="$1"
    local deploy_dir="$2"
    local backup_file="$deploy_dir.backup.tar.gz"
    
    if [ -f "$backup_file" ]; then
        rm -rf "$deploy_dir"
        tar xzf "$backup_file" -C "$(dirname "$deploy_dir")"
        systemctl restart "$app_name"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Rolled back $app_name to previous version" >> "$deploy_log"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] No backup found for $app_name" >> "$deploy_log"
    fi
}
```

## Configuration Management
###### tags: `configuration`, `management`, `templates`

```bash
# Configuration Manager
#!/bin/bash
config_dir="/etc/automation/configs"
template_dir="/etc/automation/templates"
inventory_file="/etc/automation/inventory.yml"

apply_configuration() {
    local host="$1"
    local role="$2"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Applying configuration for $host ($role)" >> "$log_file"
    
    # Load host variables
    eval "$(parse_yaml "$inventory_file" "host_")"
    
    # Process templates
    for template in "$template_dir/$role"/*.j2; do
        output_file=$(basename "${template%.j2}")
        envsubst < "$template" > "$config_dir/$output_file"
    done
    
    # Apply configuration
    case "$role" in
        "webserver")
            configure_webserver
            ;;
        "database")
            configure_database
            ;;
        "loadbalancer")
            configure_loadbalancer
            ;;
    esac
}

configure_webserver() {
    # Configure Nginx
    cp "$config_dir/nginx.conf" /etc/nginx/nginx.conf
    nginx -t && systemctl restart nginx
    
    # Configure PHP-FPM
    cp "$config_dir/php-fpm.conf" /etc/php-fpm.d/www.conf
    systemctl restart php-fpm
}

configure_database() {
    # Configure MySQL
    cp "$config_dir/my.cnf" /etc/my.cnf
    systemctl restart mysqld
    
    # Configure backup
    cp "$config_dir/backup.cnf" /etc/automysqlbackup/myserver.conf
    automysqlbackup
}

configure_loadbalancer() {
    # Configure HAProxy
    cp "$config_dir/haproxy.cfg" /etc/haproxy/haproxy.cfg
    haproxy -c -f /etc/haproxy/haproxy.cfg && systemctl restart haproxy
}
```

## Automated Testing
###### tags: `testing`, `automation`, `quality`

```bash
# Test Automation Manager
#!/bin/bash
test_dir="/etc/automation/tests"
report_dir="/var/log/automation/tests"
date_format=$(date +%Y%m%d)

run_tests() {
    local environment="$1"
    local test_suite="$2"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting test suite: $test_suite on $environment" >> "$log_file"
    
    # Prepare test environment
    case "$environment" in
        "development")
            export APP_ENV=dev
            export API_URL="http://dev-api.example.com"
            ;;
        "staging")
            export APP_ENV=staging
            export API_URL="http://staging-api.example.com"
            ;;
        *)
            echo "Invalid environment: $environment"
            exit 1
            ;;
    esac
    
    # Run tests
    case "$test_suite" in
        "unit")
            run_unit_tests
            ;;
        "integration")
            run_integration_tests
            ;;
        "e2e")
            run_e2e_tests
            ;;
        "all")
            run_unit_tests
            run_integration_tests
            run_e2e_tests
            ;;
    esac
}

run_unit_tests() {
    echo "Running unit tests..."
    if [ -f "package.json" ]; then
        npm test
    elif [ -f "pytest.ini" ]; then
        pytest tests/unit
    fi
}

run_integration_tests() {
    echo "Running integration tests..."
    if [ -f "package.json" ]; then
        npm run test:integration
    elif [ -f "pytest.ini" ]; then
        pytest tests/integration
    fi
}

run_e2e_tests() {
    echo "Running end-to-end tests..."
    if [ -f "package.json" ]; then
        npm run test:e2e
    elif [ -f "pytest.ini" ]; then
        pytest tests/e2e
    fi
}
```

## Continuous Integration
###### tags: `ci`, `automation`, `pipeline`

```bash
# CI Pipeline Manager
#!/bin/bash
ci_config="/etc/automation/ci.conf"
workspace="/var/lib/automation/workspace"
artifacts_dir="/var/lib/automation/artifacts"

run_pipeline() {
    local repo_url="$1"
    local branch="$2"
    local build_id=$(date +%Y%m%d_%H%M%S)
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting pipeline for $repo_url:$branch (Build: $build_id)" >> "$log_file"
    
    # Create workspace
    local build_dir="$workspace/$build_id"
    mkdir -p "$build_dir"
    
    # Clone repository
    git clone -b "$branch" "$repo_url" "$build_dir"
    cd "$build_dir"
    
    # Run stages
    if ! run_stage "build"; then
        echo "Build stage failed"
        cleanup_workspace
        exit 1
    fi
    
    if ! run_stage "test"; then
        echo "Test stage failed"
        cleanup_workspace
        exit 1
    fi
    
    if ! run_stage "deploy"; then
        echo "Deploy stage failed"
        cleanup_workspace
        exit 1
    fi
    
    # Archive artifacts
    mkdir -p "$artifacts_dir/$build_id"
    cp -r dist/* "$artifacts_dir/$build_id/"
    
    cleanup_workspace
}

run_stage() {
    local stage="$1"
    
    case "$stage" in
        "build")
            npm install && npm run build
            ;;
        "test")
            npm test
            ;;
        "deploy")
            # Deploy to staging
            rsync -avz dist/ user@staging:/var/www/app/
            ;;
    esac
    
    return $?
}

cleanup_workspace() {
    rm -rf "$build_dir"
}
```

## See Also
- [Basic Operations](basics.md)
- [System Monitoring](monitoring.md)
- [Deployment Scripts](deployment.md)
