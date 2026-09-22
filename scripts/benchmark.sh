#!/bin/bash
# Sysbench CPU Benchmark Execution Automation Script

set -e

echo "=================================================="
echo " Starting Sysbench CPU Hypervisor Performance Test"
echo "=================================================="

# 1. Check if sysbench is installed
if ! command -v sysbench &> /dev/null; then
    echo "[!] sysbench could not be found. Installing..."
    sudo apt-get update -y && sudo apt-get install -y sysbench
fi

# 2. Display System Info
echo "[+] System Info:"
hostnamectl
echo ""
echo "[+] CPU Allocation:"
lscpu | grep -E "Model name|CPU\(s\):|Thread\(s\) per core:"
echo ""
echo "[+] Memory Allocation:"
free -h

# 3. Run Benchmark
echo "=================================================="
echo " Running Sysbench CPU Prime Calculation (20k max prime)..."
echo "=================================================="

sysbench cpu --cpu-max-prime=20000 run

echo "=================================================="
echo " Benchmark Execution Complete."
echo "=================================================="
