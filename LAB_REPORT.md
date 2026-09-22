# LABORATORY EXPERIMENT REPORT

**Course Title:** Cloud Computing  
**Topic:** Empirical CPU Performance Benchmark Analysis of Type-1 (Bare-Metal) vs. Type-2 (Hosted) Hypervisors  
**Author / Repository Owner:** `chhavi-2006`  
**Repository:** [https://github.com/chhavi-2006/cloud_computing-](https://github.com/chhavi-2006/cloud_computing-)  
**Date:** September 2026  

---

## 1. Abstract

This laboratory experiment investigates the performance impact of hypervisor architecture on virtualized CPU execution. We provisioned two identical guest operating environments (Ubuntu 22.04.5 LTS, 2 vCPUs, 2 GB RAM, 20 GB Disk Allocation) across a Type-1 Bare-Metal Hypervisor (Proxmox VE / KVM) and a Type-2 Hosted Hypervisor (VMware Workstation on Windows OS). We conducted CPU stress testing using `sysbench --cpu-max-prime=20000` to measure total execution time, total events completed, events per second (throughput), and execution latency (minimum, average, 95th percentile, and maximum). The empirical results demonstrate that Proxmox VE (Type-1) achieved **981.14 Events/sec** versus **779.24 Events/sec** on VMware Workstation (Type-2), representing a **+25.91% throughput advantage**, a **20.31% reduction in average latency**, and a **32.62% reduction in peak latency spikes**.

---

## 2. Experimental Objectives

1. Deploy identical Linux virtual machines across Type-1 (Proxmox VE) and Type-2 (VMware Workstation) hypervisors.
2. Maintain strict control parameters: 2 vCPU, 2048 MB RAM, 20 GB Virtual Disk.
3. Quantify virtualization overhead using the standardized `sysbench` CPU prime number calculation benchmark up to 20,000 prime numbers.
4. Evaluate throughput and latency distribution metrics.
5. Provide technical analysis explaining architectural causes for performance differences.

---

## 3. System Architecture & Resource Allocation

### 3.1 Hardware & Software Specifications Table

| Metric / Parameter | Type-1 Bare-Metal Hypervisor | Type-2 Hosted Hypervisor | Standardization Status |
| :--- | :--- | :--- | :--- |
| **Hypervisor Solution** | Proxmox VE (Linux KVM) | VMware Workstation Pro | Tested Platform |
| **Host Environment** | Bare-Metal Hardware | Windows Host OS | Evaluated Architecture |
| **Guest Hostname** | `type1-virtual-machine` | `type2-virtual-machine` | Verified via `hostnamectl` |
| **Guest OS Distribution** | Ubuntu 22.04.5 LTS (x86_64) | Ubuntu 22.04.5 LTS (x86_64) | Identical OS Kernel |
| **Linux Kernel** | 6.8.0-138-generic | 6.8.0-138-generic | Identical System Kernel |
| **Virtual CPUs** | 2 vCPU | 2 vCPU | Identical Compute Allocation |
| **Memory Allocation** | 2048 MiB (2 GB) | 2048 MB (2 GB) | Identical RAM Allocation |
| **Disk Storage** | 20.0 GB VirtIO | 20.0 GB Virtual Disk | Identical Disk Allocation |
| **Benchmark Suite** | Sysbench 1.0.20 | Sysbench 1.0.20 | Standardized Tool |

---

## 4. Empirical Data & Benchmarking Results

### 4.1 Benchmark Summary Table

| Benchmark Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Absolute Delta | Percentage Delta | Superior Platform |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Total Execution Time** | **10.0006 s** | **10.0013 s** | -0.0007 s | -0.007% | Standardized ~10s |
| **Total Events Processed** | **9,812** | **7,795** | **+2,017 events** | **+25.88%** | **Proxmox VE (Type-1)** |
| **Events per Second (EPS)** | **981.14** | **779.24** | **+201.90 eps** | **+25.91%** | **Proxmox VE (Type-1)** |
| **Minimum Latency** | **0.92 ms** | **1.16 ms** | **-0.24 ms** | **-20.69%** | **Proxmox VE (Faster)** |
| **Average Latency** | **1.02 ms** | **1.28 ms** | **-0.26 ms** | **-20.31%** | **Proxmox VE (Lower)** |
| **95th Percentile Latency** | **1.14 ms** | **1.45 ms** | **-0.31 ms** | **-21.38%** | **Proxmox VE (Consistent)** |
| **Maximum Latency** | **2.85 ms** | **4.23 ms** | **-1.38 ms** | **-32.62%** | **Proxmox VE (Fewer Spikes)** |

---

## 5. Performance Visualizations

### 5.1 Throughput & Latency Figures

1. **Figure 1 (`images/1.png`)**: Guest VM `hostnamectl` terminal system report.
2. **Figure 2 (`images/2.png`)**: Type-2 Hypervisor Performance Results Table.
3. **Figure 3 (`images/3.png`)**: Benchmark Observation Parameters Table.
4. **Figure 4 (`images/events_per_second_comparison.png`)**: Throughput (EPS) Bar Chart (+25.91% gain).
5. **Figure 5 (`images/latency_comparison.png`)**: Latency Metrics Comparison Bar Chart (Min, Avg, 95th Pct, Max).
6. **Figure 6 (`images/total_events_comparison.png`)**: Total Events Completed Bar Chart.
7. **Figure 7 (`images/overall_performance_dashboard.png`)**: 4-Panel Performance Dashboard.

---

## 6. Discussion & Technical Findings

1. **Direct Hardware Execution vs Hosted Emulation**: Type-1 hypervisors execute CPU virtualization using hardware VT-x/AMD-V instructions directly, bypassing host OS context switches. Type-2 hypervisors must process instructions through a VMM application layer on top of a desktop operating system (Windows NT kernel).
2. **Thread Scheduling Impact**: Linux KVM maps guest vCPUs to host kernel threads managed by the Completely Fair Scheduler (CFS). VMware Workstation guest threads contend with host Windows processes, resulting in higher latency spikes (4.23 ms vs 2.85 ms max latency).

---

## 7. Conclusion

The experimental findings confirm that **Type-1 Bare-Metal Hypervisors (Proxmox VE)** outperform **Type-2 Hosted Hypervisors (VMware Workstation)** across all compute efficiency metrics, yielding **+25.91% higher CPU throughput** and **20.31% lower average latency**.
