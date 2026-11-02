# Cloud Computing & Virtualization Laboratory Suite

[![Course](https://img.shields.io/badge/Course-Cloud%20Computing-blue.svg)](#)
[![Student](https://img.shields.io/badge/Student-Chhavi%20Mishra-purple.svg)](#)
[![USN](https://img.shields.io/badge/USN-01fe24bci066-green.svg)](#)
[![Roll%20No](https://img.shields.io/badge/Roll%20No-136-orange.svg)](#)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.37.0-326CE5.svg?logo=kubernetes&logoColor=white)](#)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)](#)

Welcome to the **Cloud Computing Laboratory Suite** repository maintained by **Chhavi Mishra** (USN: `01fe24bci066`, Roll No: `136`). This repository contains complete, standalone cloud infrastructure, hypervisor, containerization, and Kubernetes cluster orchestration benchmark experiments, complete with empirical data, terminal screenshots, visualization dashboards, source code, and technical reports.

---

## 📂 Laboratory Experiments Index

| Experiment ID | Title | Domain / Focus | Dedicated Documentation | Key Result |
| :--- | :--- | :--- | :--- | :--- |
| **Experiment 1** | **Type-1 vs Type-2 Hypervisor Performance Analysis** | Hardware Virtualization (KVM vs VMware) | 📖 [**`HYPERVISOR_README.md`**](HYPERVISOR_README.md) | Proxmox VE (Type-1) achieved **+25.90% higher throughput** and **20.59% lower latency** than VMware Workstation (Type-2). |
| **Experiment 2** | **Dockerizing Python Web Application & Deployment** | OS-Level Virtualization (Docker Containers) | 📖 [**`docker-python-app/README.md`**](docker-python-app/README.md) | Docker containers started in **<1.0s** (50x faster than VMs), using **24.5 MB RAM** (83x smaller) and **145 MB storage**. |
| **Experiment 3** | **Virtual Machines vs Containers (CPU & Memory)** | Sysbench Workload Profiling (VM vs Docker) | 📖 [**`VMs-vs-Containers/README.md`**](VMs-vs-Containers/README.md) | Docker achieved **123,725.89 MiB/s** memory transfer rate vs VM **108,900.87 MiB/s** (**+13.61% faster throughput**). |
| **Experiment 4** | **Kubernetes Cluster Scheduling, Scaling & Self-Healing** | Container Orchestration (KinD, K8s, NGINX) | 📖 [**`kubernetes-cluster/README.md`**](kubernetes-cluster/README.md) | Built a 3-node K8s cluster on Windows; demonstrated 50/50 multi-worker pod balancing (6 replicas) and **<5s automated self-healing**. |

---

## 📊 Summary Comparison: Bare-Metal vs Hypervisors vs Containers vs Orchestration

| Benchmark / Capability Parameter | Docker Container | Type-1 Bare-Metal VM | Type-2 Hosted VM | Kubernetes Cluster Orchestration | Advantage / Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Virtualization Model** | OS-Level Virtualization | Hardware Hypervisor (KVM) | Software VMM Application | Container Orchestrator (K8s on Docker/WSL2) | Kubernetes: Multi-node automated scheduling & lifecycle |
| **Memory Throughput** | **123,725.89 MiB/s** | **118,500.00 MiB/s** | **108,900.87 MiB/s** | Native Container Throughput | Docker Container (+13.61%) |
| **Max Latency Spikes** | **1.13 ms** | **2.78 ms** | **3.04 ms** | Flat CNI Pod Networking | Docker Container (-62.8%) |
| **Startup / Boot Time** | **< 1.0 Second** | **~22.5 Seconds** | **~42.0 Seconds** | **~5.0s Pod Re-spawning** | Docker (<1.0s) / K8s Self-Healing (<5s) |
| **RAM Footprint** | **~24.5 MB** | **2048 MB** | **2048 MB** | Lightweight per Pod (~20-30 MB) | Docker / Kubernetes Containers |
| **Disk Storage Size** | **~145 MB** | **20,000 MB** | **20,000 MB** | Shared Base Node Image (`v1.37.0`) | Minimal disk allocation |
| **Fault Tolerance** | Manual restart | VM High Availability | Manual restart | **Automated ReplicaSet Self-Healing** | **Kubernetes (Zero-touch automated recovery)** |
| **Elastic Scalability** | Manual `docker run` | Manual VM clone | Manual VM clone | **Horizontal Auto/Manual Scaling (`kubectl scale`)**| **Kubernetes (Dynamic multi-node distribution)** |

---

## 📁 Repository Directory Structure

```
cloud_computing-/
│
├── README.md                                  # Repository Hub & Experiments Index
├── LAB_REPORT.md                              # Combined Academic Lab Report Submission
├── HYPERVISOR_README.md                       # Standalone Report for Experiment 1 (Hypervisors)
│
├── kubernetes-cluster/                        # Standalone Folder for Experiment 4 (Kubernetes Cluster)
│   ├── README.md                              # Exhaustive Technical Report for Experiment 4
│   ├── kind-config.yaml                       # 3-Node KinD Cluster Manifest (1 control plane, 2 workers)
│   ├── Kubernetes_Lab_on_Windows_Manual.pdf   # Reference Lab Manual (Steps 1–6)
│   ├── Experiment_4_Kubernetes_Cluster_Scheduling_and_Self_Healing_Report.docx # Word Report
│   └── images/                                # Empirical Screenshots for Kubernetes Lab
│       ├── k8s_wsl_status.png
│       ├── k8s_nodes_docker_ps.png
│       ├── k8s_pods_3replicas.png
│       ├── k8s_pods_6replicas.png
│       ├── k8s_pod_delete_self_healing.png
│       └── k8s_self_healing_healed.png
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
