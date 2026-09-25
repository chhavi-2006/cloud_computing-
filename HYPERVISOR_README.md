# Experiment 1: Type-1 (Bare-Metal) vs Type-2 (Hosted) Hypervisor Performance Analysis

[![Hypervisors](https://img.shields.io/badge/Hypervisors-Proxmox%20VE%20%7C%20VMware%20Workstation-orange.svg)](#)
[![Benchmark](https://img.shields.io/badge/Benchmark-Sysbench%20CPU%2020k%20Primes-green.svg)](#)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)](#)

---

## Executive Summary

This report contains the complete experimental setup, empirical benchmark data, performance visualization, and technical analysis comparing the CPU performance of a **Type-1 Bare-Metal Hypervisor (Proxmox VE)** and a **Type-2 Hosted Hypervisor (VMware Workstation)**.

Both hypervisors were deployed with identically configured **Ubuntu Virtual Machines** (2 vCPU, 2 GB RAM, 20 GB Disk). The standard `sysbench` CPU prime-number calculation benchmark (`--cpu-max-prime=20000`) was executed on both virtual machines under identical workload conditions.

### Key Finding

> **Proxmox VE (Type-1 Hypervisor) achieved 925.32 Events/sec compared to VMware Workstation's 734.96 Events/sec — demonstrating a +25.90% throughput advantage, a 20.59% reduction in average latency, and a 31.77% reduction in maximum latency spikes.**

---

## Table of Contents

1. [Project Objectives](#1-project-objectives)
2. [Hypervisor Architectural Comparison](#2-hypervisor-architectural-comparison)
3. [Virtual Machine Specifications](#3-virtual-machine-specifications)
4. [Experimental Procedure](#4-experimental-procedure)
5. [Empirical Results & Screenshots](#5-empirical-results--screenshots)
6. [Performance Comparison Table](#6-performance-comparison-table)
7. [Metric Explanations & Visualizations](#7-metric-explanations--visualizations)
8. [Technical Analysis & Discussion](#8-technical-analysis--discussion)
9. [Conclusion & Engineering Takeaways](#9-conclusion--engineering-takeaways)

---

## 1. Project Objectives

The primary objectives of this hypervisor performance analysis are:

1. **Deployment**: Provision two identical Ubuntu Virtual Machines across different hypervisor architectures:
   - **Type-1 (Bare-Metal)**: Proxmox VE (Kernel-based Virtual Machine / KVM)
   - **Type-2 (Hosted)**: VMware Workstation Pro on a Windows Host OS
2. **Standardization**: Enforce uniform hardware resource allocations (2 vCPU, 2048 MB RAM, 20 GB Virtual Storage) to ensure direct comparability.
3. **Benchmarking**: Execute the `sysbench` CPU computational benchmark using 20,000 prime numbers to stress test CPU virtualization efficiency.
4. **Metric Collection**: Capture execution time, total events processed, throughput (events/sec), and latency statistics (min, avg, max, 95th percentile).
5. **Architectural Evaluation**: Quantify the performance overhead introduced by host operating system abstraction layers in Type-2 hypervisors versus bare-metal hypervisor execution.

---

## 2. Hypervisor Architectural Comparison

### Type-1 Hypervisor — Proxmox VE (Bare-Metal Architecture)

Proxmox VE runs directly on physical host hardware. The Linux kernel integrated with KVM (Kernel-based Virtual Machine) acts as the hypervisor. Guest operating system instructions execute directly on hardware CPU VT-x/AMD-V extensions without passing through an intermediate desktop operating system.

```
+-------------------------------------------------------------------+
|               Ubuntu Virtual Machine (Type-1 Guest)               |
+-------------------------------------------------------------------+
|               Proxmox VE Hypervisor (Linux Kernel / KVM)          |
+-------------------------------------------------------------------+
|                 Physical Server Hardware (Bare Metal)             |
+-------------------------------------------------------------------+
```

---

### Type-2 Hypervisor — VMware Workstation (Hosted Architecture)

VMware Workstation runs as an application process on top of a host operating system (Windows 11/10). CPU requests from the guest VM must navigate through the VMware VMM engine, translate through host OS system calls, and be scheduled by the Windows NT kernel scheduler before reaching physical hardware.

```
+-------------------------------------------------------------------+
|               Ubuntu Virtual Machine (Type-2 Guest)               |
+-------------------------------------------------------------------+
|               VMware Workstation (Virtual Machine Monitor)        |
+-------------------------------------------------------------------+
|               Host Operating System (Windows 11 / 10)             |
+-------------------------------------------------------------------+
|                        Physical PC Hardware                       |
+-------------------------------------------------------------------+
```

---

## 3. Virtual Machine Specifications

| Resource Parameter | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Status |
| :--- | :--- | :--- | :--- |
| **Virtual Machine Name** | `type1-virtual-machine` | `type2-virtual-machine` | Standardized |
| **Guest Operating System** | Ubuntu 22.04.5 LTS (x86_64) | Ubuntu 22.04.5 LTS (x86_64) | Standardized |
| **Kernel Version** | Linux 6.8.0-138-generic | Linux 6.8.0-138-generic | Standardized |
| **CPU Allocation** | 2 vCPU (1 Socket, 2 Cores) | 2 vCPU (1 Processor, 2 Cores) | Identical |
| **RAM Allocation** | 2048 MiB (2.0 GB) | 2048 MB (2.0 GB) | Identical |
| **Virtual Disk Capacity** | 20.0 GB | 20.0 GB | Identical |
| **Virtualization Backend** | KVM / VirtIO | VMware Virtual Platform | Standardized |
| **Benchmark Tool** | `sysbench 1.0.20` | `sysbench 1.0.20` | Identical |

---

## 4. Experimental Procedure

```bash
# Verify Host System Specs
hostnamectl
lscpu
free -h

# Install Sysbench
sudo apt update && sudo apt install sysbench -y

# Run CPU Benchmark (20k Primes)
sysbench cpu --cpu-max-prime=20000 run
```

---

## 5. Empirical Results & Screenshots

### Guest VM Host System Terminal Verification (`hostnamectl`)
![Type-2 Hostnamectl Screenshot](images/1.png)

*Figure 1: `hostnamectl` verification output on `type2-virtual-machine` running Ubuntu 22.04.5 LTS.*

---

### Type-2 Hypervisor Performance Summary & Benchmark Results
![Type-2 Hypervisor Performance Results Table](images/2.png)

*Figure 2: Empirical Performance Results Table recorded for VMware Workstation (Type-2 Hypervisor).*

![Type-2 Sysbench Terminal Execution](images/type2_sysbench_terminal.png)

*Figure 3: Empirical Sysbench terminal output recorded for VMware Workstation (Type-2 Hypervisor).*

---

## 6. Performance Comparison Table

| Performance Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Performance Delta | Winner / Advantage |
| :--- | :---: | :---: | :---: | :---: |
| **Hypervisor Architecture** | Bare-Metal | Hosted | Architectural | Type-1 Direct Control |
| **Guest OS** | Ubuntu 22.04.5 LTS | Ubuntu 22.04.5 LTS | Matched | Identical Baseline |
| **vCPU Allocation** | 2 vCPU | 2 vCPU | Matched | Identical Compute |
| **RAM Allocation** | 2 GB | 2 GB | Matched | Identical Memory |
| **Disk Capacity** | 20 GB | 20 GB | Matched | Identical Storage |
| **Total Execution Time** | **10.0008 s** | **10.0014 s** | ~0.006% difference | Fixed 10s Window |
| **Total Events Processed** | **9,254** | **7,352** | **+1,902 events (+25.87%)** | **Proxmox VE (Type-1)** |
| **Events per Second (EPS)** | **925.32** | **734.96** | **+190.36 eps (+25.90%)** | **Proxmox VE (Type-1)** |
| **Minimum Latency** | **0.65 ms** | **0.82 ms** | **-0.17 ms (-20.73%)** | **Proxmox VE (Faster)** |
| **Average Latency** | **1.08 ms** | **1.36 ms** | **-0.28 ms (-20.59%)** | **Proxmox VE (Lower)** |
| **95th Percentile Latency**| **1.63 ms** | **2.07 ms** | **-0.44 ms (-21.26%)** | **Proxmox VE (More Consistent)**|
| **Maximum Latency** | **8.42 ms** | **12.34 ms** | **-3.92 ms (-31.77%)** | **Proxmox VE (Fewer Spikes)** |

---

## 7. Metric Explanations & Visualizations

### Chart 1: CPU Throughput Comparison (Events / Sec)
![CPU Throughput Comparison](images/events_per_second_comparison.png)

*Figure 4: CPU Throughput comparison showing Proxmox VE (+25.90% faster).*

---

### Chart 2: CPU Latency Metrics Comparison
![Latency Comparison](images/latency_comparison.png)

*Figure 5: Latency metrics comparison (Min, Avg, 95th Pct, Max) across both hypervisors.*

---

### Chart 3: Comprehensive Performance Dashboard
![Overall Performance Dashboard](images/overall_performance_dashboard.png)

*Figure 6: Multi-panel performance evaluation dashboard.*

---

## 8. Technical Analysis & Discussion

1. **Architectural Overhead & Context Switching**: Proxmox VE (Type-1) utilizes Linux KVM, which interfaces directly with hardware Intel VT-x / AMD-V virtualization extensions in VMX root mode. VMware Workstation (Type-2) operates on top of Windows NT OS, requiring context transitions through Windows system calls (`NtSystemService`).
2. **CPU Scheduling**: In Proxmox VE, guest vCPUs map directly to host Linux kernel POSIX threads scheduled by CFS. In VMware Workstation, guest CPU execution competes with Windows host background services, leading to higher latency spikes (Max Latency: 12.34 ms on VMware vs 8.42 ms on Proxmox).

---

## 9. Conclusion & Engineering Takeaways

1. **Bare-metal dominance**: Proxmox VE (Type-1) delivers **+25.90% higher CPU throughput** and **20.59% lower average latency** compared to VMware Workstation (Type-2).
2. **Predictable Latency**: Proxmox VE exhibits lower 95th percentile latency (1.63 ms vs 2.07 ms), making Type-1 hypervisors essential for enterprise workloads.
