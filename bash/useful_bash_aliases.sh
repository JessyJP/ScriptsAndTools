# Project Specific
alias ssh_connect="clear; dos2unix ssh_connect.sh; ./ssh_connect.sh"
alias connect="clear; dos2unix ssh_connect.sh; ./ssh_connect.sh"
alias redeploy_the_lazy_way="clear; dos2unix ./redeploy_the_lazy_way.sh; time ./redeploy_the_lazy_way.sh"
alias lazy="clear; dos2unix ./redeploy_the_lazy_way.sh; time ./redeploy_the_lazy_way.sh"
alias move="clear; dos2unix move.sh; ./move.sh .env"

# Print my public IP
alias myip='curl ipinfo.io/ip; echo ""'
# Resume wget by default
alias wget="wget -c"  # Resume incomplete downloads

# Networking Commands
alias ports='sudo netstat -tulanp'  # List all listening ports
alias ports2='nmap localhost'  # Scan open ports on localhost
alias dens="sudo systemd-resolve --status | grep 'DNS Servers'"  # Get DNS server information

# System Control and Information
alias ctl="systemctl"
alias whatsup='service --status-all'
# For processes
alias psmem="ps auxf | sort -nr -k 4"  # Sort processes by memory usage
alias psmem10="ps auxf | sort -nr -k 4 | head -10"  # Top 10 processes by memory usage
# Process Management
alias paux='ps aux | grep'  # Search processes

# CPU Information
alias cpuinfo="lscpu"  # Display CPU architecture information
alias cpuinfo_old="less /proc/cpuinfo"  # Display CPU information from /proc
alias pscpu="ps auxf | sort -nr -k 3"  # Sort processes by CPU usage
alias pscpu10="ps auxf | sort -nr -k 3 | head -10"  # Top 10 processes by CPU usage

# Memory Information
alias meminfo="free -m -l -t"  # Show memory usage in MB
alias gpumeminfo="grep -i --color memory /var/log/Xorg.0.log"  # Display GPU memory info from Xorg log

# File Navigation and Management
function cds {
  cd "$1" && ls -lah  # Change directory and list all files in long format with hidden files
}

# Copy with progress bar
alias cpv='rsync -ah --info=progress2'  # Copy files with progress info

# File Listing
alias du1="du -d 1"  # Show disk usage to depth 1
alias ll="ls -al"  # List all files in long format
alias lt='ls --human-readable --size -1 -S --classify'  # List files sorted by size
alias la='ls -A'  # List all files excluding . and ..
alias ls='ls -CF'  # List files in columns
alias lu='du -sh * | sort -h'  # Sort files by size
alias lc='find . -type f | wc -l'  # Count all files recursively
alias ld='ls -d */'  # List directories only
alias usage='du -ch | grep total'  # Show disk usage in current directory
alias totalusage='df -hl --total | grep total'  # Show total disk usage on machine
alias partusage='df -hlT --exclude-type=tmpfs --exclude-type=devtmpfs'  # Show partition usages excluding temporary memory
alias most='du -hsx * | sort -rh | head -10'  # Show top 10 largest files and directories

# Calculator
alias bc="bc -l"  # Use bc with math library

# History commands
alias h="history"  # Show command history
alias h1="history 10"  # Show last 10 commands
alias h2="history 20"  # Show last 20 commands
alias h3="history 30"  # Show last 30 commands
alias hgrep='history | grep'  # Search command history

# Launch Simple HTTP Server
alias serve='python -m SimpleHTTPServer'

# Docker Commands
dc-run() { sudo docker run -i -t --privileged "$@" ;}  # Run a Docker container in interactive mode with privileges
dc-exec() { sudo docker exec -i -t "$@" /bin/bash ;}  # Execute a command in a running container
dc-log() { sudo docker logs --tail=all -f "$@" ;}  # Follow logs of a container
dc-port() { sudo docker port "$@" ;}  # List port mappings for a container
dc-vol() { sudo docker inspect --format '{{ .Volumes }}' "$@" ;}  # Inspect volumes of a container
dc-ip() { sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' "$@" ;}  # Get IP address of a container
dc-rmc() { sudo docker rm $(sudo docker ps -qa --filter 'status=exited') ;}  # Remove all stopped containers
dc-rmi() { sudo docker rmi -f $(sudo docker images | grep '^<none>' | awk '{print $3}') ;}  # Remove all dangling images
dc-stop() { sudo docker stop $(docker ps -a -q); }  # Stop all running containers
dc-rm() { sudo docker rm $(docker ps -a -q); }  # Remove all containers

# Docker bulk operation - starts, stops, pauses, or unpauses all containers based on the argument
dc-do() {
  if [ "$#" -ne 1 ]; then echo "Usage: $0 start|stop|pause|unpause"; return 1; fi
  for c in $(sudo docker ps -a | awk '{print $1}' | sed "1 d"); do
    sudo docker "$1" "$c"
  done
}

# Fix command
alias fix="fuck"  # Alias for thefuck command
