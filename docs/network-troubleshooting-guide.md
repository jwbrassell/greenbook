# Network Troubleshooting Tools Guide

## Table of Contents
- [Network Troubleshooting Tools Guide](#network-troubleshooting-tools-guide)
  - [Table of Contents](#table-of-contents)
  - [For RHEL, Rocky Linux, and macOS](#for-rhel,-rocky-linux,-and-macos)
  - [Common Tools Across All Platforms](#common-tools-across-all-platforms)
    - [1. ping](#1-ping)
    - [2. traceroute](#2-traceroute)
    - [3. netstat](#3-netstat)
    - [4. ss](#4-ss)
  - [RHEL/Rocky Linux Specific Tools](#rhel/rocky-linux-specific-tools)
    - [1. nmcli](#1-nmcli)
    - [2. firewall-cmd](#2-firewall-cmd)
  - [macOS Specific Tools](#macos-specific-tools)
    - [1. networksetup](#1-networksetup)
    - [2. airport](#2-airport)
  - [Advanced Tools (All Platforms)](#advanced-tools-all-platforms)
    - [1. tcpdump](#1-tcpdump)
    - [2. nmap](#2-nmap)
    - [3. dig](#3-dig)
  - [Best Practices](#best-practices)
  - [Common Troubleshooting Scenarios](#common-troubleshooting-scenarios)


## For RHEL, Rocky Linux, and macOS

This guide covers common network troubleshooting tools available on RHEL-based systems (RHEL/Rocky Linux) and macOS, along with their usage and key options.

## Common Tools Across All Platforms

### 1. ping
Tests connectivity to a host by sending ICMP echo requests.

**Basic Usage:**
```bash
ping google.com
ping -c 4 8.8.8.8  # Send only 4 packets
```

**Key Options:**
- `-c count`: Number of packets to send
- `-i interval`: Interval between packets (in seconds)
- `-s size`: Size of packets to send
- `-t ttl`: Set Time To Live
- `-W timeout`: Time to wait for response

### 2. traceroute
Shows the path packets take to reach a destination.

**Basic Usage:**
```bash
traceroute google.com
traceroute -n 8.8.8.8  # Don't resolve hostnames
```

**Key Options:**
- `-n`: Don't resolve hostnames
- `-w timeout`: Wait time for response
- `-q queries`: Number of queries per hop
- `-m max_ttl`: Maximum number of hops
- `-p port`: Specify port number

### 3. netstat
Displays network connections, routing tables, and interface statistics.

**Basic Usage:**
```bash
netstat -an  # Show all connections numerically
netstat -rn  # Show routing table numerically
```

**Key Options:**
- `-a`: Show all sockets
- `-n`: Show numerical addresses
- `-p`: Show processes
- `-r`: Show routing table
- `-t`: Show TCP connections
- `-u`: Show UDP connections

### 4. ss
Modern replacement for netstat, shows socket statistics.

**Basic Usage:**
```bash
ss -tuln  # Show TCP and UDP listening sockets
ss -ta    # Show all TCP sockets
```

**Key Options:**
- `-t`: Show TCP sockets
- `-u`: Show UDP sockets
- `-l`: Show listening sockets
- `-n`: Don't resolve service names
- `-p`: Show processes using sockets
- `-i`: Show internal TCP information

## RHEL/Rocky Linux Specific Tools

### 1. nmcli
NetworkManager command-line interface.

**Basic Usage:**
```bash
nmcli device status
nmcli connection show
```

**Key Options:**
- `device`: Manage network interfaces
- `connection`: Manage network connections
- `general`: General NetworkManager status
- `radio`: Manage radio switches
- `monitor`: Monitor NetworkManager changes

### 2. firewall-cmd
Firewall management tool.

**Basic Usage:**
```bash
firewall-cmd --state
firewall-cmd --list-all
```

**Key Options:**
- `--state`: Check firewall state
- `--list-all`: List all firewall rules
- `--add-port=port/protocol`: Add port
- `--remove-port=port/protocol`: Remove port
- `--reload`: Reload firewall configuration

## macOS Specific Tools

### 1. networksetup
Configure network settings.

**Basic Usage:**
```bash
networksetup -listallnetworkservices
networksetup -getinfo "Wi-Fi"
```

**Key Options:**
- `-listallnetworkservices`: List all network services
- `-getinfo`: Get network service information
- `-setdnsservers`: Set DNS servers
- `-getdnsservers`: Get DNS servers
- `-setairportpower`: Enable/disable Wi-Fi

### 2. airport
Wi-Fi diagnostic tool (located at /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport).

**Basic Usage:**
```bash
airport -I  # Show current Wi-Fi information
airport -s  # Scan for available networks
```

**Key Options:**
- `-I`: Show current Wi-Fi information
- `-s`: Scan for networks
- `-z`: Disconnect from current network
- `-x`: Remove remembered networks

## Advanced Tools (All Platforms)

### 1. tcpdump
Packet analyzer tool.

**Basic Usage:**
```bash
tcpdump -i any
tcpdump -i eth0 port 80
```

**Key Options:**
- `-i interface`: Specify interface
- `-n`: Don't resolve hostnames
- `-v`: Verbose output
- `-w file`: Write to file
- `-r file`: Read from file

### 2. nmap
Network exploration and security scanning.

**Basic Usage:**
```bash
nmap localhost
nmap -p 80,443 example.com
```

**Key Options:**
- `-p ports`: Specify ports to scan
- `-sS`: TCP SYN scan
- `-sU`: UDP scan
- `-A`: Aggressive scan
- `-v`: Verbose output

### 3. dig
DNS lookup utility.

**Basic Usage:**
```bash
dig google.com
dig +short google.com
```

**Key Options:**
- `+short`: Short form answer
- `+trace`: Trace DNS resolution
- `-t type`: Specify record type
- `+noall`: Turn off all display flags
- `+answer`: Show answer section only

## Best Practices

1. Always start with basic connectivity tests (ping) before moving to more complex tools
2. Use `-v` (verbose) options when you need more detailed information
3. Save output to files for complex troubleshooting sessions
4. Be cautious with tools like nmap on networks you don't own/manage
5. Consider security implications when using these tools in production environments

## Common Troubleshooting Scenarios

1. **Connectivity Issues:**
   ```bash
   ping gateway_ip
   traceroute problematic_host
   ```

2. **DNS Problems:**
   ```bash
   dig domain_name
   nslookup domain_name
   ```

3. **Port/Service Issues:**
   ```bash
   ss -tuln | grep port_number
   netstat -an | grep port_number
   ```

4. **Network Performance:**
   ```bash
   mtr destination_host
   iperf3 -c server_ip
   ```

Remember to check system logs (/var/log/messages, /var/log/syslog, or journalctl) alongside these tools for comprehensive troubleshooting.
