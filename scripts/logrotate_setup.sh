#!/bin/bash

# logrotate_setup.sh - Interactive logrotate configuration script
# Usage: ./logrotate_setup.sh /path/to/logs

set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Validate input
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/logs"
    exit 1
fi

LOG_PATH="$1"
if [ ! -d "$LOG_PATH" ]; then
    echo "Error: Directory $LOG_PATH does not exist"
    exit 1
fi

# Configuration variables
CONFIG_NAME=""
ROTATE_FREQ=""
ROTATE_COUNT=""
MAX_SIZE=""
COMPRESS=""
CREATE_MODE=""
CREATE_USER=""
CREATE_GROUP=""

# Interactive configuration
echo "=== Logrotate Configuration Setup ==="
echo

# Get configuration name
read -p "Enter configuration name (e.g., myapp): " CONFIG_NAME
if [ -z "$CONFIG_NAME" ]; then
    echo "Configuration name cannot be empty"
    exit 1
fi

# Rotation frequency
echo
echo "Select rotation frequency:"
echo "1) Daily"
echo "2) Weekly"
echo "3) Monthly"
read -p "Enter choice (1-3): " freq_choice

case $freq_choice in
    1) ROTATE_FREQ="daily";;
    2) ROTATE_FREQ="weekly";;
    3) ROTATE_FREQ="monthly";;
    *) echo "Invalid choice"; exit 1;;
esac

# Rotation count
read -p "Enter number of rotated logs to keep (default: 7): " ROTATE_COUNT
ROTATE_COUNT=${ROTATE_COUNT:-7}

# Max size
read -p "Enter max size before rotation (e.g., 100M, leave empty for no size limit): " MAX_SIZE

# Compression
read -p "Enable compression? (y/n, default: y): " compress_choice
case ${compress_choice:-y} in
    [Yy]*) COMPRESS="compress";;
    [Nn]*) COMPRESS="";;
    *) echo "Invalid choice"; exit 1;;
esac

# File creation settings
read -p "Enter file creation mode (e.g., 0640, default: 0644): " CREATE_MODE
CREATE_MODE=${CREATE_MODE:-0644}

read -p "Enter file owner (default: root): " CREATE_USER
CREATE_USER=${CREATE_USER:-root}

read -p "Enter file group (default: root): " CREATE_GROUP
CREATE_GROUP=${CREATE_GROUP:-root}

# Generate configuration
CONFIG_FILE="/etc/logrotate.d/$CONFIG_NAME"
echo "Generating configuration file: $CONFIG_FILE"

cat > "$CONFIG_FILE" << EOF
$LOG_PATH/*.log {
    $ROTATE_FREQ
    missingok
    rotate $ROTATE_COUNT
    notifempty
EOF

# Add optional configurations
[ ! -z "$MAX_SIZE" ] && echo "    size $MAX_SIZE" >> "$CONFIG_FILE"
[ ! -z "$COMPRESS" ] && echo "    compress" >> "$CONFIG_FILE"
echo "    create $CREATE_MODE $CREATE_USER $CREATE_GROUP" >> "$CONFIG_FILE"

# Close the configuration
echo "}" >> "$CONFIG_FILE"

echo
echo "Configuration complete!"
echo "Testing configuration..."
logrotate -d "$CONFIG_FILE"

echo
echo "Setup finished. Your logs will now be rotated according to the specified configuration."
echo "You can manually test the rotation with: logrotate -f $CONFIG_FILE"
