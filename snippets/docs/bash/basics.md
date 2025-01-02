# Basic Bash Operations

## Table of Contents
- [Basic Bash Operations](#basic-bash-operations)
  - [Table of Contents](#table-of-contents)
          - [tags: files, directory, system, process, text, network, user, package](#tags:-files,-directory,-system,-process,-text,-network,-user,-package)
  - [File Operations](#file-operations)
          - [tags: files, copy, move, delete, permissions](#tags:-files,-copy,-move,-delete,-permissions)
- [File manipulation](#file-manipulation)
- [File permissions](#file-permissions)
- [File information](#file-information)
- [File content](#file-content)
  - [Directory Operations](#directory-operations)
          - [tags: directory, folder, navigation, path](#tags:-directory,-folder,-navigation,-path)
- [Navigation](#navigation)
- [Directory manipulation](#directory-manipulation)
- [Directory listing](#directory-listing)
  - [System Information](#system-information)
          - [tags: system, hardware, monitoring, performance](#tags:-system,-hardware,-monitoring,-performance)
- [System info](#system-info)
- [Hardware info](#hardware-info)
- [System monitoring](#system-monitoring)
  - [Process Management](#process-management)
          - [tags: process, job, background, foreground, kill](#tags:-process,-job,-background,-foreground,-kill)
- [Process control](#process-control)
- [Job control](#job-control)
- [Process priority](#process-priority)
  - [Text Processing](#text-processing)
          - [tags: text, search, replace, filter, sort](#tags:-text,-search,-replace,-filter,-sort)
- [Text search](#text-search)
- [Text manipulation](#text-manipulation)
- [Text viewing](#text-viewing)
  - [Network Commands](#network-commands)
          - [tags: network, internet, connectivity, monitoring](#tags:-network,-internet,-connectivity,-monitoring)
- [Network information](#network-information)
- [Network testing](#network-testing)
- [Network monitoring](#network-monitoring)
  - [User Management](#user-management)
          - [tags: users, groups, permissions, security](#tags:-users,-groups,-permissions,-security)
- [User commands](#user-commands)
- [Group commands](#group-commands)
- [Permission management](#permission-management)
  - [Package Management](#package-management)
          - [tags: packages, software, installation, updates](#tags:-packages,-software,-installation,-updates)
- [APT (Debian/Ubuntu)](#apt-debian/ubuntu)
- [YUM (RHEL/CentOS)](#yum-rhel/centos)
- [DNF (Fedora)](#dnf-fedora)
  - [See Also](#see-also)



###### tags: `files`, `directory`, `system`, `process`, `text`, `network`, `user`, `package`

## File Operations
###### tags: `files`, `copy`, `move`, `delete`, `permissions`

```bash
# File manipulation
cp file1 file2           # Copy file
mv file1 file2           # Move/rename file
rm file                  # Remove file
rm -f file              # Force remove
rm -r directory         # Remove directory
rm -rf directory        # Force remove directory
touch file              # Create empty file
ln -s target link       # Create symbolic link

# File permissions
chmod 755 file          # Change permissions
chmod u+x file          # Add execute permission for user
chown user:group file   # Change ownership
chown -R user directory # Recursive ownership change

# File information
ls -l file              # List file details
file filename           # Show file type
stat file               # Display file status
du -sh file             # Show file size
find . -name "*.txt"    # Find files
locate filename         # Find files in database

# File content
cat file                # Display file content
less file               # Page through file
head file              # Show first 10 lines
tail file              # Show last 10 lines
tail -f file           # Follow file changes
grep pattern file      # Search in file
```

## Directory Operations
###### tags: `directory`, `folder`, `navigation`, `path`

```bash
# Navigation
cd directory           # Change directory
cd ..                 # Go up one level
cd ~                  # Go to home directory
cd -                  # Go to previous directory
pwd                   # Print working directory

# Directory manipulation
mkdir directory       # Create directory
mkdir -p dir1/dir2    # Create parent directories
rmdir directory       # Remove empty directory
rm -r directory      # Remove directory and contents

# Directory listing
ls                    # List files
ls -l                 # Long format
ls -a                 # Show hidden files
ls -R                 # Recursive listing
ls -lh                # Human readable sizes
tree                  # Show directory tree
```

## System Information
###### tags: `system`, `hardware`, `monitoring`, `performance`

```bash
# System info
uname -a              # System information
hostname              # Show hostname
uptime                # System uptime
date                  # Show date/time
cal                   # Show calendar
w                     # Show logged in users
whoami                # Show current user

# Hardware info
lscpu                 # CPU information
free -h               # Memory usage
df -h                 # Disk usage
lsblk                 # Block devices
lsusb                 # USB devices
lspci                 # PCI devices

# System monitoring
top                   # Process monitor
htop                  # Enhanced top
ps aux               # Process list
vmstat               # Virtual memory stats
iostat               # IO statistics
netstat              # Network statistics
```

## Process Management
###### tags: `process`, `job`, `background`, `foreground`, `kill`

```bash
# Process control
ps                    # Show processes
ps aux               # Show all processes
top                  # Interactive process viewer
kill pid             # Kill process
kill -9 pid          # Force kill
killall name         # Kill by name
pkill pattern        # Kill by pattern

# Job control
command &            # Run in background
fg                   # Bring to foreground
bg                   # Send to background
jobs                 # List jobs
nohup command &      # Run immune to hangups
screen               # Terminal multiplexer
tmux                 # Terminal multiplexer

# Process priority
nice -n 10 command   # Run with priority
renice +10 pid       # Change priority
```

## Text Processing
###### tags: `text`, `search`, `replace`, `filter`, `sort`

```bash
# Text search
grep pattern file     # Search for pattern
grep -r pattern dir   # Recursive search
grep -i pattern file  # Case insensitive
grep -v pattern file  # Invert match
egrep pattern file    # Extended regex

# Text manipulation
sed 's/old/new/' file # Replace text
sed -i 's/old/new/g' file # Replace in file
awk '{print $1}' file # Process text
sort file            # Sort lines
uniq file           # Remove duplicates
wc file             # Count words/lines
cut -d: -f1 file    # Cut columns

# Text viewing
cat file            # Show file content
less file           # Page through file
head -n 5 file      # Show first 5 lines
tail -n 5 file      # Show last 5 lines
diff file1 file2    # Compare files
```

## Network Commands
###### tags: `network`, `internet`, `connectivity`, `monitoring`

```bash
# Network information
ifconfig             # Network interfaces
ip addr              # IP addresses
netstat -tuln        # Open ports
ss -tuln             # Socket statistics
route -n             # Routing table
arp -a               # ARP cache

# Network testing
ping host           # Test connectivity
traceroute host     # Trace route
dig domain          # DNS lookup
nslookup domain     # Name server lookup
whois domain        # Domain information
curl url            # HTTP request
wget url            # Download file

# Network monitoring
tcpdump             # Packet capture
iftop               # Network monitor
nethogs             # Per-process monitor
iptables -L         # Firewall rules
```

## User Management
###### tags: `users`, `groups`, `permissions`, `security`

```bash
# User commands
useradd username     # Create user
usermod -a -G group user # Add to group
userdel username     # Delete user
passwd username      # Change password

# Group commands
groupadd group       # Create group
groupdel group       # Delete group
groups username      # Show user groups
id username         # Show user/group IDs

# Permission management
chmod 755 file       # Change permissions
chown user file      # Change owner
chgrp group file     # Change group
umask 022           # Set default permissions
```

## Package Management
###### tags: `packages`, `software`, `installation`, `updates`

```bash
# APT (Debian/Ubuntu)
apt update           # Update package list
apt upgrade          # Upgrade packages
apt install package  # Install package
apt remove package   # Remove package
apt search pattern   # Search packages

# YUM (RHEL/CentOS)
yum update           # Update packages
yum install package  # Install package
yum remove package   # Remove package
yum search pattern   # Search packages

# DNF (Fedora)
dnf update          # Update packages
dnf install package # Install package
dnf remove package  # Remove package
dnf search pattern  # Search packages
```

## See Also
- [Shell Scripting Fundamentals](scripting.md)
- [Advanced Script Patterns](advanced_patterns.md)
- [System Monitoring](monitoring.md)
