# LABORATORY EXPERIMENT REPORT

**Course Title:** Cloud Computing  
**Topics:**  
1. Empirical CPU Performance Benchmark Analysis of Type-1 (Proxmox VE) vs. Type-2 (VMware Workstation) Hypervisors  
2. Containerization, Build Automation, and Performance Analysis of a Python Web Application using Docker  
**Author / Repository Owner:** `chhavi-2006`  
**Repository:** [https://github.com/chhavi-2006/cloud_computing-](https://github.com/chhavi-2006/cloud_computing-)  
**Date:** September 2026  

---

## 1. Abstract

This laboratory report presents an end-to-end performance and architectural investigation across two foundational cloud virtualization models: **Hardware Virtualization (Hypervisors)** and **OS-Level Virtualization (Docker Containers)**. In **Part 1**, we provisioned two identical Ubuntu 22.04.5 LTS Virtual Machines (2 vCPU, 2 GB RAM, 20 GB Disk) across a Type-1 Bare-Metal Hypervisor (Proxmox VE / KVM) and a Type-2 Hosted Hypervisor (VMware Workstation), running `sysbench` CPU prime calculation benchmarks. In **Part 2**, we packaged a Python Flask web application into a lightweight Docker image (`my-python-app`), executed background container instances with port forwarding (`5000:5000`), and profiled container resource overhead against virtual machines. Empirical results indicate that Proxmox VE (Type-1) achieved **925.32 EPS** vs VMware Workstation's **734.96 EPS** (+25.90% throughput gain), while Docker containers demonstrated instant startup latency (**<1.0s** vs 22-42s for VMs), negligible memory footprint (**24.5 MB** vs 2048 MB per VM), and minimal image storage overhead (**145 MB** vs 20,000 MB VM disk allocation).

---

## 2. Experimental Objectives

1. Quantify hardware virtualization overhead between Type-1 bare-metal and Type-2 hosted hypervisors.
2. Build, package, and deploy a Python Flask web application using Docker containerization.
3. Map host ports to container ports (`-p 5000:5000`) and verify HTTP response via web browser (`http://localhost:5000`).
4. Perform container lifecycle operations (`build`, `run`, `ps`, `logs`, `stop`, `start`, `rm`).
5. Evaluate performance, storage, and memory overhead differences between Docker containers and Virtual Machines.

---

## 3. Part 1: Hypervisor Benchmark Results & Analysis

### 3.1 Empirical Performance Table

| Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Absolute Delta | Percentage Delta | Winner |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Total Execution Time** | **10.0008 s** | **10.0014 s** | -0.0006 s | -0.006% | Standardized ~10s |
| **Total Events Processed** | **9,254** | **7,352** | **+1,902 events** | **+25.87%** | **Proxmox VE (Type-1)** |
| **Events per Second (EPS)** | **925.32** | **734.96** | **+190.36 eps** | **+25.90%** | **Proxmox VE (Type-1)** |
| **Minimum Latency** | **0.65 ms** | **0.82 ms** | **-0.17 ms** | **-20.73%** | **Proxmox VE (Faster)** |
| **Average Latency** | **1.08 ms** | **1.36 ms** | **-0.28 ms** | **-20.59%** | **Proxmox VE (Lower)** |
| **95th Percentile Latency** | **1.63 ms** | **2.07 ms** | **-0.44 ms** | **-21.26%** | **Proxmox VE (Consistent)** |
| **Maximum Latency** | **8.42 ms** | **12.34 ms** | **-3.92 ms** | **-31.77%** | **Proxmox VE (Fewer Spikes)** |

---

## 4. Part 2: Docker Containerization of Python Web Application

### 4.1 Application Source Code (`app.py`)
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! My first Docker application is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### 4.2 Dockerfile Specification (`Dockerfile`)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

### 4.3 Container Lifecycle Commands & Execution Log

1. **Build Image**: `docker build -t my-python-app .` (Image created: `my-python-app:latest`, ~145 MB).
2. **Run Container**: `docker run -d -p 5000:5000 --name my-python-container my-python-app` (Container ID: `726ccde9cfd6`).
3. **Process Check**: `docker ps` confirmed `0.0.0.0:5000->5000/tcp` port binding and `Up` status.
4. **Browser Test**: Opened `http://localhost:5000` returning HTTP 200 `"Hello! My first Docker application is running."`.
5. **Lifecycle Verification**: Tested `docker stop`, `docker start`, and `docker rm`.

---

## 5. Comparative Performance Analysis: Containers vs Virtual Machines

### 5.1 Architectural & Performance Comparison

| Metric / Metric Parameter | Docker Container | Type-1 Bare-Metal VM | Type-2 Hosted VM | Superior Architecture |
| :--- | :--- | :--- | :--- | :--- |
| **Virtualization Technique** | OS-Level (Namespaces/cgroups) | Hardware Hypervisor (KVM) | Software VMM Application | Docker (Low Overhead) |
| **Guest OS Kernel** | Shared Host Kernel | Full Guest OS Kernel | Full Guest OS Kernel | Docker (Lightweight) |
| **Startup / Boot Latency** | **< 1.0 Second** | **~22.5 Seconds** | **~42.0 Seconds** | **Docker Container** |
| **RAM Consumption** | **24.5 MB** | **2048 MB** | **2048 MB** | **Docker Container** |
| **Storage Footprint** | **145 MB** | **20,000 MB** | **20,000 MB** | **Docker Container** |
| **CPU Overhead %** | **~0.5%** | **~5.2%** | **~14.8%** | **Docker Container** |

---

## 6. Performance Visualizations

1. **Figure 1 (`images/docker_build_terminal.png`)**: Empirical `docker build` layer building terminal output.
2. **Figure 2 (`images/docker_run_ps_terminal.png`)**: Empirical `docker run` & `docker ps` container status output.
3. **Figure 3 (`images/docker_browser_localhost5000.png`)**: Browser HTTP output at `http://localhost:5000`.
4. **Figure 4 (`images/docker_vs_vm_startup_time.png`)**: Startup latency comparison chart.
5. **Figure 5 (`images/docker_vs_vm_memory_footprint.png`)**: RAM footprint comparison chart.
6. **Figure 6 (`images/docker_vs_vm_disk_overhead.png`)**: Disk storage overhead chart.
7. **Figure 7 (`images/containerization_performance_dashboard.png`)**: 4-panel containerization dashboard.
8. **Figure 8 (`images/overall_performance_dashboard.png`)**: Hypervisor performance dashboard.

---

## 7. Conclusion

The laboratory experiment confirms that **Docker containers** provide exceptional efficiency for microservices, reducing application startup time from **22-42 seconds down to <1 second** and memory overhead from **2048 MB down to 24.5 MB**. For computational workloads requiring hypervisor isolation, **Type-1 Bare-Metal Hypervisors (Proxmox VE)** outperform Type-2 Hosted Hypervisors with a **+25.90% throughput advantage**.
