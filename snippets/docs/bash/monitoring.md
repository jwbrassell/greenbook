# System Monitoring Scripts

## Table of Contents
- [System Monitoring Scripts](#system-monitoring-scripts)
  - [Table of Contents](#table-of-contents)
          - [tags: monitoring, resources, processes, disk, network, health](#tags:-monitoring,-resources,-processes,-disk,-network,-health)
  - [Resource Monitoring](#resource-monitoring)
          - [tags: resources, cpu, memory, load](#tags:-resources,-cpu,-memory,-load)
- [System Resource Monitor](#system-resource-monitor)
- [!/bin/bash](#!/bin/bash)
- [Alert thresholds](#alert-thresholds)
- [Start monitoring](#start-monitoring)
  - [Process Monitoring](#process-monitoring)
          - [tags: processes, cpu, memory, zombie](#tags:-processes,-cpu,-memory,-zombie)
- [Process Monitor](#process-monitor)
- [!/bin/bash](#!/bin/bash)
- [Zombie Process Check](#zombie-process-check)
  - [Disk Space Monitoring](#disk-space-monitoring)
          - [tags: disk, space, filesystem, inodes](#tags:-disk,-space,-filesystem,-inodes)
- [Disk Space Monitor](#disk-space-monitor)
- [!/bin/bash](#!/bin/bash)
- [Large File Finder](#large-file-finder)
- [Disk Growth Rate](#disk-growth-rate)
  - [Network Monitoring](#network-monitoring)
          - [tags: network, bandwidth, connections, ports](#tags:-network,-bandwidth,-connections,-ports)
- [Network Monitor](#network-monitor)
- [!/bin/bash](#!/bin/bash)
- [Port Scanner](#port-scanner)
- [Network Latency Monitor](#network-latency-monitor)
  - [Service Health Checks](#service-health-checks)
          - [tags: services, health, status, monitoring](#tags:-services,-health,-status,-monitoring)
- [Service Health Monitor](#service-health-monitor)
- [!/bin/bash](#!/bin/bash)
- [URL Health Check](#url-health-check)
- [Database Connection Check](#database-connection-check)
- [Main monitoring loop](#main-monitoring-loop)
  - [See Also](#see-also)



###### tags: `monitoring`, `resources`, `processes`, `disk`, `network`, `health`

## Resource Monitoring
###### tags: `resources`, `cpu`, `memory`, `load`

```bash
# System Resource Monitor
#!/bin/bash
log_file="/var/log/system_monitor.log"
interval=5

monitor_resources() {
    while true; do
        # CPU Usage
        cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
        
        # Memory Usage
        mem_total=$(free -m | awk 'NR==2{print $2}')
        mem_used=$(free -m | awk 'NR==2{print $3}')
        mem_usage=$(awk "BEGIN {printf \"%.2f\", $mem_used/$mem_total*100}")
        
        # Load Average
        load_avg=$(uptime | awk -F'load average:' '{print $2}' | tr -d ',')
        
        # Log Results
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] CPU: ${cpu_usage}% MEM: ${mem_usage}% Load: $load_avg" >> "$log_file"
        
        sleep "$interval"
    done
}

# Alert thresholds
check_thresholds() {
    if (( $(echo "$cpu_usage > 90" | bc -l) )); then
        send_alert "High CPU usage: ${cpu_usage}%"
    fi
    
    if (( $(echo "$mem_usage > 90" | bc -l) )); then
        send_alert "High memory usage: ${mem_usage}%"
    fi
}

# Start monitoring
monitor_resources &
```

## Process Monitoring
###### tags: `processes`, `cpu`, `memory`, `zombie`

```bash
# Process Monitor
#!/bin/bash
process_name="$1"
pid_file="/var/run/$process_name.pid"
log_file="/var/log/process_monitor.log"

monitor_process() {
    while true; do
        if ! pgrep -x "$process_name" > /dev/null; then
            echo "[$(date)] Process $process_name is not running!" >> "$log_file"
            restart_process
        else
            # Get process stats
            pid=$(pgrep -x "$process_name")
            cpu=$(ps -p "$pid" -o %cpu | tail -1)
            mem=$(ps -p "$pid" -o %mem | tail -1)
            
            echo "[$(date)] $process_name (PID: $pid) CPU: $cpu% MEM: $mem%" >> "$log_file"
        fi
        sleep 60
    done
}

restart_process() {
    echo "[$(date)] Attempting to restart $process_name..." >> "$log_file"
    systemctl restart "$process_name"
    sleep 5
    
    if pgrep -x "$process_name" > /dev/null; then
        echo "[$(date)] Successfully restarted $process_name" >> "$log_file"
    else
        echo "[$(date)] Failed to restart $process_name" >> "$log_file"
        send_alert "Failed to restart $process_name"
    fi
}

# Zombie Process Check
check_zombies() {
    zombies=$(ps aux | awk '$8=="Z"' | wc -l)
    if [ "$zombies" -gt 0 ]; then
        echo "[$(date)] Found $zombies zombie processes" >> "$log_file"
        ps aux | awk '$8=="Z"' >> "$log_file"
    fi
}
```

## Disk Space Monitoring
###### tags: `disk`, `space`, `filesystem`, `inodes`

```bash
# Disk Space Monitor
#!/bin/bash
threshold=90
email="admin@example.com"
log_file="/var/log/disk_monitor.log"

check_disk_space() {
    echo "=== Disk Space Check $(date) ===" >> "$log_file"
    
    # Check disk space usage
    df -h | grep '^/dev' | while read -r line; do
        usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
        mount=$(echo "$line" | awk '{print $6}')
        
        if [ "$usage" -gt "$threshold" ]; then
            message="WARNING: $mount is ${usage}% full"
            echo "$message" >> "$log_file"
            echo "$message" | mail -s "Disk Space Alert" "$email"
        fi
    done
    
    # Check inode usage
    df -i | grep '^/dev' | while read -r line; do
        usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
        mount=$(echo "$line" | awk '{print $6}')
        
        if [ "$usage" -gt "$threshold" ]; then
            message="WARNING: $mount inodes are ${usage}% used"
            echo "$message" >> "$log_file"
            echo "$message" | mail -s "Inode Usage Alert" "$email"
        fi
    done
}

# Large File Finder
find_large_files() {
    echo "=== Large Files Report $(date) ===" >> "$log_file"
    find / -type f -size +100M -exec ls -lh {} \; >> "$log_file" 2>/dev/null
}

# Disk Growth Rate
monitor_growth() {
    local mount="$1"
    local initial_usage=$(df -P "$mount" | awk 'NR==2 {print $3}')
    sleep 3600  # Wait an hour
    local final_usage=$(df -P "$mount" | awk 'NR==2 {print $3}')
    local growth=$(( (final_usage - initial_usage) / 1024 ))  # MB per hour
    echo "[$(date)] Growth rate for $mount: $growth MB/hour" >> "$log_file"
}
```

## Network Monitoring
###### tags: `network`, `bandwidth`, `connections`, `ports`

```bash
# Network Monitor
#!/bin/bash
interface="eth0"
log_file="/var/log/network_monitor.log"
interval=60

monitor_network() {
    while true; do
        # Get interface statistics
        rx_bytes_old=$(cat /sys/class/net/$interface/statistics/rx_bytes)
        tx_bytes_old=$(cat /sys/class/net/$interface/statistics/tx_bytes)
        sleep "$interval"
        rx_bytes_new=$(cat /sys/class/net/$interface/statistics/rx_bytes)
        tx_bytes_new=$(cat /sys/class/net/$interface/statistics/tx_bytes)
        
        # Calculate bandwidth
        rx_rate=$(( (rx_bytes_new - rx_bytes_old) / interval ))
        tx_rate=$(( (tx_bytes_new - tx_bytes_old) / interval ))
        
        # Get connection counts
        total_conn=$(netstat -an | grep ESTABLISHED | wc -l)
        
        echo "[$(date)] RX: $(( rx_rate / 1024 )) KB/s TX: $(( tx_rate / 1024 )) KB/s Connections: $total_conn" >> "$log_file"
        
        # Check thresholds
        if [ "$total_conn" -gt 1000 ]; then
            send_alert "High connection count: $total_conn"
        fi
    done
}

# Port Scanner
check_ports() {
    local host="$1"
    local ports="22 80 443 3306 5432"
    
    for port in $ports; do
        if nc -zv "$host" "$port" 2>&1 | grep -q succeeded; then
            echo "[$(date)] Port $port is open on $host" >> "$log_file"
        else
            echo "[$(date)] Port $port is closed on $host" >> "$log_file"
        fi
    done
}

# Network Latency Monitor
monitor_latency() {
    local target="$1"
    while true; do
        ping -c 1 "$target" | tail -1 | awk '{print $4}' | cut -d '/' -f 2 >> "$log_file"
        sleep 60
    done
}
```

## Service Health Checks
###### tags: `services`, `health`, `status`, `monitoring`

```bash
# Service Health Monitor
#!/bin/bash
services=("nginx" "mysql" "redis-server" "postgresql")
log_file="/var/log/service_health.log"

check_services() {
    echo "=== Service Health Check $(date) ===" >> "$log_file"
    
    for service in "${services[@]}"; do
        if systemctl is-active "$service" >/dev/null 2>&1; then
            echo "[OK] $service is running" >> "$log_file"
        else
            message="[FAIL] $service is not running"
            echo "$message" >> "$log_file"
            
            # Attempt to restart
            systemctl restart "$service"
            sleep 5
            
            if systemctl is-active "$service" >/dev/null 2>&1; then
                echo "[RECOVERED] $service was restarted successfully" >> "$log_file"
            else
                echo "[FATAL] Failed to restart $service" >> "$log_file"
                send_alert "Service $service is down and could not be restarted"
            fi
        fi
    done
}

# URL Health Check
check_urls() {
    local urls=(
        "http://localhost"
        "http://localhost:8080"
        "https://api.example.com"
    )
    
    for url in "${urls[@]}"; do
        response=$(curl -sL -w "%{http_code}" "$url" -o /dev/null)
        if [ "$response" = "200" ]; then
            echo "[OK] $url is accessible" >> "$log_file"
        else
            message="[FAIL] $url returned HTTP $response"
            echo "$message" >> "$log_file"
            send_alert "$message"
        fi
    done
}

# Database Connection Check
check_database() {
    if mysql -u "$DB_USER" -p"$DB_PASS" -e "SELECT 1" >/dev/null 2>&1; then
        echo "[OK] MySQL connection successful" >> "$log_file"
    else
        message="[FAIL] Cannot connect to MySQL"
        echo "$message" >> "$log_file"
        send_alert "$message"
    fi
}

# Main monitoring loop
while true; do
    check_services
    check_urls
    check_database
    sleep 300  # Check every 5 minutes
done
```

## See Also
- [Basic Operations](basics.md)
- [Advanced Script Patterns](advanced_patterns.md)
- [Log Analysis](logging.md)
