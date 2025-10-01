#!/bin/bash

# Script Name: system-info.sh
# Description: Collects and prints basic system information including:
#              - Hardware model (via dmidecode, /sys, or /proc fallbacks)
#              - Operating system details (from /etc/os-release, lsb_release, etc.)
#              - Hostname of the system
# Author: JessyJP
# Dependencies: dmidecode (optional), lsb_release (optional)
# Usage: ./system-info.sh

# Function to get the hardware model
get_hardware_model() {
    local model=""

    if command -v dmidecode &> /dev/null; then
        model=$(sudo dmidecode -s system-product-name 2>/dev/null | tr -d '\0')
    fi

    if [ -z "$model" ] && [ -f /sys/class/dmi/id/product_name ]; then
        model=$(cat /sys/class/dmi/id/product_name | tr -d '\0')
    fi

    if [ -z "$model" ] && [ -f /proc/device-tree/model ]; then
        model=$(cat /proc/device-tree/model | tr -d '\0')
    fi

    if [ -z "$model" ] && [ -f /proc/cpuinfo ]; then
        model=$(grep -m 1 'Model' /proc/cpuinfo | awk -F ': ' '{print $2}' | tr -d '\0')
    fi

    if [ -z "$model" ]; then
        model="Unknown Hardware Model"
    fi

    echo "$model"
}

# Function to get the OS information
get_os_info() {
    local os_info=""

    if [ -f /etc/os-release ]; then
        . /etc/os-release
        os_info="$NAME $VERSION"
    elif command -v lsb_release &> /dev/null; then
        os_info=$(lsb_release -d | awk -F ': ' '{print $2}')
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        os_info="$DISTRIB_DESCRIPTION"
    elif [ -f /etc/debian_version ]; then
        os_info="Debian $(cat /etc/debian_version)"
    else
        os_info="Unknown OS"
    fi

    echo "$os_info"
}

# Function to get the hostname
get_hostname() {
    hostname
}

# Function to print all system information
print_system_info() {
    echo "Hardware Model: $(get_hardware_model)"
    echo "OS Information: $(get_os_info)"
    echo "Hostname: $(get_hostname)"
}

# If the script is executed directly, print the system information
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    print_system_info
fi
