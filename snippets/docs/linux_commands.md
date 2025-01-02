# Linux System Administration Commands Reference

###### tags: `linux`, `system`, `admin`, `server`, `configuration`, `management`, `security`, `monitoring`

## Table of Contents
- [Linux System Administration Commands Reference](#linux-system-administration-commands-reference)
          - [tags: linux, system, admin, server, configuration, management, security, monitoring](#tags:-linux,-system,-admin,-server,-configuration,-management,-security,-monitoring)
  - [Table of Contents](#table-of-contents)
  - [System Information](#system-information)
          - [tags: system, info, configuration, kernel, os](#tags:-system,-info,-configuration,-kernel,-os)
- [System and OS](#system-and-os)
- [Hardware Resources](#hardware-resources)
- [System Uptime and Load](#system-uptime-and-load)
  - [Hardware Information](#hardware-information)
          - [tags: hardware, devices, drivers, memory, cpu](#tags:-hardware,-devices,-drivers,-memory,-cpu)
- [CPU Information](#cpu-information)
- [Memory Information](#memory-information)
- [Storage Information](#storage-information)
- [Hardware Monitoring](#hardware-monitoring)
  - [Performance Monitoring](#performance-monitoring)
          - [tags: monitoring, performance, resources, troubleshooting](#tags:-monitoring,-performance,-resources,-troubleshooting)
- [Process Monitoring](#process-monitoring)
- [Resource Usage](#resource-usage)
- [Network Monitoring](#network-monitoring)
- [Performance Analysis](#performance-analysis)
  - [Disk Management](#disk-management)
          - [tags: disk, storage, filesystem, partitions, mount](#tags:-disk,-storage,-filesystem,-partitions,-mount)
- [Disk Partitioning](#disk-partitioning)
- [Filesystem Operations](#filesystem-operations)
- [Disk Usage](#disk-usage)
- [LVM Management](#lvm-management)
  - [Network Administration](#network-administration)
          - [tags: network, connectivity, firewall, routing, dns](#tags:-network,-connectivity,-firewall,-routing,-dns)
- [Network Configuration](#network-configuration)
- [Network Diagnostics](#network-diagnostics)
- [Firewall Management](#firewall-management)
- [Network Monitoring](#network-monitoring)
  - [Service Management](#service-management)
          - [tags: services, systemd, daemons, processes](#tags:-services,-systemd,-daemons,-processes)
- [Systemd Services](#systemd-services)
- [Service Logs](#service-logs)
- [Process Management](#process-management)
  - [User Administration](#user-administration)
          - [tags: users, groups, permissions, accounts](#tags:-users,-groups,-permissions,-accounts)
- [User Management](#user-management)
- [Group Management](#group-management)
- [Account Information](#account-information)
  - [Security and Permissions](#security-and-permissions)
          - [tags: security, permissions, access, encryption](#tags:-security,-permissions,-access,-encryption)
- [File Permissions](#file-permissions)
- [Security Tools](#security-tools)
- [Encryption](#encryption)
  - [Log Management](#log-management)
          - [tags: logs, monitoring, troubleshooting, analysis](#tags:-logs,-monitoring,-troubleshooting,-analysis)
- [System Logs](#system-logs)
- [Log Analysis](#log-analysis)
- [Log Rotation](#log-rotation)
  - [Backup and Recovery](#backup-and-recovery)
          - [tags: backup, recovery, restore, archive](#tags:-backup,-recovery,-restore,-archive)
- [Backup Commands](#backup-commands)
- [Recovery Tools](#recovery-tools)
  - [System Maintenance](#system-maintenance)
          - [tags: maintenance, updates, cleanup, optimization](#tags:-maintenance,-updates,-cleanup,-optimization)
- [System Updates](#system-updates)
- [System Cleanup](#system-cleanup)
- [System Optimization](#system-optimization)
  - [Container Management](#container-management)
          - [tags: docker, kubernetes, containers, orchestration, microservices](#tags:-docker,-kubernetes,-containers,-orchestration,-microservices)
- [Docker Basic Commands](#docker-basic-commands)
- [Docker Container Management](#docker-container-management)
- [Docker Compose](#docker-compose)
- [Kubernetes Basic Commands](#kubernetes-basic-commands)
- [Kubernetes Management](#kubernetes-management)
- [Container Networking](#container-networking)
  - [Advanced Networking](#advanced-networking)
          - [tags: networking, vpn, firewall, routing, traffic, security](#tags:-networking,-vpn,-firewall,-routing,-traffic,-security)
  - [System Hardening](#system-hardening)
          - [tags: security, hardening, compliance, audit, protection](#tags:-security,-hardening,-compliance,-audit,-protection)
- [Security Auditing](#security-auditing)
- [Access Control](#access-control)
- [Service Hardening](#service-hardening)
- [Password Policies](#password-policies)
- [File Security](#file-security)
- [Network Hardening](#network-hardening)
  - [Performance Tuning](#performance-tuning)
          - [tags: performance, optimization, tuning, profiling, monitoring](#tags:-performance,-optimization,-tuning,-profiling,-monitoring)
  - [Advanced Storage](#advanced-storage)
          - [tags: storage, lvm, raid, zfs, filesystem, backup](#tags:-storage,-lvm,-raid,-zfs,-filesystem,-backup)
- [LVM Operations](#lvm-operations)
- [LVM Management](#lvm-management)
- [RAID Management](#raid-management)
- [ZFS Management](#zfs-management)
- [ZFS Properties](#zfs-properties)
- [Advanced Filesystem](#advanced-filesystem)
  - [Virtualization](#virtualization)
          - [tags: virtualization, kvm, qemu, libvirt, containers, hypervisor](#tags:-virtualization,-kvm,-qemu,-libvirt,-containers,-hypervisor)
  - [Monitoring Systems](#monitoring-systems)
          - [tags: monitoring, alerting, metrics, prometheus, grafana, nagios, zabbix](#tags:-monitoring,-alerting,-metrics,-prometheus,-grafana,-nagios,-zabbix)
  - [High Availability](#high-availability)
          - [tags: ha, clustering, failover, load-balancing, replication, redundancy](#tags:-ha,-clustering,-failover,-load-balancing,-replication,-redundancy)
  - [Infrastructure Automation](#infrastructure-automation)
          - [tags: automation, infrastructure, configuration, provisioning, orchestration, iac](#tags:-automation,-infrastructure,-configuration,-provisioning,-orchestration,-iac)
  - [Cloud Integration](#cloud-integration)
          - [tags: cloud, aws, gcp, azure, iam, security](#tags:-cloud,-aws,-gcp,-azure,-iam,-security)
- [AWS CLI Basic Operations](#aws-cli-basic-operations)
- [AWS EC2 Management](#aws-ec2-management)
- [AWS S3 Operations](#aws-s3-operations)
- [AWS RDS Management](#aws-rds-management)
- [GCP CLI Basic Operations](#gcp-cli-basic-operations)
- [GCP Compute Engine](#gcp-compute-engine)
- [GCP Storage Operations](#gcp-storage-operations)
- [GCP Cloud SQL](#gcp-cloud-sql)
- [Azure CLI Basic Operations](#azure-cli-basic-operations)
- [Azure VM Management](#azure-vm-management)
- [Azure Storage Operations](#azure-storage-operations)
- [Azure Database](#azure-database)
- [Cloud Security](#cloud-security)
- [AWS IAM](#aws-iam)
- [GCP IAM](#gcp-iam)
- [Azure IAM](#azure-iam)
- [Cross-Cloud Management](#cross-cloud-management)
- [Infrastructure](#infrastructure)
- [Monitoring](#monitoring)
- [Cost Management](#cost-management)
- [Ansible Commands](#ansible-commands)
- [Ansible Playbook Operations](#ansible-playbook-operations)
- [Puppet Commands](#puppet-commands)
- [Puppet Development](#puppet-development)
- [Chef Commands](#chef-commands)
- [Chef Development](#chef-development)
- [Terraform Commands](#terraform-commands)
- [Terraform State Management](#terraform-state-management)
- [SaltStack Commands](#saltstack-commands)
- [SaltStack State Management](#saltstack-state-management)
- [Version Control Integration](#version-control-integration)
- [Git](#git)
- [CI/CD Integration](#ci/cd-integration)
- [Jenkins](#jenkins)
- [Testing Tools](#testing-tools)
- [Molecule](#molecule)
- [InSpec](#inspec)
- [Pacemaker Cluster Management](#pacemaker-cluster-management)
- [Corosync Configuration](#corosync-configuration)
- [HAProxy Load Balancing](#haproxy-load-balancing)
- [Keepalived VRRP](#keepalived-vrrp)
- [Database Replication](#database-replication)
- [MySQL/MariaDB](#mysql/mariadb)
- [PostgreSQL](#postgresql)
- [Redis Replication](#redis-replication)
- [Distributed Storage](#distributed-storage)
- [GlusterFS](#glusterfs)
- [Ceph](#ceph)
- [Service Discovery](#service-discovery)
- [Consul](#consul)
- [etcd](#etcd)
- [Cluster Monitoring](#cluster-monitoring)
- [Failover Testing](#failover-testing)
- [Prometheus Management](#prometheus-management)
- [Prometheus Query](#prometheus-query)
- [Grafana CLI](#grafana-cli)
- [Grafana Management](#grafana-management)
- [Nagios Core](#nagios-core)
- [Nagios Configuration](#nagios-configuration)
- [Zabbix Server](#zabbix-server)
- [Zabbix Agent](#zabbix-agent)
- [Monitoring Tools](#monitoring-tools)
- [Alert Management](#alert-management)
- [Metric Collection](#metric-collection)
- [Visualization](#visualization)
- [KVM Management](#kvm-management)
- [VM Creation](#vm-creation)
- [VM Resources](#vm-resources)
- [Storage Management](#storage-management)
- [Network Management](#network-management)
- [VM Snapshots](#vm-snapshots)
  - [Performance Tuning](#performance-tuning)
          - [tags: performance, optimization, tuning, profiling, monitoring](#tags:-performance,-optimization,-tuning,-profiling,-monitoring)
- [CPU Tuning](#cpu-tuning)
- [Memory Optimization](#memory-optimization)
- [Disk I/O Tuning](#disk-i/o-tuning)
- [Network Performance](#network-performance)
- [Process Optimization](#process-optimization)
- [Database Tuning](#database-tuning)
  - [Advanced Networking](#advanced-networking)
          - [tags: networking, vpn, firewall, routing, traffic, security](#tags:-networking,-vpn,-firewall,-routing,-traffic,-security)
- [VPN Management](#vpn-management)
- [Advanced Firewall](#advanced-firewall)
- [Traffic Control](#traffic-control)
- [Advanced Routing](#advanced-routing)
- [Network Monitoring](#network-monitoring)
- [Load Balancing](#load-balancing)
  - [Useful One-liners](#useful-one-liners)
          - [tags: oneliners, scripts, automation](#tags:-oneliners,-scripts,-automation)
- [Find large files/directories](#find-large-files/directories)
- [Monitor system resources](#monitor-system-resources)
- [Kill processes by pattern](#kill-processes-by-pattern)
- [System backup](#system-backup)
- [Monitor failed SSH attempts](#monitor-failed-ssh-attempts)
- [Check disk IO](#check-disk-io)
- [Find files modified in last 24h](#find-files-modified-in-last-24h)
- [System load average graph](#system-load-average-graph)

## System Information
###### tags: `system`, `info`, `configuration`, `kernel`, `os`

```bash
# System and OS
uname -a                # All system info
cat /etc/os-release    # OS version info
lsb_release -a         # Distribution info
hostnamectl            # System hostname info
timedatectl           # System time info

# Hardware Resources
lscpu                  # CPU information
free -h                # Memory usage
df -h                  # Disk usage
lsblk                  # Block devices
lspci                  # PCI devices
lsusb                  # USB devices
dmidecode              # Hardware info

# System Uptime and Load
uptime                 # System uptime and load
w                      # Who is logged in
last                   # Login history
dmesg                  # Kernel messages
journalctl            # System logs
```

## Hardware Information
###### tags: `hardware`, `devices`, `drivers`, `memory`, `cpu`

```bash
# CPU Information
cat /proc/cpuinfo      # CPU details
lscpu                  # CPU architecture
mpstat                 # CPU statistics
top                    # CPU usage

# Memory Information
free -h                # Memory usage
vmstat                 # Virtual memory stats
cat /proc/meminfo      # Memory details
swapon --show         # Swap usage

# Storage Information
fdisk -l               # Disk partitions
parted -l              # Partition info
smartctl -a /dev/sda   # Disk health
hdparm -i /dev/sda     # Disk parameters

# Hardware Monitoring
sensors                # Temperature sensors
lm-sensors             # Hardware monitoring
acpi -V                # Battery info
```

## Performance Monitoring
###### tags: `monitoring`, `performance`, `resources`, `troubleshooting`

```bash
# Process Monitoring
top                    # System monitor
htop                   # Enhanced monitor
ps aux                 # Process list
pstree                 # Process tree
strace command        # Trace system calls

# Resource Usage
iostat                 # IO statistics
iotop                  # IO monitor
sar                    # System activity
vmstat                 # Virtual memory
pidstat                # Process stats

# Network Monitoring
nethogs                # Network process monitor
iftop                  # Network monitor
netstat               # Network statistics
ss                    # Socket statistics
iptraf                # Network monitor

# Performance Analysis
perf stat command     # Performance stats
perf record command   # Record performance
perf report           # Show performance report
```

## Disk Management
###### tags: `disk`, `storage`, `filesystem`, `partitions`, `mount`

```bash
# Disk Partitioning
fdisk /dev/sda         # Partition editor
gdisk /dev/sda         # GPT partition editor
parted /dev/sda        # Partition manager
gparted                # GUI partition editor

# Filesystem Operations
mkfs.ext4 /dev/sda1    # Create filesystem
mount /dev/sda1 /mnt   # Mount filesystem
umount /mnt            # Unmount filesystem
fsck /dev/sda1         # Check filesystem

# Disk Usage
du -sh directory       # Directory size
df -h                  # Disk usage
ncdu                   # Disk usage analyzer
iotop                  # IO monitor

# LVM Management
pvcreate /dev/sda1     # Create physical volume
vgcreate vg0 /dev/sda1 # Create volume group
lvcreate -L 10G vg0    # Create logical volume
lvextend -L +5G /dev/vg0/lv0 # Extend volume
```

## Network Administration
###### tags: `network`, `connectivity`, `firewall`, `routing`, `dns`

```bash
# Network Configuration
ip addr                # IP addresses
ip link               # Network interfaces
ip route              # Routing table
nmcli                 # Network manager
nmtui                 # Network manager TUI

# Network Diagnostics
ping host             # Test connectivity
traceroute host       # Trace route
mtr host              # Network diagnostic
dig domain            # DNS lookup
nslookup domain       # Name resolution

# Firewall Management
iptables -L           # List rules
ufw status            # UFW status
firewall-cmd --list-all # firewalld rules
nft list ruleset      # nftables rules

# Network Monitoring
tcpdump               # Packet capture
wireshark             # Packet analyzer
nmap                  # Port scanner
netstat -tuln         # Open ports
ss -tuln              # Socket statistics
```

## Service Management
###### tags: `services`, `systemd`, `daemons`, `processes`

```bash
# Systemd Services
systemctl status service    # Service status
systemctl start service    # Start service
systemctl stop service     # Stop service
systemctl restart service  # Restart service
systemctl enable service   # Enable at boot
systemctl disable service  # Disable at boot

# Service Logs
journalctl -u service     # Service logs
journalctl -f            # Follow logs
journalctl --since today  # Today's logs
systemctl list-units     # List services

# Process Management
service apache2 status    # Service status
update-rc.d service enable # Enable service
update-rc.d service disable # Disable service
chkconfig service on     # Enable service
chkconfig service off    # Disable service
```

## User Administration
###### tags: `users`, `groups`, `permissions`, `accounts`

```bash
# User Management
useradd username         # Create user
usermod -aG group user   # Add to group
userdel username         # Delete user
passwd username          # Set password

# Group Management
groupadd groupname       # Create group
groupdel groupname       # Delete group
gpasswd -a user group   # Add user to group
gpasswd -d user group   # Remove from group

# Account Information
id username             # User/group IDs
who                     # Logged in users
w                       # Who is logged in
last                    # Login history
ac                      # Connect time
```

## Security and Permissions
###### tags: `security`, `permissions`, `access`, `encryption`

```bash
# File Permissions
chmod 755 file          # Change mode
chown user:group file   # Change owner
chattr +i file          # Make immutable
lsattr file            # List attributes
getfacl file           # ACL permissions
setfacl -m u:user:rwx file # Set ACL

# Security Tools
fail2ban-client status # Fail2ban status
auditctl -l            # Audit rules
ausearch -k keyword    # Audit search
semanage               # SELinux management
getenforce            # SELinux status

# Encryption
openssl enc -aes-256-cbc # Encrypt file
gpg -c file            # Encrypt file
gpg -d file.gpg        # Decrypt file
ssh-keygen            # Generate SSH key
ssh-copy-id user@host # Copy SSH key
```

## Log Management
###### tags: `logs`, `monitoring`, `troubleshooting`, `analysis`

```bash
# System Logs
tail -f /var/log/syslog # Follow syslog
grep pattern /var/log/auth.log # Auth logs
less /var/log/messages # System messages
journalctl            # Systemd logs
dmesg                 # Kernel ring buffer

# Log Analysis
logwatch              # Log analyzer
fail2ban-client status # Security log
lastlog               # Last logins
aureport              # Audit reports
sa                    # Process accounting

# Log Rotation
logrotate -f /etc/logrotate.conf # Force rotation
cat /etc/logrotate.d/apache2 # Apache rotation
```

## Backup and Recovery
###### tags: `backup`, `recovery`, `restore`, `archive`

```bash
# Backup Commands
tar -czf backup.tar.gz directory/ # Create backup
rsync -av source/ dest/  # Sync files
dd if=/dev/sda of=disk.img # Disk image
dump -0uf /backup /dev/sda1 # Filesystem backup

# Recovery Tools
restore -if /backup     # Restore dump
fsck /dev/sda1         # Check filesystem
testdisk               # Data recovery
photorec               # File recovery
```

## System Maintenance
###### tags: `maintenance`, `updates`, `cleanup`, `optimization`

```bash
# System Updates
apt update && apt upgrade # Debian/Ubuntu
yum update              # RHEL/CentOS
dnf update              # Fedora
zypper update           # openSUSE

# System Cleanup
apt autoremove          # Remove unused
apt clean               # Clean cache
yum clean all           # Clean cache
journalctl --vacuum-size=500M # Clean logs

# System Optimization
nice -n 19 command     # Set priority
ionice -c2 -n7 command # IO priority
sysctl -w param=value  # Kernel parameter
ulimit -n 65535        # File limits
```

## Container Management
###### tags: `docker`, `kubernetes`, `containers`, `orchestration`, `microservices`

```bash
# Docker Basic Commands
docker ps                # List running containers
docker ps -a            # List all containers
docker images           # List images
docker pull image       # Pull image from registry
docker run image        # Run container
docker stop container   # Stop container
docker rm container     # Remove container
docker rmi image        # Remove image

# Docker Container Management
docker run -d -p 80:80 nginx     # Run nginx in background
docker exec -it container bash    # Enter container shell
docker logs container            # View container logs
docker inspect container         # Container details
docker stats                     # Container resource usage
docker cp file container:/path   # Copy to container
docker commit container image    # Create image from container

# Docker Compose
docker-compose up -d            # Start services
docker-compose down            # Stop services
docker-compose ps              # List services
docker-compose logs           # View service logs
docker-compose build          # Build services
docker-compose restart        # Restart services

# Kubernetes Basic Commands
kubectl get pods              # List pods
kubectl get nodes            # List nodes
kubectl get services         # List services
kubectl get deployments      # List deployments
kubectl describe pod name    # Pod details
kubectl logs pod             # Pod logs
kubectl exec -it pod bash    # Enter pod shell

# Kubernetes Management
kubectl apply -f file.yaml   # Apply configuration
kubectl delete -f file.yaml  # Delete resources
kubectl scale deployment name --replicas=3  # Scale
kubectl rollout status deployment/name     # Check rollout
kubectl port-forward pod 8080:80          # Port forward
kubectl top pods                          # Resource usage

# Container Networking
docker network ls            # List networks
docker network create net    # Create network
docker network connect net container  # Connect
kubectl get networkpolicies  # List network policies
kubectl port-forward        # Port forwarding
```

## Advanced Networking
###### tags: `networking`, `vpn`, `firewall`, `routing`, `traffic`, `security`

[Previous content remains unchanged...]

## System Hardening
###### tags: `security`, `hardening`, `compliance`, `audit`, `protection`

```bash
# Security Auditing
lynis audit system           # System security audit
tiger                       # Security audit tool
rkhunter --check           # Rootkit detection
chkrootkit                 # Another rootkit checker
aide --check               # File integrity check
tripwire --check          # File integrity monitor

# Access Control
sestatus                   # SELinux status
setenforce 1              # Enable SELinux
apparmor_status           # AppArmor status
aa-enforce /etc/apparmor.d/profile  # Enforce profile
pam-auth-update           # Configure PAM
authselect current        # Show auth config

# Service Hardening
sshd -T                   # Show SSH config
ss -tulpn                 # Show listening ports
lsof -i                   # List open files
systemctl mask service    # Disable service
systemctl list-dependencies # Show dependencies
needrestart              # Check service restarts

# Password Policies
pwck -r                   # Check password files
grpck -r                  # Check group files
chage -l user            # Password aging info
pam_tally2 --user=user   # Login attempts
pwscore                  # Check password strength
pwgen -s 20              # Generate strong password

# File Security
find / -perm -4000       # Find SUID files
find / -perm -2000       # Find SGID files
find / -perm -1000       # Find sticky bit
lsattr -a                # List file attributes
getcap file             # Show capabilities
setcap cap_net_bind_service+ep file # Set capabilities

# Network Hardening
ufw default deny         # Default deny
iptables-save > rules   # Backup rules
fail2ban-client status  # Show jail status
crowdsec status        # Show CrowdSec status
sysctl -a | grep net.ipv4.conf # Show network params
netstat -tapn          # Show network connections
```

## Performance Tuning
###### tags: `performance`, `optimization`, `tuning`, `profiling`, `monitoring`

[Previous content remains unchanged...]

## Advanced Storage
###### tags: `storage`, `lvm`, `raid`, `zfs`, `filesystem`, `backup`

```bash
# LVM Operations
pvdisplay                # Show physical volumes
vgdisplay                # Show volume groups
lvdisplay                # Show logical volumes
pvs                      # PV summary
vgs                      # VG summary
lvs                      # LV summary

# LVM Management
pvcreate /dev/sdb        # Create PV
vgcreate vg0 /dev/sdb    # Create VG
lvcreate -L 10G vg0      # Create LV
lvextend -l +100%FREE vg0/lv0  # Extend LV
pvmove /dev/sdb1         # Move PV data
vgreduce vg0 /dev/sdb    # Remove PV from VG

# RAID Management
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sd[bc]1  # Create RAID1
mdadm --detail /dev/md0  # RAID details
mdadm --manage /dev/md0 --add /dev/sdd1  # Add disk
mdadm --manage /dev/md0 --remove /dev/sdb1  # Remove disk
cat /proc/mdstat         # RAID status
mdadm --assemble --scan  # Assemble arrays

# ZFS Management
zpool status            # Pool status
zpool list              # List pools
zfs list                # List filesystems
zpool create tank mirror sdb sdc  # Create mirror
zfs snapshot tank@snap  # Create snapshot
zfs send tank@snap | zfs receive backup/tank  # Backup

# ZFS Properties
zfs get all tank        # Show properties
zfs set compression=lz4 tank  # Set compression
zfs set quota=100G tank # Set quota
zpool scrub tank        # Check integrity
zpool add tank cache sdd # Add cache device
zfs rollback tank@snap  # Restore snapshot

# Advanced Filesystem
xfs_info /dev/sda1      # XFS info
xfs_repair /dev/sda1    # Repair XFS
btrfs fi show          # BTRFS info
btrfs balance start /   # Balance BTRFS
tune2fs -l /dev/sda1    # Ext4 info
resize2fs /dev/sda1     # Resize Ext4
```

## Virtualization
###### tags: `virtualization`, `kvm`, `qemu`, `libvirt`, `containers`, `hypervisor`

[Previous content remains unchanged...]

## Monitoring Systems
###### tags: `monitoring`, `alerting`, `metrics`, `prometheus`, `grafana`, `nagios`, `zabbix`

[Previous content remains unchanged...]

## High Availability
###### tags: `ha`, `clustering`, `failover`, `load-balancing`, `replication`, `redundancy`

[Previous content remains unchanged...]

## Infrastructure Automation
###### tags: `automation`, `infrastructure`, `configuration`, `provisioning`, `orchestration`, `iac`

[Previous content remains unchanged...]

## Cloud Integration
###### tags: `cloud`, `aws`, `gcp`, `azure`, `iam`, `security`

```bash
# AWS CLI Basic Operations
aws configure                # Configure credentials
aws sts get-caller-identity # Check identity
aws ec2 describe-instances  # List EC2 instances
aws s3 ls                   # List S3 buckets
aws rds describe-db-instances # List RDS instances
aws lambda list-functions   # List Lambda functions

# AWS EC2 Management
aws ec2 run-instances --image-id ami-id --instance-type t2.micro  # Launch instance
aws ec2 start-instances --instance-ids id  # Start instance
aws ec2 stop-instances --instance-ids id   # Stop instance
aws ec2 terminate-instances --instance-ids id # Terminate instance
aws ec2 describe-security-groups          # List security groups
aws ec2 create-tags --resources id --tags Key=Name,Value=value # Tag resource

# AWS S3 Operations
aws s3 mb s3://bucket-name              # Create bucket
aws s3 cp file.txt s3://bucket/         # Upload file
aws s3 sync local/ s3://bucket/         # Sync directory
aws s3api put-bucket-policy --bucket name --policy file # Set policy
aws s3 presign s3://bucket/object       # Generate URL
aws s3api list-object-versions --bucket name # List versions

# AWS RDS Management
aws rds create-db-instance              # Create database
aws rds describe-db-instances           # List instances
aws rds start-db-instance              # Start instance
aws rds stop-db-instance               # Stop instance
aws rds create-db-snapshot             # Create snapshot
aws rds restore-db-instance-from-snapshot # Restore snapshot

# GCP CLI Basic Operations
gcloud init                            # Initialize SDK
gcloud auth login                      # Authenticate
gcloud config list                     # Show config
gcloud projects list                   # List projects
gcloud compute instances list          # List instances
gcloud services list                   # List services

# GCP Compute Engine
gcloud compute instances create name   # Create instance
gcloud compute instances start name    # Start instance
gcloud compute instances stop name     # Stop instance
gcloud compute instances delete name   # Delete instance
gcloud compute ssh instance-name       # SSH to instance
gcloud compute images list            # List images

# GCP Storage Operations
gsutil mb gs://bucket-name            # Create bucket
gsutil cp file.txt gs://bucket/       # Upload file
gsutil rsync -r local/ gs://bucket/   # Sync directory
gsutil iam ch user:role gs://bucket   # Set permissions
gsutil signurl -d 10m key gs://path   # Generate URL
gsutil versioning set on gs://bucket  # Enable versioning

# GCP Cloud SQL
gcloud sql instances create name      # Create instance
gcloud sql instances patch name       # Modify instance
gcloud sql backups create            # Create backup
gcloud sql connect instance-name      # Connect to DB
gcloud sql users list                # List users
gcloud sql instances clone source target # Clone instance

# Azure CLI Basic Operations
az login                             # Login
az account show                      # Show account
az account list                      # List accounts
az group list                        # List groups
az vm list                          # List VMs
az storage account list             # List storage

# Azure VM Management
az vm create                        # Create VM
az vm start --name vm --resource-group group  # Start VM
az vm stop --name vm --resource-group group   # Stop VM
az vm delete --name vm --resource-group group # Delete VM
az vm list-sizes --location location         # List sizes
az vm image list                            # List images

# Azure Storage Operations
az storage account create           # Create account
az storage container create         # Create container
az storage blob upload             # Upload blob
az storage blob download           # Download blob
az storage account keys list       # List keys
az storage share create           # Create file share

# Azure Database
az sql server create              # Create server
az sql db create                 # Create database
az sql db list                   # List databases
az sql server firewall-rule create # Create firewall rule
az sql db restore                # Restore database
az sql db export                 # Export database

# Cloud Security
# AWS IAM
aws iam create-user              # Create user
aws iam create-role              # Create role
aws iam attach-role-policy       # Attach policy
aws iam list-users               # List users
aws iam list-roles               # List roles
aws kms list-keys               # List KMS keys

# GCP IAM
gcloud iam service-accounts create # Create service account
gcloud projects add-iam-policy-binding # Add binding
gcloud iam roles create          # Create role
gcloud iam service-accounts keys create # Create key
gcloud kms keys list            # List KMS keys
gcloud organizations get-iam-policy # Get org policy

# Azure IAM
az ad user create               # Create user
az role assignment create       # Assign role
az role definition create      # Create role
az ad app create               # Create app
az keyvault create            # Create vault
az keyvault secret set        # Set secret

# Cross-Cloud Management
# Infrastructure
terraform init                 # Initialize
terraform plan                # Plan changes
terraform apply               # Apply changes
terraform destroy            # Destroy resources
terraform workspace list     # List workspaces
terraform state list        # List resources

# Monitoring
aws cloudwatch get-metrics   # AWS metrics
gcloud monitoring metrics list # GCP metrics
az monitor metrics list     # Azure metrics
prometheus query api        # Query metrics
grafana dashboard import    # Import dashboard
datadog agent status       # Agent status

# Cost Management
aws ce get-cost-and-usage  # AWS costs
gcloud billing accounts list # GCP billing
az consumption usage list  # Azure usage
infracost breakdown       # Cost analysis
komiser analyze          # Cloud inventory
cloudhealth report      # Cost report
```

```bash
# Ansible Commands
ansible all -m ping                     # Test connectivity
ansible-playbook playbook.yml          # Run playbook
ansible-galaxy install role             # Install role
ansible-vault create secret.yml         # Create vault
ansible-inventory --list                # List inventory
ansible-config dump                     # Show config

# Ansible Playbook Operations
ansible-playbook site.yml --check       # Dry run
ansible-playbook site.yml --diff        # Show changes
ansible-playbook site.yml --tags "tag"  # Run specific tags
ansible-playbook site.yml --limit host  # Limit hosts
ansible-lint playbook.yml               # Lint playbook
ansible-doc -l                          # List modules

# Puppet Commands
puppet agent --test                     # Run agent
puppet apply manifest.pp                # Apply manifest
puppet cert list                        # List certs
puppet config print                     # Show config
puppet module install module            # Install module
puppet resource package nginx           # Show resource

# Puppet Development
puppet parser validate file.pp          # Validate syntax
puppet-lint manifest.pp                 # Lint manifest
puppet module generate name             # Create module
puppet lookup key --node node           # Lookup value
puppet device --verbose                 # Run device
r10k deploy environment                 # Deploy env

# Chef Commands
chef-client                            # Run client
knife node list                        # List nodes
knife cookbook upload cookbook         # Upload cookbook
knife role show role                   # Show role
knife ssh 'name:*' 'command'           # Run command
berks install                          # Install cookbooks

# Chef Development
chef generate cookbook name            # Create cookbook
chef exec rspec                        # Run tests
foodcritic cookbook                    # Lint cookbook
kitchen test                          # Test cookbook
chef-run node recipe                  # Run recipe
ohai                                  # System info

# Terraform Commands
terraform init                        # Initialize
terraform plan                        # Show changes
terraform apply                       # Apply changes
terraform destroy                     # Destroy resources
terraform validate                    # Validate config
terraform fmt                         # Format code

# Terraform State Management
terraform state list                  # List resources
terraform state show resource         # Show resource
terraform import resource id          # Import resource
terraform state mv source dest        # Move resource
terraform state rm resource           # Remove resource
terraform refresh                     # Update state

# SaltStack Commands
salt '*' test.ping                    # Test minions
salt-key -L                           # List keys
salt-call --local state.apply         # Apply state
salt '*' pkg.install nginx            # Install package
salt '*' service.restart nginx        # Restart service
salt-run jobs.active                  # Show jobs

# SaltStack State Management
salt '*' state.show_top               # Show top file
salt '*' state.show_sls state         # Show state
salt '*' state.apply state test=True  # Test state
salt '*' state.highstate             # Apply highstate
salt-run state.orch orchestrate      # Run orchestration
salt-run manage.status               # Show status

# Version Control Integration
# Git
git clone repo                       # Clone repo
git pull origin master              # Update repo
git add .                           # Stage changes
git commit -m "message"             # Commit changes
git push origin master             # Push changes

# CI/CD Integration
# Jenkins
jenkins-jobs update job.yml         # Update job
jenkins-jobs test job.yml          # Test job
java -jar jenkins-cli.jar -s url   # CLI access
curl -X POST jenkins/job/build     # Trigger build
jenkins-plugin-cli --plugins list  # List plugins

# Testing Tools
# Molecule
molecule init scenario             # Create scenario
molecule create                    # Create instances
molecule converge                 # Apply changes
molecule verify                   # Run tests
molecule destroy                  # Cleanup

# InSpec
inspec init profile name          # Create profile
inspec exec profile              # Run tests
inspec check profile            # Validate profile
inspec shell                    # Interactive mode
inspec compliance login        # Login to Chef
```

```bash
# Pacemaker Cluster Management
pcs status                # Cluster status
pcs cluster setup --name cluster_name node1 node2  # Setup cluster
pcs cluster start --all   # Start cluster
pcs cluster enable --all  # Enable at boot
pcs resource show         # Show resources
pcs stonith list         # Show fencing devices

# Corosync Configuration
corosync-cfgtool -s      # Cluster status
corosync-quorumtool -l   # Quorum status
corosync-cmapctl         # Show config
corosync-keygen          # Generate key
corosync -f              # Run in foreground
crm_verify -L            # Verify config

# HAProxy Load Balancing
haproxy -c -f /etc/haproxy/haproxy.cfg  # Check config
haproxy -D -f /etc/haproxy/haproxy.cfg  # Start daemon
echo "show info" | socat stdio /var/run/haproxy.sock  # Get info
echo "show stat" | nc -U /var/run/haproxy.sock  # Show stats
hatop -s /var/run/haproxy.sock          # Interactive monitor
halog -srv < /var/log/haproxy.log       # Analyze logs

# Keepalived VRRP
keepalived -f /etc/keepalived/keepalived.conf  # Start service
keepalived -t           # Test config
ip addr show           # Check VIP
ipvsadm -Ln            # Show LVS table
ipvsadm -Z             # Clear statistics
genhash -s server -p 80 -u /path  # Generate hash

# Database Replication
# MySQL/MariaDB
show master status;     # Show master status
show slave status\G     # Show slave status
change master to ...    # Configure replication
start slave;           # Start replication
stop slave;            # Stop replication
reset slave;           # Reset slave

# PostgreSQL
pg_basebackup -D /path -h host -U user  # Create standby
pg_ctl promote         # Promote to master
pg_rewind              # Resync instance
pg_receivexlog         # Stream WAL
psql -x -c "select * from pg_stat_replication;"  # Check status

# Redis Replication
redis-cli info replication  # Show replication info
redis-cli role            # Show node role
redis-cli cluster info    # Cluster status
redis-cli sentinel master mymaster  # Sentinel info
redis-cli slaveof host port  # Configure replica
redis-cli cluster nodes   # Show cluster nodes

# Distributed Storage
# GlusterFS
gluster peer status              # Show peers
gluster volume info              # Volume info
gluster volume create vol replica 2 server1:/brick1 server2:/brick1  # Create volume
gluster volume start vol         # Start volume
gluster volume heal vol info     # Check healing
gluster volume rebalance vol status  # Check rebalance

# Ceph
ceph status                     # Cluster status
ceph osd tree                   # Show OSD tree
ceph df                        # Show usage
ceph auth list                 # Show auth
rados df                       # Pool usage
rbd ls                        # List images

# Service Discovery
# Consul
consul members                 # Show members
consul info                   # Show info
consul kv put key value       # Set key
consul kv get key            # Get key
consul monitor               # Watch events
consul reload               # Reload config

# etcd
etcdctl member list           # Show members
etcdctl get key              # Get key
etcdctl put key value        # Set key
etcdctl watch key            # Watch key
etcdctl endpoint health      # Check health
etcdctl snapshot save file   # Create snapshot

# Cluster Monitoring
crm_mon -1                   # One-shot status
crm_mon -f                   # Monitor status
clustat                      # Cluster status
cluster.py                   # Cluster tools
drbdadm status              # DRBD status
lvs -v                      # LVS status

# Failover Testing
pcs resource move resource node  # Move resource
pcs resource ban resource node   # Ban from node
pcs resource clear resource     # Clear constraints
pcs stonith fence node         # Fence node
crm_failcount -r resource show  # Show failures
crm_attribute -n maintenance-mode -v true  # Maintenance mode
```

```bash
# Prometheus Management
prometheus --config.file=/etc/prometheus/prometheus.yml  # Start Prometheus
promtool check config /etc/prometheus/prometheus.yml     # Check config
promtool debug all /etc/prometheus/prometheus.yml        # Debug config
curl localhost:9090/-/healthy                           # Health check
curl localhost:9090/-/reload                            # Reload config

# Prometheus Query
promql-cli "up"                    # Check targets up/down
promql-cli "rate(http_requests_total[5m])"  # Request rate
promtool query instant http://localhost:9090 'memory_usage'  # Instant query
curl -G --data-urlencode 'query=up' http://localhost:9090/api/v1/query  # API query

# Grafana CLI
grafana-cli plugins list-remote    # List plugins
grafana-cli plugins install plugin # Install plugin
grafana-server -config /etc/grafana/grafana.ini  # Start server
grafana-cli admin reset-admin-password newpass   # Reset password
curl http://localhost:3000/api/health            # Health check

# Grafana Management
grafana-cli plugins update-all     # Update plugins
grafana-cli plugins remove plugin  # Remove plugin
systemctl restart grafana-server   # Restart service
grafana-cli data-migration        # Run migrations
grafana-cli admin user-create     # Create user

# Nagios Core
systemctl status nagios           # Service status
nagios -v /etc/nagios/nagios.cfg # Verify config
nagiostats                       # Show statistics
nagios --test                    # Test config
send_nsca                        # Send check results
nagios --verify-config           # Deep config check

# Nagios Configuration
check_nrpe -H host               # Check NRPE
check_http -H host               # Check HTTP
check_ping -H host               # Check ping
check_load                       # Check system load
check_disk -w 80 -c 90          # Check disk space
check_users -w 5 -c 10          # Check users

# Zabbix Server
zabbix_server -R config_cache_reload  # Reload config
zabbix_server -R housekeeper_execute  # Run housekeeper
zabbix_get -s host -k key            # Get item value
zabbix_sender -z server -s host -k key -o value  # Send value
zbxcmd                               # Command line tool
zabbix_proxy -R config_cache_reload  # Reload proxy

# Zabbix Agent
zabbix_agentd -t key                 # Test item
zabbix_agentd -p                     # Print supported
zabbix_agent2 -R userparameter_reload # Reload parameters
zabbix_get -s 127.0.0.1 -k "system.cpu.load"  # Local check
userparameter_mysql                  # MySQL monitoring

# Monitoring Tools
collectd                            # System statistics
statsd                             # Stats aggregation
telegraf --config telegraf.conf    # Metrics collection
node_exporter                      # System metrics
cadvisor                          # Container metrics
blackbox_exporter                 # Endpoint probing

# Alert Management
alertmanager --config.file=alertmanager.yml  # Start AlertManager
amtool check-config alertmanager.yml         # Check config
amtool alert add alertname=test              # Add alert
amtool silence add alertname=test            # Add silence
amtool cluster show                         # Show cluster
amtool config routes show                   # Show routes

# Metric Collection
netdata                           # Real-time monitoring
collectd -t                       # Test config
influxd                          # Time series DB
victoria-metrics                 # Time series DB
prometheus-node-exporter         # System metrics
mtail                           # Log metrics

# Visualization
grafana-reporter                 # Generate reports
grafana-image-renderer          # Render panels
chronograf                      # Time series UI
kapacitor                      # Real-time processing
alerta                        # Alert management
```

```bash
# KVM Management
virsh list --all         # List VMs
virsh start vm-name      # Start VM
virsh shutdown vm-name   # Stop VM
virsh destroy vm-name    # Force stop
virsh edit vm-name       # Edit config
virsh console vm-name    # Connect to VM

# VM Creation
virt-install --name vm --ram 2048 --disk path=/vm.qcow2  # Create VM
qemu-img create -f qcow2 vm.qcow2 20G  # Create disk
qemu-img info vm.qcow2   # Show disk info
qemu-img resize vm.qcow2 +10G  # Resize disk
virt-clone --original vm --name vm2 --auto-clone  # Clone VM

# VM Resources
virsh setmem vm-name 4G  # Set RAM
virsh setvcpus vm-name 2 # Set CPUs
virsh dominfo vm-name    # VM info
virsh domstats vm-name   # VM stats
virsh cpu-stats vm-name  # CPU stats
virsh dommemstat vm-name # Memory stats

# Storage Management
virsh pool-list          # List pools
virsh vol-list default   # List volumes
virsh pool-create-as name dir --target /vm/pools  # Create pool
virsh vol-create-as default vm.qcow2 20G  # Create volume
virsh pool-destroy name  # Delete pool
virsh vol-delete vm.qcow2 default  # Delete volume

# Network Management
virsh net-list           # List networks
virsh net-info default   # Network info
virsh net-start name     # Start network
virsh net-destroy name   # Stop network
virsh net-edit name      # Edit network
virsh net-dhcp-leases default  # Show leases

# VM Snapshots
virsh snapshot-create-as vm-name snap1  # Create snapshot
virsh snapshot-list vm-name  # List snapshots
virsh snapshot-revert vm-name snap1  # Restore
virsh snapshot-delete vm-name snap1  # Delete snapshot
virsh snapshot-info vm-name snap1  # Snapshot info
```

## Performance Tuning
###### tags: `performance`, `optimization`, `tuning`, `profiling`, `monitoring`

```bash
# CPU Tuning
cpupower frequency-info   # CPU frequency info
cpupower frequency-set -g performance # Set governor
taskset -pc 0-3 pid      # Set CPU affinity
nice -n -20 command      # Set high priority
chrt -f 99 command       # Set real-time priority
tuned-adm profile throughput-performance # Set profile

# Memory Optimization
sysctl vm.swappiness=10  # Reduce swapping
sysctl vm.vfs_cache_pressure=50 # Cache pressure
sysctl vm.dirty_ratio=10 # Dirty ratio
vmstat -SM 1            # Monitor VM stats
free -h                 # Show memory usage
smem -tk               # Show memory by process

# Disk I/O Tuning
hdparm -tT /dev/sda     # Disk speed test
blockdev --report       # Block device report
ionice -c2 -n0 command  # Set I/O priority
fstrim -av              # TRIM SSD
echo deadline > /sys/block/sda/queue/scheduler # I/O scheduler
fio --name=test --filename=file # I/O benchmark

# Network Performance
ethtool -g eth0         # NIC buffer size
ip link set eth0 txqueuelen 10000 # Queue length
sysctl net.core.rmem_max=16777216 # Socket buffer
tc qdisc add dev eth0 root fq # Fair queuing
netperf -H server       # Network benchmark
iperf3 -c server       # Bandwidth test

# Process Optimization
systemd-cgtop           # Show cgroup usage
systemd-analyze         # Boot time analysis
systemd-analyze blame   # Service startup time
pmap pid               # Process memory map
strace -c command      # System call profile
perf top               # Performance monitor

# Database Tuning
mysqltuner             # MySQL tuner
pgbench -i dbname      # PostgreSQL benchmark
redis-benchmark        # Redis benchmark
mongotop              # MongoDB monitoring
vacuum analyze table   # PostgreSQL maintenance
analyze table tbl      # MySQL table analysis
```

## Advanced Networking
###### tags: `networking`, `vpn`, `firewall`, `routing`, `traffic`, `security`

```bash
# VPN Management
openvpn --config file.ovpn   # Start OpenVPN
systemctl status openvpn     # VPN service status
ipsec status                # IPsec status
strongswan status           # StrongSwan status
wireguard-quick up wg0      # Start WireGuard
wg show                     # WireGuard status

# Advanced Firewall
iptables -L                 # List rules
iptables -A INPUT -p tcp --dport 80 -j ACCEPT  # Allow HTTP
ufw status verbose         # UFW status
ufw allow from 192.168.1.0/24  # Allow subnet
firewall-cmd --list-all    # firewalld rules
nft list ruleset          # nftables rules

# Traffic Control
tc qdisc show              # Show queuing disciplines
tc class show dev eth0     # Show traffic classes
wondershaper eth0 1024 512 # Limit bandwidth
trickle -d 100 -u 50 command  # Limit program bandwidth
nethogs                    # Monitor per-process traffic
iftop -i eth0             # Monitor interface traffic

# Advanced Routing
ip route add 10.0.0.0/24 via 192.168.1.1  # Add route
ip rule add from 192.168.1.0/24 table 10  # Policy routing
vconfig add eth0 100      # Add VLAN
brctl addbr br0           # Add bridge
ovs-vsctl add-br br0      # Add OpenvSwitch bridge
iproute2 tc qdisc add     # Traffic control

# Network Monitoring
tcpdump -i eth0 port 80   # Capture HTTP traffic
wireshark -i eth0         # GUI packet analyzer
nmap -sS 192.168.1.0/24   # Network scan
mtr hostname              # Network diagnostic
iperf3 -s                # Network performance
netstat -tunapl          # Connection status

# Load Balancing
haproxy -f config        # Start HAProxy
nginx -t                 # Test Nginx config
keepalived -f config     # High availability
ipvsadm -L              # Show LVS rules
balance 80              # Simple TCP balancer
```

## Useful One-liners
###### tags: `oneliners`, `scripts`, `automation`

```bash
# Find large files/directories
find / -type f -size +100M -exec ls -lh {} \;
du -h / | sort -rh | head -n 20

# Monitor system resources
watch -n 1 'free -h; df -h; w'

# Kill processes by pattern
ps aux | grep pattern | awk '{print $2}' | xargs kill

# System backup
tar czf backup-$(date +%F).tar.gz /important/directory/

# Monitor failed SSH attempts
tail -f /var/log/auth.log | grep 'Failed password'

# Check disk IO
iostat -xz 1

# Find files modified in last 24h
find / -mtime -1 -type f -exec ls -l {} \;

# System load average graph
sar -q | awk '{print $4}' | grep -v Linux | graph -T png > load.png
