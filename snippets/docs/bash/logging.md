# Log Analysis Scripts

## Table of Contents
- [Log Analysis Scripts](#log-analysis-scripts)
  - [Table of Contents](#table-of-contents)
          - [tags: logs, analysis, parsing, statistics, reporting](#tags:-logs,-analysis,-parsing,-statistics,-reporting)
  - [Log Parser](#log-parser)
          - [tags: parsing, logs, filtering](#tags:-parsing,-logs,-filtering)
- [Log Parser](#log-parser)
- [!/bin/bash](#!/bin/bash)
- [Parse logs by severity](#parse-logs-by-severity)
- [Parse logs by service](#parse-logs-by-service)
- [Parse logs by time period](#parse-logs-by-time-period)
  - [Pattern Recognition](#pattern-recognition)
          - [tags: patterns, analysis, recognition](#tags:-patterns,-analysis,-recognition)
- [Pattern Recognition](#pattern-recognition)
- [!/bin/bash](#!/bin/bash)
- [Custom pattern matching](#custom-pattern-matching)
- [Pattern correlation](#pattern-correlation)
  - [Statistical Analysis](#statistical-analysis)
          - [tags: statistics, analysis, metrics](#tags:-statistics,-analysis,-metrics)
- [Statistical Analysis](#statistical-analysis)
- [!/bin/bash](#!/bin/bash)
- [Time-based analysis](#time-based-analysis)
- [Service performance metrics](#service-performance-metrics)
  - [Report Generation](#report-generation)
          - [tags: reports, html, documentation](#tags:-reports,-html,-documentation)
- [Report Generator](#report-generator)
- [!/bin/bash](#!/bin/bash)
- [Log Analysis Report](#log-analysis-report)
  - [Summary Statistics](#summary-statistics)
  - [Pattern Matches](#pattern-matches)
  - [Severity Analysis](#severity-analysis)
  - [Service Analysis](#service-analysis)
- [Generate PDF report](#generate-pdf-report)
- [Email report](#email-report)
  - [Log Rotation](#log-rotation)
          - [tags: rotation, archival, maintenance](#tags:-rotation,-archival,-maintenance)
- [Log Rotation Manager](#log-rotation-manager)
- [!/bin/bash](#!/bin/bash)
- [Archive old logs](#archive-old-logs)
- [Clean up temporary files](#clean-up-temporary-files)
  - [Real-time Monitoring](#real-time-monitoring)
          - [tags: monitoring, realtime, alerts](#tags:-monitoring,-realtime,-alerts)
- [Real-time Log Monitor](#real-time-log-monitor)
- [!/bin/bash](#!/bin/bash)
- [Alert function](#alert-function)
- [Start monitoring](#start-monitoring)
  - [See Also](#see-also)



###### tags: `logs`, `analysis`, `parsing`, `statistics`, `reporting`

## Log Parser
###### tags: `parsing`, `logs`, `filtering`

```bash
# Log Parser
#!/bin/bash
log_file="/var/log/syslog"
output_dir="/var/log/analysis"
date_format=$(date +%Y%m%d)

# Parse logs by severity
parse_by_severity() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Parsing logs by severity..." >> "$output_dir/parser.log"
    
    # Create output directory
    mkdir -p "$output_dir"
    
    # Emergency (emerg)
    grep -i "emerg" "$log_file" > "$output_dir/emerg_$date_format.log"
    
    # Alert (alert)
    grep -i "alert" "$log_file" > "$output_dir/alert_$date_format.log"
    
    # Critical (crit)
    grep -i "crit" "$log_file" > "$output_dir/crit_$date_format.log"
    
    # Error (err)
    grep -i "error" "$log_file" > "$output_dir/error_$date_format.log"
    
    # Warning (warning)
    grep -i "warning" "$log_file" > "$output_dir/warning_$date_format.log"
    
    # Generate summary
    {
        echo "=== Log Analysis Summary $(date) ==="
        echo "Emergency messages: $(wc -l < "$output_dir/emerg_$date_format.log")"
        echo "Alert messages: $(wc -l < "$output_dir/alert_$date_format.log")"
        echo "Critical messages: $(wc -l < "$output_dir/crit_$date_format.log")"
        echo "Error messages: $(wc -l < "$output_dir/error_$date_format.log")"
        echo "Warning messages: $(wc -l < "$output_dir/warning_$date_format.log")"
    } > "$output_dir/severity_summary_$date_format.log"
}

# Parse logs by service
parse_by_service() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Parsing logs by service..." >> "$output_dir/parser.log"
    
    # Define services to monitor
    services=("sshd" "apache2" "nginx" "mysql" "postgresql")
    
    for service in "${services[@]}"; do
        grep "$service" "$log_file" > "$output_dir/${service}_$date_format.log"
    done
}

# Parse logs by time period
parse_by_time() {
    local start_time="$1"  # Format: HH:MM
    local end_time="$2"    # Format: HH:MM
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Parsing logs by time period..." >> "$output_dir/parser.log"
    
    awk -v start="$start_time" -v end="$end_time" '
        $3 >= start && $3 <= end
    ' "$log_file" > "$output_dir/time_${start_time}-${end_time}_$date_format.log"
}
```

## Pattern Recognition
###### tags: `patterns`, `analysis`, `recognition`

```bash
# Pattern Recognition
#!/bin/bash
patterns_file="/etc/log_patterns.conf"
report_file="/var/log/pattern_matches.log"

analyze_patterns() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting pattern analysis..." >> "$report_file"
    
    while IFS=: read -r pattern description; do
        echo "=== Analyzing pattern: $description ===" >> "$report_file"
        
        # Count occurrences
        count=$(grep -c "$pattern" "$log_file")
        echo "Occurrences: $count" >> "$report_file"
        
        # Show examples
        echo "Examples:" >> "$report_file"
        grep "$pattern" "$log_file" | head -n 3 >> "$report_file"
        echo "---" >> "$report_file"
    done < "$patterns_file"
}

# Custom pattern matching
match_custom_patterns() {
    # Authentication failures
    grep -E "authentication failure|failed password|invalid user" "$log_file" \
        > "$output_dir/auth_failures_$date_format.log"
    
    # Resource issues
    grep -E "out of memory|disk full|load average" "$log_file" \
        > "$output_dir/resource_issues_$date_format.log"
    
    # Security events
    grep -E "firewall|blocked|violation|attack" "$log_file" \
        > "$output_dir/security_events_$date_format.log"
}

# Pattern correlation
correlate_patterns() {
    local time_window=300  # 5 minutes in seconds
    
    while read -r line1; do
        timestamp1=$(date -d "$(echo "$line1" | cut -d' ' -f1,2,3)" +%s)
        
        while read -r line2; do
            timestamp2=$(date -d "$(echo "$line2" | cut -d' ' -f1,2,3)" +%s)
            
            if [ $((timestamp2 - timestamp1)) -le "$time_window" ]; then
                echo "Correlated events within $time_window seconds:" >> "$report_file"
                echo "$line1" >> "$report_file"
                echo "$line2" >> "$report_file"
                echo "---" >> "$report_file"
            fi
        done < "$output_dir/security_events_$date_format.log"
    done < "$output_dir/resource_issues_$date_format.log"
}
```

## Statistical Analysis
###### tags: `statistics`, `analysis`, `metrics`

```bash
# Statistical Analysis
#!/bin/bash
stats_file="/var/log/log_statistics.log"

generate_statistics() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generating log statistics..." >> "$stats_file"
    
    # Total entries
    total_lines=$(wc -l < "$log_file")
    echo "Total Log Entries: $total_lines" >> "$stats_file"
    
    # Entries by hour
    echo -e "\nEntries by Hour:" >> "$stats_file"
    awk '{print $3}' "$log_file" | cut -d: -f1 | sort | uniq -c >> "$stats_file"
    
    # Top IP addresses
    echo -e "\nTop Source IPs:" >> "$stats_file"
    grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' "$log_file" | \
        sort | uniq -c | sort -nr | head -n 10 >> "$stats_file"
    
    # Most frequent messages
    echo -e "\nMost Common Messages:" >> "$stats_file"
    awk '{$1=$2=$3=$4=""; print $0}' "$log_file" | \
        sort | uniq -c | sort -nr | head -n 10 >> "$stats_file"
    
    # Error rate calculation
    total_errors=$(grep -ci "error" "$log_file")
    error_rate=$(awk "BEGIN {printf \"%.2f\", $total_errors/$total_lines*100}")
    echo -e "\nError Rate: $error_rate%" >> "$stats_file"
}

# Time-based analysis
analyze_time_patterns() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Analyzing time patterns..." >> "$stats_file"
    
    # Peak hours
    echo -e "\nPeak Hours:" >> "$stats_file"
    awk '{print $3}' "$log_file" | cut -d: -f1 | sort | uniq -c | \
        sort -nr | head -n 5 >> "$stats_file"
    
    # Weekend vs Weekday
    echo -e "\nWeekday vs Weekend Distribution:" >> "$stats_file"
    awk '{print $1,$2,$3}' "$log_file" | \
        while read -r month day time; do
            date -d "$month $day" +%u
        done | sort | uniq -c >> "$stats_file"
}

# Service performance metrics
analyze_service_performance() {
    local service="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Analyzing $service performance..." >> "$stats_file"
    
    # Response times
    grep "$service" "$log_file" | grep "time=" | \
        awk -F"time=" '{print $2}' | cut -d' ' -f1 | \
        awk '
            BEGIN {sum=0; count=0}
            {sum+=$1; count++}
            END {
                if(count>0) printf "Average response time: %.2fms\n", sum/count
            }
        ' >> "$stats_file"
    
    # Error frequency
    grep "$service" "$log_file" | grep -i "error" | \
        awk '{print $3}' | cut -d: -f1 | sort | uniq -c >> "$stats_file"
}
```

## Report Generation
###### tags: `reports`, `html`, `documentation`

```bash
# Report Generator
#!/bin/bash
report_dir="/var/log/reports"
html_report="$report_dir/log_analysis_$date_format.html"

generate_html_report() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generating HTML report..." >> "$report_dir/generator.log"
    
    cat > "$html_report" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Log Analysis Report - $(date)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .section { margin-bottom: 20px; }
        .chart { width: 800px; height: 400px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        th { background-color: #f2f2f2; }
        .warning { color: orange; }
        .error { color: red; }
        .critical { color: darkred; }
    </style>
</head>
<body>
    <h1>Log Analysis Report</h1>
    
    <div class="section">
        <h2>Summary Statistics</h2>
        <pre>$(cat "$stats_file")</pre>
    </div>
    
    <div class="section">
        <h2>Pattern Matches</h2>
        <pre>$(cat "$report_file")</pre>
    </div>
    
    <div class="section">
        <h2>Severity Analysis</h2>
        <table>
            <tr><th>Severity</th><th>Count</th></tr>
            <tr><td>Emergency</td><td>$(wc -l < "$output_dir/emerg_$date_format.log")</td></tr>
            <tr><td>Alert</td><td>$(wc -l < "$output_dir/alert_$date_format.log")</td></tr>
            <tr><td>Critical</td><td>$(wc -l < "$output_dir/crit_$date_format.log")</td></tr>
            <tr><td>Error</td><td>$(wc -l < "$output_dir/error_$date_format.log")</td></tr>
            <tr><td>Warning</td><td>$(wc -l < "$output_dir/warning_$date_format.log")</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Service Analysis</h2>
        <pre>$(cat "$output_dir/service_analysis_$date_format.log")</pre>
    </div>
</body>
</html>
EOF
}

# Generate PDF report
generate_pdf_report() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generating PDF report..." >> "$report_dir/generator.log"
    
    wkhtmltopdf "$html_report" "$report_dir/log_analysis_$date_format.pdf"
}

# Email report
email_report() {
    local recipient="$1"
    local subject="Log Analysis Report - $(date '+%Y-%m-%d')"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Emailing report to $recipient..." >> "$report_dir/generator.log"
    
    mutt -s "$subject" \
        -a "$report_dir/log_analysis_$date_format.pdf" \
        -- "$recipient" < /dev/null
}
```

## Log Rotation
###### tags: `rotation`, `archival`, `maintenance`

```bash
# Log Rotation Manager
#!/bin/bash
max_size=100M              # Maximum log size
retention_days=30          # Days to keep logs
archive_dir="/var/archives/logs"
compress_logs=true         # Whether to compress rotated logs

rotate_logs() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking logs for rotation..." >> "$log_file"
    
    # Check log size
    current_size=$(du -b "$log_file" | cut -f1)
    max_size_bytes=$(numfmt --from=iec $max_size)
    
    if [ "$current_size" -gt "$max_size_bytes" ]; then
        # Rotate the log
        mv "$log_file" "$log_file.1"
        touch "$log_file"
        
        # Compress if enabled
        if [ "$compress_logs" = true ]; then
            gzip "$log_file.1"
        fi
        
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Rotated log file" >> "$log_file"
    fi
}

# Archive old logs
archive_old_logs() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Archiving old logs..." >> "$log_file"
    
    # Create archive directory
    mkdir -p "$archive_dir"
    
    # Move old logs to archive
    find "$output_dir" -type f -name "*.log" -mtime +"$retention_days" \
        -exec mv {} "$archive_dir/" \;
    
    # Compress archived logs
    find "$archive_dir" -type f -name "*.log" ! -name "*.gz" \
        -exec gzip {} \;
    
    # Remove old archives
    find "$archive_dir" -type f -mtime +365 -delete
}

# Clean up temporary files
cleanup_temp_files() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleaning up temporary files..." >> "$log_file"
    
    find "$output_dir" -type f -name "temp_*" -mtime +1 -delete
    find "$report_dir" -type f -name "*.tmp" -mtime +1 -delete
}
```

## Real-time Monitoring
###### tags: `monitoring`, `realtime`, `alerts`

```bash
# Real-time Log Monitor
#!/bin/bash
alert_threshold=10         # Alert if more than X errors per minute
notification_email="admin@example.com"
error_count=0
last_check=$(date +%s)

monitor_realtime() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting real-time monitoring..." >> "$log_file"
    
    tail -F "$log_file" | while read -r line; do
        # Check for errors
        if echo "$line" | grep -iE "error|failed|failure" > /dev/null; then
            ((error_count++))
            
            # Check if we should reset counter
            current_time=$(date +%s)
            if [ $((current_time - last_check)) -ge 60 ]; then
                if [ "$error_count" -gt "$alert_threshold" ]; then
                    send_alert "High error rate: $error_count errors in last minute"
                fi
                error_count=0
                last_check=$current_time
            fi
        fi
        
        # Process other patterns
        case "$line" in
            *"Authentication failure"*)
                echo "[AUTH] $line" >> "$output_dir/auth_failures.log"
                ;;
            *"Connection refused"*)
                echo "[CONN] $line" >> "$output_dir/connection_issues.log"
                ;;
            *"Out of memory"*)
                echo "[OOM] $line" >> "$output_dir/resource_issues.log"
                ;;
        esac
    done
}

# Alert function
send_alert() {
    local message="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: $message" >> "$log_file"
    
    # Email alert
    echo "$message" | mail -s "Log Alert" "$notification_email"
    
    # Slack notification (if configured)
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"$message\"}" \
            "$SLACK_WEBHOOK"
    fi
}

# Start monitoring
monitor_realtime &
```

## See Also
- [Basic Operations](basics.md)
- [System Monitoring](monitoring.md)
- [Security Auditing](security.md)
