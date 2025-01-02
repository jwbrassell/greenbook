# Security Audit Scripts

## Table of Contents
- [Security Audit Scripts](#security-audit-scripts)
  - [Table of Contents](#table-of-contents)
          - [tags: security, audit, compliance, monitoring, scanning](#tags:-security,-audit,-compliance,-monitoring,-scanning)
  - [File System Integrity](#file-system-integrity)
          - [tags: filesystem, integrity, monitoring, changes](#tags:-filesystem,-integrity,-monitoring,-changes)
- [File System Integrity Checker](#file-system-integrity-checker)
- [!/bin/bash](#!/bin/bash)
- [Create baseline database](#create-baseline-database)
- [Check against baseline](#check-against-baseline)
- [Monitor for real-time changes](#monitor-for-real-time-changes)
  - [User Activity Monitoring](#user-activity-monitoring)
          - [tags: users, activity, monitoring, audit](#tags:-users,-activity,-monitoring,-audit)
- [User Activity Monitor](#user-activity-monitor)
- [!/bin/bash](#!/bin/bash)
- [Monitor suspicious activity](#monitor-suspicious-activity)
  - [Security Policy Compliance](#security-policy-compliance)
          - [tags: compliance, policy, security, audit](#tags:-compliance,-policy,-security,-audit)
- [Security Policy Checker](#security-policy-checker)
- [!/bin/bash](#!/bin/bash)
  - [Vulnerability Scanning](#vulnerability-scanning)
          - [tags: vulnerability, scanning, security, assessment](#tags:-vulnerability,-scanning,-security,-assessment)
- [Vulnerability Scanner](#vulnerability-scanner)
- [!/bin/bash](#!/bin/bash)
- [Package vulnerability check](#package-vulnerability-check)
  - [Access Control Auditing](#access-control-auditing)
          - [tags: access, permissions, audit, security](#tags:-access,-permissions,-audit,-security)
- [Access Control Auditor](#access-control-auditor)
- [!/bin/bash](#!/bin/bash)
  - [Security Baseline](#security-baseline)
          - [tags: baseline, security, audit, compliance](#tags:-baseline,-security,-audit,-compliance)
- [Security Baseline Checker](#security-baseline-checker)
- [!/bin/bash](#!/bin/bash)
  - [See Also](#see-also)



###### tags: `security`, `audit`, `compliance`, `monitoring`, `scanning`

## File System Integrity
###### tags: `filesystem`, `integrity`, `monitoring`, `changes`

```bash
# File System Integrity Checker
#!/bin/bash
log_file="/var/log/fs_audit.log"
baseline="/var/lib/fs_baseline.db"
exclude_list="/etc/audit/exclude.list"

# Create baseline database
create_baseline() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Creating baseline..." >> "$log_file"
    
    find / -type f \
        -not -path "/proc/*" \
        -not -path "/sys/*" \
        -not -path "/tmp/*" \
        -not -path "/run/*" \
        -not -path "/dev/*" \
        -not -path "/var/log/*" \
        -exec sha256sum {} \; 2>/dev/null | \
        grep -v -f "$exclude_list" > "$baseline"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Baseline created" >> "$log_file"
}

# Check against baseline
check_integrity() {
    local changes=0
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting integrity check..." >> "$log_file"
    
    while IFS= read -r line; do
        hash=${line%% *}
        file=${line#* }
        
        if [ -f "$file" ]; then
            current_hash=$(sha256sum "$file" 2>/dev/null | cut -d' ' -f1)
            if [ "$hash" != "$current_hash" ]; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] File changed: $file" >> "$log_file"
                ((changes++))
            fi
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] File missing: $file" >> "$log_file"
            ((changes++))
        fi
    done < "$baseline"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Found $changes changes" >> "$log_file"
    return $changes
}

# Monitor for real-time changes
monitor_changes() {
    inotifywait -m -r \
        --exclude '(/proc|/sys|/tmp|/run|/dev|/var/log)' \
        -e modify,create,delete,move / | \
    while read -r directory event file; do
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $event: $directory$file" >> "$log_file"
    done
}
```

## User Activity Monitoring
###### tags: `users`, `activity`, `monitoring`, `audit`

```bash
# User Activity Monitor
#!/bin/bash
auth_log="/var/log/auth.log"
report_dir="/var/log/user_audit"
date_format=$(date +%Y%m%d)

monitor_user_activity() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting user activity audit..." >> "$report_dir/audit.log"
    
    # Failed login attempts
    grep "Failed password" "$auth_log" > "$report_dir/failed_logins_$date_format.log"
    
    # Successful logins
    grep "session opened" "$auth_log" > "$report_dir/successful_logins_$date_format.log"
    
    # Sudo usage
    grep "sudo:" "$auth_log" > "$report_dir/sudo_usage_$date_format.log"
    
    # User modifications
    grep -E "useradd|usermod|userdel" "$auth_log" > "$report_dir/user_changes_$date_format.log"
    
    # Generate summary
    {
        echo "=== User Activity Summary $(date) ==="
        echo "Failed login attempts: $(wc -l < "$report_dir/failed_logins_$date_format.log")"
        echo "Successful logins: $(wc -l < "$report_dir/successful_logins_$date_format.log")"
        echo "Sudo commands: $(wc -l < "$report_dir/sudo_usage_$date_format.log")"
        echo "User account changes: $(wc -l < "$report_dir/user_changes_$date_format.log")"
    } > "$report_dir/summary_$date_format.log"
}

# Monitor suspicious activity
monitor_suspicious() {
    # Multiple failed logins
    awk '/Failed password/ {print $11}' "$auth_log" | \
        sort | uniq -c | \
        awk '$1 >= 5 {print $2}' | \
        while read -r ip; do
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Multiple failed logins from $ip" >> "$report_dir/suspicious.log"
            send_alert "Multiple failed logins from $ip"
        done
    
    # Root login attempts
    grep "authentication failure.*root" "$auth_log" >> "$report_dir/root_attempts.log"
    
    # Off-hours activity
    if [ "$(date +%H)" -gt 22 ] || [ "$(date +%H)" -lt 6 ]; then
        grep "session opened" "$auth_log" | tail -n 10 >> "$report_dir/off_hours.log"
    fi
}
```

## Security Policy Compliance
###### tags: `compliance`, `policy`, `security`, `audit`

```bash
# Security Policy Checker
#!/bin/bash
policy_file="/etc/security/policy.conf"
report_file="/var/log/compliance_report.log"

check_password_policy() {
    local issues=0
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking password policies..." >> "$report_file"
    
    # Check password aging
    for user in $(cut -d: -f1 /etc/passwd); do
        max_days=$(chage -l "$user" | grep "Maximum" | cut -d: -f2)
        if [ "$max_days" -gt 90 ]; then
            echo "Password policy violation: $user password max age > 90 days" >> "$report_file"
            ((issues++))
        fi
    done
    
    # Check password complexity
    if ! grep -q "^password.*pam_cracklib.so" /etc/pam.d/common-password; then
        echo "Password complexity not enforced" >> "$report_file"
        ((issues++))
    fi
    
    return $issues
}

check_ssh_config() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking SSH configuration..." >> "$report_file"
    
    # Check SSH configuration
    local ssh_config="/etc/ssh/sshd_config"
    local issues=0
    
    # Root login
    if grep -q "^PermitRootLogin yes" "$ssh_config"; then
        echo "Security violation: Root login allowed" >> "$report_file"
        ((issues++))
    fi
    
    # Password authentication
    if grep -q "^PasswordAuthentication yes" "$ssh_config"; then
        echo "Warning: Password authentication enabled" >> "$report_file"
        ((issues++))
    fi
    
    # Protocol version
    if grep -q "^Protocol 1" "$ssh_config"; then
        echo "Security violation: SSHv1 enabled" >> "$report_file"
        ((issues++))
    fi
    
    return $issues
}

check_firewall() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking firewall configuration..." >> "$report_file"
    
    # Check if firewall is active
    if ! systemctl is-active --quiet ufw; then
        echo "Security violation: Firewall not active" >> "$report_file"
        return 1
    fi
    
    # Check default policies
    ufw status verbose | grep "Default" >> "$report_file"
}
```

## Vulnerability Scanning
###### tags: `vulnerability`, `scanning`, `security`, `assessment`

```bash
# Vulnerability Scanner
#!/bin/bash
scan_targets="/etc/security/scan_targets.txt"
output_dir="/var/log/security_scans"
date_format=$(date +%Y%m%d)

run_security_scan() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting security scan..." >> "$output_dir/scan.log"
    
    # Port scan
    while IFS= read -r target; do
        nmap -sV -sC -oN "$output_dir/nmap_$target_$date_format.log" "$target"
    done < "$scan_targets"
    
    # SSL/TLS check
    while IFS= read -r target; do
        openssl s_client -connect "$target:443" \
            < /dev/null 2> "$output_dir/ssl_$target_$date_format.log"
    done < "$scan_targets"
    
    # Web vulnerability scan
    while IFS= read -r target; do
        nikto -h "$target" -o "$output_dir/nikto_$target_$date_format.txt"
    done < "$scan_targets"
}

# Package vulnerability check
check_package_vulnerabilities() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking package vulnerabilities..." >> "$output_dir/packages.log"
    
    # Update package lists
    apt-get update >/dev/null 2>&1
    
    # Check for security updates
    apt-get --just-print upgrade | grep -i security >> "$output_dir/security_updates.log"
    
    # List installed packages with known vulnerabilities
    debsecan --suite $(lsb_release -cs) --only-fixed >> "$output_dir/vulnerable_packages.log"
}
```

## Access Control Auditing
###### tags: `access`, `permissions`, `audit`, `security`

```bash
# Access Control Auditor
#!/bin/bash
acl_report="/var/log/acl_audit.log"

audit_file_permissions() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting file permissions audit..." >> "$acl_report"
    
    # World-writable files
    find / -type f -perm -0002 -ls 2>/dev/null >> "$acl_report"
    
    # Files without owner
    find / -type f -nouser -ls 2>/dev/null >> "$acl_report"
    
    # SUID/SGID files
    find / -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null >> "$acl_report"
    
    # ACL usage
    getfacl -R -p /etc 2>/dev/null >> "$acl_report"
}

audit_user_groups() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting user/group audit..." >> "$acl_report"
    
    # Users with UID 0
    awk -F: '$3 == 0 {print $1}' /etc/passwd >> "$acl_report"
    
    # Users in sudo group
    getent group sudo | cut -d: -f4 >> "$acl_report"
    
    # Empty password check
    awk -F: '$2 == "" {print $1}' /etc/shadow >> "$acl_report"
    
    # Group membership audit
    for user in $(cut -d: -f1 /etc/passwd); do
        groups "$user" >> "$acl_report"
    done
}
```

## Security Baseline
###### tags: `baseline`, `security`, `audit`, `compliance`

```bash
# Security Baseline Checker
#!/bin/bash
baseline_report="/var/log/security_baseline.log"

check_security_baseline() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting security baseline check..." >> "$baseline_report"
    
    # Kernel parameters
    {
        echo "=== Kernel Security Parameters ==="
        sysctl -a | grep -E \
            'kernel.randomize_va_space|net.ipv4.tcp_syncookies|kernel.core_pattern'
    } >> "$baseline_report"
    
    # Running services
    {
        echo "=== Running Services ==="
        systemctl list-units --type=service --state=running
    } >> "$baseline_report"
    
    # Open ports
    {
        echo "=== Open Ports ==="
        netstat -tulpn
    } >> "$baseline_report"
    
    # Installed packages
    {
        echo "=== Installed Packages ==="
        dpkg -l | grep '^ii'
    } >> "$baseline_report"
    
    # System updates
    {
        echo "=== Available Updates ==="
        apt list --upgradable 2>/dev/null
    } >> "$baseline_report"
    
    # Security configurations
    {
        echo "=== Security Configurations ==="
        echo "Password aging:"
        grep "^PASS_MAX_DAYS" /etc/login.defs
        echo "SSH settings:"
        grep -E '^(PermitRootLogin|PasswordAuthentication|Protocol)' /etc/ssh/sshd_config
    } >> "$baseline_report"
}
```

## See Also
- [Basic Operations](basics.md)
- [Network Management](network.md)
- [System Monitoring](monitoring.md)
