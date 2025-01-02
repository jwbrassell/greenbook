# System Level Troubleshooting

## Table of Contents
- [System Level Troubleshooting](#system-level-troubleshooting)
  - [Table of Contents](#table-of-contents)
  - [Resource Monitoring](#resource-monitoring)
    - [Memory Issues](#memory-issues)
- [Check memory usage](#check-memory-usage)
- [Check swap usage](#check-swap-usage)
- [Monitor memory in real-time](#monitor-memory-in-real-time)
- [Check application memory](#check-application-memory)
    - [CPU Problems](#cpu-problems)
- [Check CPU usage](#check-cpu-usage)
- [Check load average](#check-load-average)
- [Monitor specific process](#monitor-specific-process)
    - [Disk Space Issues](#disk-space-issues)
- [Check disk space](#check-disk-space)
- [Check inodes](#check-inodes)
- [Find large files](#find-large-files)
- [Check disk I/O](#check-disk-i/o)
    - [Process Management](#process-management)
- [Check process status](#check-process-status)
- [Service management](#service-management)
- [Process limits](#process-limits)
  - [System Logs](#system-logs)
    - [Key Log Locations](#key-log-locations)
    - [Log Analysis Tools](#log-analysis-tools)
- [Real-time log monitoring](#real-time-log-monitoring)
- [Search logs](#search-logs)
- [Analyze Apache/Nginx logs](#analyze-apache/nginx-logs)
- [System journal](#system-journal)
  - [Performance Tuning](#performance-tuning)
    - [System Optimization](#system-optimization)
- [Kernel parameters](#kernel-parameters)
- [File system tuning](#file-system-tuning)
- [Network tuning](#network-tuning)
    - [Application Optimization](#application-optimization)
- [Profile CPU usage](#profile-cpu-usage)
- [Memory profiling](#memory-profiling)
- [Network profiling](#network-profiling)
  - [Preventive Measures](#preventive-measures)



## Resource Monitoring

### Memory Issues

**Symptoms:**
- System slowdown
- Out of memory errors
- Swap usage increases
- Application crashes

**Commands:**
```bash
# Check memory usage
free -h
vmstat 1
ps aux --sort=-%mem | head -n 10

# Check swap usage
swapon --show
cat /proc/swaps

# Monitor memory in real-time
watch -n 1 'free -h'

# Check application memory
pmap -x PID
smem -tk
```

**Solutions:**
1. Identify memory-hungry processes
   ```bash
   ps aux --sort=-%mem | head -n 10
   ```
2. Adjust application memory limits
   - Update systemd service files
   - Modify container resource limits
   - Adjust JVM heap settings
3. Optimize application memory usage
   - Enable garbage collection logging
   - Profile memory usage
   - Fix memory leaks
4. System-level adjustments
   ```bash
   # Adjust swappiness
   sysctl vm.swappiness=10
   
   # Clear page cache if needed
   sync; echo 3 > /proc/sys/vm/drop_caches
   ```

### CPU Problems

**Symptoms:**
- High load average
- Process throttling
- System unresponsiveness
- Slow application response

**Commands:**
```bash
# Check CPU usage
top -b n 1
mpstat -P ALL
pidstat 1

# Check load average
uptime
cat /proc/loadavg

# Monitor specific process
top -p PID
perf top -p PID
```

**Solutions:**
1. Identify CPU-intensive processes
   ```bash
   ps aux --sort=-%cpu | head -n 10
   ```
2. Profile application performance
   ```bash
   perf record -p PID
   perf report
   ```
3. System optimization
   ```bash
   # Adjust process priority
   renice -n 10 -p PID
   
   # CPU governor settings
   cpupower frequency-info
   ```

### Disk Space Issues

**Symptoms:**
- No space left errors
- Write failures
- System warnings
- Slow disk operations

**Commands:**
```bash
# Check disk space
df -h
du -sh /*
ncdu /

# Check inodes
df -i

# Find large files
find / -type f -size +100M -exec ls -lh {} \;

# Check disk I/O
iostat -x 1
iotop
```

**Solutions:**
1. Clean up disk space
   ```bash
   # Clean package cache
   apt-get clean
   yum clean all
   
   # Remove old logs
   journalctl --vacuum-time=7d
   
   # Find and remove old files
   find /var/log -type f -mtime +30 -delete
   ```
2. Monitor disk usage
   ```bash
   # Set up disk usage alerts
   df -h | awk '{ print $5 " " $1 }' | while read output;
   do
     usage=$(echo $output | awk '{ print $1}' | cut -d'%' -f1)
     partition=$(echo $output | awk '{ print $2 }')
     if [ $usage -ge 90 ]; then
       echo "Warning: $partition usage is $usage%"
     fi
   done
   ```

### Process Management

**Symptoms:**
- Unresponsive services
- Zombie processes
- High resource usage
- Service failures

**Commands:**
```bash
# Check process status
ps aux
pstree
top

# Service management
systemctl status service_name
journalctl -u service_name -f

# Process limits
ulimit -a
cat /proc/PID/limits
```

**Solutions:**
1. Handle unresponsive processes
   ```bash
   # Kill process
   kill -15 PID  # Graceful
   kill -9 PID   # Force
   
   # Restart service
   systemctl restart service_name
   ```
2. Adjust process limits
   ```bash
   # Edit system limits
   vim /etc/security/limits.conf
   
   # Set ulimit in script
   ulimit -n 65535
   ```

## System Logs

### Key Log Locations
```
/var/log/syslog          # General system logs
/var/log/messages        # General system messages
/var/log/dmesg          # Kernel ring buffer
/var/log/auth.log       # Authentication logs
/var/log/kern.log       # Kernel logs
~/.pm2/logs/            # PM2 process logs
/var/log/nginx/         # Nginx logs
/var/log/mysql/         # MySQL logs
```

### Log Analysis Tools
```bash
# Real-time log monitoring
tail -f /var/log/syslog

# Search logs
grep -r "error" /var/log/

# Analyze Apache/Nginx logs
goaccess /var/log/nginx/access.log

# System journal
journalctl -f
journalctl -u service_name
```

## Performance Tuning

### System Optimization
```bash
# Kernel parameters
sysctl -a
vim /etc/sysctl.conf

# File system tuning
tune2fs -l /dev/sda1
hdparm -tT /dev/sda

# Network tuning
ethtool eth0
tc qdisc show
```

### Application Optimization
```bash
# Profile CPU usage
perf record -F 99 -p PID -g -- sleep 30
perf report

# Memory profiling
valgrind --tool=massif ./program
massif-visualizer massif.out.pid

# Network profiling
nethogs
iftop
```

## Preventive Measures

1. **Monitoring Setup**
   - Configure system monitoring (Nagios, Prometheus, etc.)
   - Set up alerting thresholds
   - Implement log rotation
   - Regular backup verification

2. **Maintenance Schedule**
   - Regular system updates
   - Log rotation and cleanup
   - Backup verification
   - Performance audit

3. **Documentation**
   - Keep system inventory
   - Document configuration changes
   - Maintain troubleshooting runbooks
   - Update recovery procedures

4. **Automation**
   - Automated backups
   - System health checks
   - Log analysis
   - Performance monitoring
