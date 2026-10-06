# Cloud Computing & Virtualization Laboratory Suite

[![Course](https://img.shields.io/badge/Course-Cloud%20Computing-blue.svg)](#)
[![Student](https://img.shields.io/badge/Student-Chhavi%20Mishra-purple.svg)](#)
[![USN](https://img.shields.io/badge/USN-01fe24bci066-green.svg)](#)
[![Roll%20No](https://img.shields.io/badge/Roll%20No-136-orange.svg)](#)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)](#)

Welcome to the **Cloud Computing Laboratory Suite** repository maintained by **Chhavi Mishra** (USN: `01fe24bci066`, Roll No: `136`). This repository contains complete, standalone cloud infrastructure, hypervisor, and containerization benchmark experiments, complete with empirical data, terminal screenshots, visualization dashboards, source code, and technical reports.

---

## 📂 Laboratory Experiments Index

| Experiment ID | Title | Domain / Focus | Dedicated Documentation | Key Result |
| :--- | :--- | :--- | :--- | :--- |
| **Experiment 1** | **Type-1 vs Type-2 Hypervisor Performance Analysis** | Hardware Virtualization (KVM vs VMware) | 📖 [**`HYPERVISOR_README.md`**](HYPERVISOR_README.md) | Proxmox VE (Type-1) achieved **+25.90% higher throughput** and **20.59% lower latency** than VMware Workstation (Type-2). |
| **Experiment 2** | **Dockerizing Python Web Application & Deployment** | OS-Level Virtualization (Docker Containers) | 📖 [**`docker-python-app/README.md`**](docker-python-app/README.md) | Docker containers started in **<1.0s** (50x faster than VMs), using **24.5 MB RAM** (83x smaller) and **145 MB storage**. |
| **Experiment 3** | **Virtual Machines vs Containers (CPU & Memory)** | Sysbench Workload Profiling (VM vs Docker) | 📖 [**`VMs-vs-Containers/README.md`**](VMs-vs-Containers/README.md) | Docker achieved **123,725.89 MiB/s** memory transfer rate vs VM **108,900.87 MiB/s** (**+13.61% faster throughput**). |

---

## 📊 Summary Comparison: Bare-Metal vs Hypervisors vs Docker Containers

| Benchmark Parameter | Docker Container | Type-1 Bare-Metal VM | Type-2 Hosted VM | Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **Virtualization Model** | OS-Level Virtualization | Hardware Hypervisor (KVM) | Software VMM Application | Docker (Low Overhead) |
| **Memory Throughput** | **123,725.89 MiB/s** | **118,500.00 MiB/s** | **108,900.87 MiB/s** | **Docker Container (+13.61%)** |
| **Max Latency Spikes** | **1.13 ms** | **2.78 ms** | **3.04 ms** | **Docker Container (-62.8%)** |
| **Startup / Boot Time** | **< 1.0 Second** | **~22.5 Seconds** | **~42.0 Seconds** | **Docker (50x-52x Faster)** |
| **RAM Footprint** | **~24.5 MB** | **2048 MB** | **2048 MB** | **Docker (83x Smaller)** |
| **Disk Storage Size** | **~145 MB** | **20,000 MB** | **20,000 MB** | **Docker (137x Smaller)** |

---

## 📁 Repository Directory Structure

```
cloud_computing-/
│
├── README.md                                  # Repository Hub & Experiments Index
├── LAB_REPORT.md                              # Combined Academic Lab Report Submission
├── HYPERVISOR_README.md                       # Standalone Report for Experiment 1 (Hypervisors)
│
├── docker-python-app/                         # Standalone Folder for Experiment 2 (Docker App)
│   ├── README.md                              # Standalone Report for Experiment 2 (Docker App)
│   ├── app.py                                 # Flask Web Application Code
│   ├── requirements.txt                       # Python Dependencies
│   ├── Dockerfile                             # Docker Build Configuration
│   └── .dockerignore                          # Context Exclusion Rules
│
├── VMs-vs-Containers/                         # Standalone Folder for Experiment 3 (VMs vs Containers)
│   ├── README.md                              # Standalone Report for VMs vs Containers
│   ├── experiment-1-cpu-throughput.png        # Sysbench CPU Throughput Graph
│   ├── experiment-2-memory-throughput.png     # Sysbench Memory Throughput Graph
│   ├── Experiment_1_CPU_Performance_VM_vs_Container.pdf # Original Reference Manual
│   └── Experiment_2_Memory_Performance_Final.pdf       # Original Reference Manual
│
├── images/                                    # Screenshots & Performance Charts
└── scripts/                                   # Automation Scripts
```

---

## 👤 Student Metadata

- **Student Name**: Chhavi Mishra
- **USN**: `01fe24bci066`
- **Roll No**: `136`
- **Course**: Cloud Computing Laboratory
- **Repository Link**: [https://github.com/chhavi-2006/cloud_computing-](https://github.com/chhavi-2006/cloud_computing-)

---
*Laboratory Suite conducted for Cloud Computing Course.*
