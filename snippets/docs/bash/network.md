# Network Management Scripts

## Table of Contents
- [Network Management Scripts](#network-management-scripts)
  - [Table of Contents](#table-of-contents)
          - [tags: network, firewall, monitoring, discovery, balancing, vpn, dns](#tags:-network,-firewall,-monitoring,-discovery,-balancing,-vpn,-dns)
  - [Interface Configuration](#interface-configuration)
          - [tags: interface, ip, network, configuration](#tags:-interface,-ip,-network,-configuration)
- [Network Interface Manager](#network-interface-manager)
- [!/bin/bash](#!/bin/bash)
- [Network Configuration Backup/Restore](#network-configuration-backup/restore)
- [DHCP Configuration](#dhcp-configuration)
- [Static IP Configuration](#static-ip-configuration)
  - [Firewall Management](#firewall-management)
          - [tags: firewall, iptables, security, rules](#tags:-firewall,-iptables,-security,-rules)
- [IPTables Firewall Manager](#iptables-firewall-manager)
- [!/bin/bash](#!/bin/bash)
- [Initialize firewall](#initialize-firewall)
- [Add service rules](#add-service-rules)
- [Rate limiting](#rate-limiting)
- [Port forwarding](#port-forwarding)
- [Block IP address](#block-ip-address)
- [Unblock IP address](#unblock-ip-address)
  - [Traffic Monitoring](#traffic-monitoring)
          - [tags: traffic, monitoring, bandwidth, analysis](#tags:-traffic,-monitoring,-bandwidth,-analysis)
- [Traffic Monitor](#traffic-monitor)
- [!/bin/bash](#!/bin/bash)
- [Bandwidth threshold monitoring](#bandwidth-threshold-monitoring)
- [Connection tracking](#connection-tracking)
  - [Service Discovery](#service-discovery)
          - [tags: discovery, services, ports, scanning](#tags:-discovery,-services,-ports,-scanning)
- [Service Discovery](#service-discovery)
- [!/bin/bash](#!/bin/bash)
- [Service registration](#service-registration)
- [Service health check](#service-health-check)
  - [Load Balancing](#load-balancing)
          - [tags: loadbalancer, haproxy, balancing](#tags:-loadbalancer,-haproxy,-balancing)
- [HAProxy Load Balancer Manager](#haproxy-load-balancer-manager)
- [!/bin/bash](#!/bin/bash)
- [Generate HAProxy configuration](#generate-haproxy-configuration)
- [Add backend server](#add-backend-server)
- [Remove backend server](#remove-backend-server)
- [Reload HAProxy](#reload-haproxy)
- [Check backend health](#check-backend-health)
  - [VPN Management](#vpn-management)
          - [tags: vpn, openvpn, tunnel](#tags:-vpn,-openvpn,-tunnel)
- [OpenVPN Manager](#openvpn-manager)
- [!/bin/bash](#!/bin/bash)
- [Start VPN connection](#start-vpn-connection)
- [Stop VPN connection](#stop-vpn-connection)
- [Monitor VPN connection](#monitor-vpn-connection)
  - [DNS Management](#dns-management)
          - [tags: dns, bind, domain](#tags:-dns,-bind,-domain)
- [DNS Zone Manager](#dns-zone-manager)
- [!/bin/bash](#!/bin/bash)
- [Update DNS record](#update-dns-record)
- [Add DNS zone](#add-dns-zone)
- [Check DNS propagation](#check-dns-propagation)
  - [See Also](#see-also)



###### tags: `network`, `firewall`, `monitoring`, `discovery`, `balancing`, `vpn`, `dns`

## Interface Configuration
###### tags: `interface`, `ip`, `network`, `configuration`

```bash
# Network Interface Manager
#!/bin/bash
interface="eth0"
log_file="/var/log/network_config.log"

configure_interface() {
    local ip_address="$1"
    local netmask="$2"
    local gateway="$3"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Configuring interface $interface..." >> "$log_file"
    
    # Backup current config
    cp /etc/network/interfaces "/etc/network/interfaces.$(date +%Y%m%d)"
    
    # Configure interface
    ip addr flush dev "$interface"
    ip addr add "$ip_address/$netmask" dev "$interface"
    ip link set "$interface" up
    ip route add default via "$gateway"
    
    # Verify configuration
    if ip addr show "$interface" | grep -q "$ip_address"; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Interface configuration successful" >> "$log_file"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Interface configuration failed" >> "$log_file"
        restore_network_config
    fi
}

# Network Configuration Backup/Restore
backup_network_config() {
    tar czf "/etc/network/backup_$(date +%Y%m%d).tar.gz" \
        /etc/network/interfaces \
        /etc/resolv.conf \
        /etc/hosts
}

restore_network_config() {
    local backup_file="$1"
    tar xzf "$backup_file" -C /
    systemctl restart networking
}

# DHCP Configuration
configure_dhcp() {
    cat > "/etc/network/interfaces.d/$interface" << EOF
auto $interface
iface $interface inet dhcp
EOF
    systemctl restart networking
}

# Static IP Configuration
configure_static() {
    local ip="$1"
    local netmask="$2"
    local gateway="$3"
    local dns="$4"
    
    cat > "/etc/network/interfaces.d/$interface" << EOF
auto $interface
iface $interface inet static
    address $ip
    netmask $netmask
    gateway $gateway
    dns-nameservers $dns
EOF
    systemctl restart networking
}
```

## Firewall Management
###### tags: `firewall`, `iptables`, `security`, `rules`

```bash
# IPTables Firewall Manager
#!/bin/bash
rules_file="/etc/iptables/rules.v4"
log_file="/var/log/firewall.log"

# Initialize firewall
init_firewall() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Initializing firewall..." >> "$log_file"
    
    # Flush existing rules
    iptables -F
    iptables -X
    iptables -t nat -F
    iptables -t nat -X
    iptables -t mangle -F
    iptables -t mangle -X
    
    # Set default policies
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT ACCEPT
    
    # Allow loopback
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A OUTPUT -o lo -j ACCEPT
    
    # Allow established connections
    iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    
    # Save rules
    iptables-save > "$rules_file"
}

# Add service rules
add_service_rules() {
    # SSH
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    
    # HTTP/HTTPS
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT
    
    # Save rules
    iptables-save > "$rules_file"
}

# Rate limiting
add_rate_limit() {
    local port="$1"
    local connections="$2"
    local seconds="$3"
    
    iptables -A INPUT -p tcp --dport "$port" -m state --state NEW \
        -m recent --set
    iptables -A INPUT -p tcp --dport "$port" -m state --state NEW \
        -m recent --update --seconds "$seconds" --hitcount "$connections" -j DROP
}

# Port forwarding
add_port_forward() {
    local external_port="$1"
    local internal_ip="$2"
    local internal_port="$3"
    
    iptables -t nat -A PREROUTING -p tcp --dport "$external_port" \
        -j DNAT --to-destination "$internal_ip:$internal_port"
    iptables -A FORWARD -p tcp -d "$internal_ip" --dport "$internal_port" -j ACCEPT
}

# Block IP address
block_ip() {
    local ip="$1"
    iptables -A INPUT -s "$ip" -j DROP
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Blocked IP: $ip" >> "$log_file"
}

# Unblock IP address
unblock_ip() {
    local ip="$1"
    iptables -D INPUT -s "$ip" -j DROP
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Unblocked IP: $ip" >> "$log_file"
}
```

## Traffic Monitoring
###### tags: `traffic`, `monitoring`, `bandwidth`, `analysis`

```bash
# Traffic Monitor
#!/bin/bash
interface="eth0"
log_file="/var/log/traffic.log"
interval=60

monitor_traffic() {
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
        
        # Log statistics
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] RX: $(( rx_rate / 1024 )) KB/s TX: $(( tx_rate / 1024 )) KB/s Connections: $total_conn" >> "$log_file"
        
        # Check thresholds
        check_bandwidth_threshold "$rx_rate" "$tx_rate"
    done
}

# Bandwidth threshold monitoring
check_bandwidth_threshold() {
    local rx_rate="$1"
    local tx_rate="$2"
    local threshold=$((100 * 1024 * 1024))  # 100 MB/s
    
    if [ "$rx_rate" -gt "$threshold" ] || [ "$tx_rate" -gt "$threshold" ]; then
        send_alert "High bandwidth usage detected"
    fi
}

# Connection tracking
track_connections() {
    echo "=== Connection Tracking $(date) ===" >> "$log_file"
    
    # Top source IPs
    echo "Top Source IPs:" >> "$log_file"
    netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head -n 10 >> "$log_file"
    
    # Top destination ports
    echo "Top Destination Ports:" >> "$log_file"
    netstat -ntu | awk '{print $4}' | cut -d: -f2 | sort | uniq -c | sort -nr | head -n 10 >> "$log_file"
}
```

## Service Discovery
###### tags: `discovery`, `services`, `ports`, `scanning`

```bash
# Service Discovery
#!/bin/bash
network="192.168.1.0/24"
ports="22,80,443,3306,5432"
output_file="/var/log/service_discovery.log"

discover_services() {
    echo "=== Service Discovery $(date) ===" > "$output_file"
    
    # Network scan
    nmap -sS -p "$ports" "$network" | \
        grep -E "^Nmap|^[0-9]|open" >> "$output_file"
    
    # Service verification
    while read -r host; do
        if nc -zv "$host" 80 2>&1 | grep -q "succeeded"; then
            echo "$host: HTTP service detected" >> "$output_file"
        fi
        
        if nc -zv "$host" 443 2>&1 | grep -q "succeeded"; then
            echo "$host: HTTPS service detected" >> "$output_file"
        fi
    done < <(grep "open" "$output_file" | awk '{print $2}')
}

# Service registration
register_service() {
    local service="$1"
    local port="$2"
    local description="$3"
    
    echo "$service:$port:$description" >> /etc/services.list
}

# Service health check
check_service() {
    local host="$1"
    local port="$2"
    
    if nc -z "$host" "$port" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}
```

## Load Balancing
###### tags: `loadbalancer`, `haproxy`, `balancing`

```bash
# HAProxy Load Balancer Manager
#!/bin/bash
haproxy_config="/etc/haproxy/haproxy.cfg"
backend_servers=()

# Generate HAProxy configuration
generate_config() {
    cat > "$haproxy_config" << EOF
global
    log /dev/log local0
    maxconn 4096
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    retries 3
    timeout connect 5000
    timeout client  50000
    timeout server  50000

frontend http-in
    bind *:80
    default_backend servers

backend servers
    balance roundrobin
EOF

    # Add backend servers
    for server in "${backend_servers[@]}"; do
        echo "    server ${server/:/ :}" >> "$haproxy_config"
    done
}

# Add backend server
add_server() {
    local name="$1"
    local address="$2"
    local port="$3"
    
    backend_servers+=("$name $address:$port check")
    generate_config
    reload_haproxy
}

# Remove backend server
remove_server() {
    local name="$1"
    
    for i in "${!backend_servers[@]}"; do
        if [[ ${backend_servers[i]} == "$name "* ]]; then
            unset 'backend_servers[i]'
            break
        fi
    done
    
    generate_config
    reload_haproxy
}

# Reload HAProxy
reload_haproxy() {
    systemctl reload haproxy
}

# Check backend health
check_backends() {
    for server in "${backend_servers[@]}"; do
        local host=${server#* }
        host=${host%:*}
        local port=${server#*:}
        port=${port%% *}
        
        if nc -z "$host" "$port" 2>/dev/null; then
            echo "$host:$port is UP"
        else
            echo "$host:$port is DOWN"
            send_alert "Backend server $host:$port is down"
        fi
    done
}
```

## VPN Management
###### tags: `vpn`, `openvpn`, `tunnel`

```bash
# OpenVPN Manager
#!/bin/bash
vpn_config="/etc/openvpn/client.conf"
vpn_log="/var/log/openvpn.log"

# Start VPN connection
start_vpn() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting VPN..." >> "$vpn_log"
    
    systemctl start openvpn@client
    sleep 5
    
    if ip addr show tun0 >/dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] VPN connection established" >> "$vpn_log"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] VPN connection failed" >> "$vpn_log"
        send_alert "VPN connection failed"
        return 1
    fi
}

# Stop VPN connection
stop_vpn() {
    systemctl stop openvpn@client
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] VPN stopped" >> "$vpn_log"
}

# Monitor VPN connection
monitor_vpn() {
    while true; do
        if ! ping -c 1 10.8.0.1 >/dev/null 2>&1; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] VPN connection lost" >> "$vpn_log"
            systemctl restart openvpn@client
        fi
        sleep 60
    done
}
```

## DNS Management
###### tags: `dns`, `bind`, `domain`

```bash
# DNS Zone Manager
#!/bin/bash
zone_file="/etc/bind/zones/example.com.db"
serial=$(date +%Y%m%d%H)

# Update DNS record
update_record() {
    local record="$1"
    local type="$2"
    local value="$3"
    
    # Update serial
    sed -i "s/[0-9]\{10\}/$serial/" "$zone_file"
    
    # Add/update record
    if grep -q "^$record" "$zone_file"; then
        sed -i "/^$record/c\\$record    IN    $type    $value" "$zone_file"
    else
        echo "$record    IN    $type    $value" >> "$zone_file"
    fi
    
    # Reload BIND
    rndc reload
}

# Add DNS zone
add_zone() {
    local domain="$1"
    local ns1="$2"
    local ns2="$3"
    
    # Create zone file
    cat > "/etc/bind/zones/$domain.db" << EOF
\$TTL    86400
@       IN      SOA     $ns1. admin.$domain. (
                        $serial         ; Serial
                        3600           ; Refresh
                        1800           ; Retry
                        604800         ; Expire
                        86400 )        ; Minimum TTL

@       IN      NS      $ns1.
@       IN      NS      $ns2.
EOF
    
    # Add zone to named.conf.local
    cat >> "/etc/bind/named.conf.local" << EOF
zone "$domain" {
    type master;
    file "/etc/bind/zones/$domain.db";
};
EOF
    
    # Reload BIND
    rndc reload
}

# Check DNS propagation
check_propagation() {
    local domain="$1"
    local record_type="$2"
    local expected_value="$3"
    
    # Check multiple DNS servers
    for server in "8.8.8.8" "1.1.1.1" "9.9.9.9"; do
        result=$(dig @"$server" "$domain" "$record_type" +short)
        echo "Server $server: $result"
        
        if [ "$result" != "$expected_value" ]; then
            echo "Warning: DNS not propagated to $server"
        fi
    done
}
```

## See Also
- [Basic Operations](basics.md)
- [System Monitoring](monitoring.md)
- [Security Auditing](security.md)
