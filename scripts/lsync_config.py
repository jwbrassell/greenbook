#!/usr/bin/env python3

"""
lsync_config.py - Interactive lsync configuration script
Usage: python3 lsync_config.py /path/to/source
"""

import argparse
import os
import sys
import pwd
import grp
from pathlib import Path
import subprocess

def check_lsync_installed():
    """Check if lsync is installed on the system."""
    try:
        subprocess.run(['which', 'lsyncd'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_user_input(prompt, default=None):
    """Get user input with optional default value."""
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    return input(f"{prompt}: ").strip()

def validate_path(path):
    """Validate if path exists and is accessible."""
    path_obj = Path(path)
    if not path_obj.exists():
        raise ValueError(f"Path does not exist: {path}")
    if not os.access(path, os.R_OK):
        raise ValueError(f"Path is not readable: {path}")
    return path_obj.resolve()

def create_lsync_config(source_path, target_path, sync_delay=1, exclude_patterns=None):
    """Create lsync configuration file."""
    if exclude_patterns is None:
        exclude_patterns = []
    
    config_dir = Path('/etc/lsyncd')
    config_file = config_dir / 'lsyncd.conf.lua'
    
    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Basic configuration template
    config_content = f'''
-- Lsyncd configuration file
settings {{
    logfile = "/var/log/lsyncd/lsyncd.log",
    statusFile = "/var/log/lsyncd/lsyncd-status.log",
    statusInterval = 20,
    maxProcesses = 1,
}}

-- Sync configuration
sync {{
    default.rsync,
    source = "{source_path}",
    target = "{target_path}",
    delay = {sync_delay},
    rsync = {{
        binary = "/usr/bin/rsync",
        archive = true,
        compress = true,
        verbose = true,
'''
    
    # Add exclude patterns if specified
    if exclude_patterns:
        config_content += '        exclude = {\n'
        for pattern in exclude_patterns:
            config_content += f'            "{pattern}",\n'
        config_content += '        },\n'
    
    config_content += '''
    }
}
'''
    
    # Write configuration file
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    # Set appropriate permissions
    os.chmod(config_file, 0o644)
    
    return config_file

def setup_systemd_service():
    """Create and enable systemd service for lsyncd."""
    service_content = '''[Unit]
Description=Live Syncing (Mirror) Daemon
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/lsyncd /etc/lsyncd/lsyncd.conf.lua
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
'''
    
    service_file = '/etc/systemd/system/lsyncd.service'
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    # Set appropriate permissions
    os.chmod(service_file, 0o644)
    
    # Reload systemd and enable service
    subprocess.run(['systemctl', 'daemon-reload'], check=True)
    subprocess.run(['systemctl', 'enable', 'lsyncd'], check=True)

def main():
    parser = argparse.ArgumentParser(description='Configure lsyncd for directory synchronization')
    parser.add_argument('source_path', help='Source directory path to sync from')
    args = parser.parse_args()

    # Check if running as root
    if os.geteuid() != 0:
        sys.exit("This script must be run as root")

    # Check if lsync is installed
    if not check_lsync_installed():
        sys.exit("lsyncd is not installed. Please install it first.")

    try:
        # Validate source path
        source_path = validate_path(args.source_path)
        
        print("\n=== Lsync Configuration Setup ===\n")
        
        # Get target path
        target_path = get_user_input("Enter target directory path")
        try:
            validate_path(target_path)
        except ValueError:
            create = get_user_input(f"Target path {target_path} doesn't exist. Create it? (y/n)", "y")
            if create.lower() == 'y':
                Path(target_path).mkdir(parents=True)
            else:
                sys.exit("Target path must exist to continue")
        
        # Get sync delay
        sync_delay = int(get_user_input("Enter sync delay in seconds", "1"))
        
        # Get exclude patterns
        exclude_patterns = []
        while True:
            pattern = get_user_input("Enter exclude pattern (or press Enter to finish)")
            if not pattern:
                break
            exclude_patterns.append(pattern)
        
        # Create configuration
        config_file = create_lsync_config(
            source_path,
            target_path,
            sync_delay,
            exclude_patterns
        )
        
        # Setup systemd service
        setup_systemd_service()
        
        print("\nConfiguration complete!")
        print(f"Configuration file created at: {config_file}")
        print("\nTo start syncing:")
        print("1. Review the configuration file if needed")
        print("2. Start the service: systemctl start lsyncd")
        print("3. Check status: systemctl status lsyncd")
        print("4. View logs: tail -f /var/log/lsyncd/lsyncd.log")

    except Exception as e:
        sys.exit(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
