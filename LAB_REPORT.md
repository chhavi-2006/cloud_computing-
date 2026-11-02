# LABORATORY EXPERIMENT REPORT

**Course Title:** Cloud Computing  
**Topics:**  
1. Empirical CPU Performance Benchmark Analysis of Type-1 (Proxmox VE) vs. Type-2 (VMware Workstation) Hypervisors  
2. Containerization, Build Automation, and Performance Analysis of a Python Web Application using Docker  
3. Multi-Node Kubernetes Cluster Provisioning, Workload Scheduling, Horizontal Scaling, and ReplicaSet Self-Healing Fault Tolerance using KinD on Windows  
**Author / Repository Owner:** `chhavi-2006` (Chhavi Mishra)  
**USN:** `01fe24bci066` | **Roll No:** `136`  
**Repository:** [https://github.com/chhavi-2006/cloud_computing-](https://github.com/chhavi-2006/cloud_computing-)  
**Academic Term:** 5th Semester, 2026  

---

## 1. Abstract

This laboratory report presents an end-to-end performance and architectural investigation across three foundational cloud virtualization and orchestration tiers: **Hardware Virtualization (Hypervisors)**, **OS-Level Virtualization (Docker Containers)**, and **Container Orchestration (Kubernetes)**. In **Part 1**, we provisioned two identical Ubuntu 22.04.5 LTS Virtual Machines (2 vCPU, 2 GB RAM, 20 GB Disk) across a Type-1 Bare-Metal Hypervisor (Proxmox VE / KVM) and a Type-2 Hosted Hypervisor (VMware Workstation), running `sysbench` CPU prime calculation benchmarks. In **Part 2**, we packaged a Python Flask web application into a lightweight Docker image (`my-python-app`), executed background container instances with port forwarding (`5000:5000`), and profiled container resource overhead against virtual machines. In **Part 3**, we orchestrated a production-mode 3-node Kubernetes cluster (1 control-plane, 2 worker nodes) using KinD over WSL 2 on Windows, deployed an NGINX web service, performed horizontal scaling from 3 to 6 replicas with automated 50/50 multi-worker pod distribution, and experimentally validated declarative self-healing recovery (<5 seconds) upon deliberate pod failure injection.

Empirical results indicate that Proxmox VE (Type-1) achieved **925.32 EPS** vs VMware Workstation's **734.96 EPS** (+25.90% throughput gain), while Docker containers demonstrated instant startup latency (**<1.0s** vs 22-42s for VMs), negligible memory footprint (**24.5 MB** vs 2048 MB per VM), and minimal image storage overhead (**145 MB** vs 20,000 MB VM disk allocation). Kubernetes container orchestration successfully decoupled workload lifecycle from physical/virtual node constraints, maintaining desired replica counts automatically and distributing compute load evenly across worker nodes.

---

## 2. Experimental Objectives

1. Quantify hardware virtualization overhead between Type-1 bare-metal and Type-2 hosted hypervisors.
2. Build, package, and deploy a Python Flask web application using Docker containerization.
3. Map host ports to container ports (`-p 5000:5000`) and verify HTTP response via web browser (`http://localhost:5000`).
4. Perform container lifecycle operations (`build`, `run`, `ps`, `logs`, `stop`, `start`, `rm`).
5. Evaluate performance, storage, and memory overhead differences between Docker containers and Virtual Machines.
6. Provision a multi-node Kubernetes cluster (1 control plane, 2 workers) on Windows using KinD and Docker Desktop WSL 2.
7. Deploy, schedule, horizontally scale (3 to 6 replicas), and validate automated self-healing fault tolerance in Kubernetes.

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

## 5. Part 3: Kubernetes Multi-Node Cluster Orchestration, Workload Scheduling & Self-Healing

### 5.1 Architecture & Cluster Configuration (`kind-config.yaml`)

To evaluate container orchestration on a multi-node topology, KinD v0.33 was configured to instantiate a 3-node Kubernetes cluster inside Docker containers on WSL 2:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

Executing `kind create cluster --config kind-config.yaml` provisioned three Docker containers:
1. `kind-control-plane` (Container `6b16706fc603`, mapped API port `127.0.0.1:65242->6443/tcp`).
2. `kind-worker` (Container `317ce8f4adcf`, CNI subnet `10.244.2.0/24`).
3. `kind-worker2` (Container `fe5c2984d1b3`, CNI subnet `10.244.1.0/24`).

All three nodes successfully joined the cluster running Kubernetes `v1.37.0` with `Ready` status.

### 5.2 NGINX Deployment & Initial Pod Scheduling (3 Replicas)

Running `kubectl create deployment web --image=nginx --replicas=3` instructed the `kube-controller-manager` to instantiate 3 pods. `kube-scheduler` assigned pods across available worker nodes:
- `web-5fc9f4bf66-lrvv7` (`10.244.2.3`) scheduled to `kind-worker`.
- `web-5fc9f4bf66-w9rd5` (`10.244.2.2`) scheduled to `kind-worker`.
- `web-5fc9f4bf66-rrnwx` (`10.244.1.2`) scheduled to `kind-worker2`.

### 5.3 Horizontal Workload Scaling (6 Replicas)

Scaling the deployment via `kubectl scale deployment web --replicas=6` triggered the scheduler's least-allocated / anti-affinity scoring algorithm. The cluster achieved an exact 50% / 50% load distribution:
- **`kind-worker` (3 pods)**: `hpncv` (10.244.2.4), `lrvv7` (10.244.2.3), `w9rd5` (10.244.2.2).
- **`kind-worker2` (3 pods)**: `9jr2v` (10.244.1.3), `j5dv4` (10.244.1.4), `rrnwx` (10.244.1.2).

### 5.4 Fault Injection & Automated Self-Healing Verification

To experimentally verify declarative self-healing:
1. Pod `web-5fc9f4bf66-lrvv7` was deliberately deleted (`kubectl delete pod web-5fc9f4bf66-lrvv7`).
2. The `ReplicaSet` control loop immediately registered a deficit: desired = 6, actual = 5.
3. Within **5 seconds**, the controller scheduled replacement pod **`web-5fc9f4bf66-49nq9`**.
4. Once the image layers initialized, the replacement pod transitioned to **`1/1 Running`**, restoring the cluster to 6/6 healthy replicas without administrative intervention.

---

## 6. Comprehensive Comparative Analysis

| Feature / Metric | Type-2 Hosted VM (VMware) | Type-1 Bare-Metal VM (Proxmox) | Docker Container | Kubernetes Cluster Orchestration |
| :--- | :--- | :--- | :--- | :--- |
| **Virtualization Level** | Host OS Application | Hardware Hypervisor | OS Kernel Namespaces/cgroups | Distributed Container Cluster |
| **Guest Kernel** | Complete Guest OS | Complete Guest OS | Shared Host Linux Kernel | Shared Node Kernel via CNI SDN |
| **Startup / Provisioning Time**| ~42.0 seconds | ~22.5 seconds | **< 1.0 second** | **< 5.0 seconds (Self-Healing)** |
| **Memory Allocation** | 2048 MB | 2048 MB | **24.5 MB** | Dynamic pod requests/limits |
| **Disk Image Size** | 20,000 MB | 20,000 MB | **145 MB** | Layer-shared node container image |
| **Fault Recovery** | Manual intervention | High-availability cluster restart | Restart policy / manual | **Automated Zero-Touch Self-Healing** |
| **Horizontal Elasticity** | Slow VM cloning | Automated VM templates | Scripted container run | **Declarative `kubectl scale` / HPA** |

---

## 7. Experimental Visualizations & Evidence

1. **Figure 1 (`images/docker_build_terminal.png`)**: Empirical `docker build` layer building terminal output.
2. **Figure 2 (`images/docker_run_ps_terminal.png`)**: Empirical `docker run` & `docker ps` container status output.
3. **Figure 3 (`images/docker_browser_localhost5000.png`)**: Browser HTTP output at `http://localhost:5000`.
4. **Figure 4 (`images/docker_vs_vm_startup_time.png`)**: Startup latency comparison chart.
5. **Figure 5 (`images/docker_vs_vm_memory_footprint.png`)**: RAM footprint comparison chart.
6. **Figure 6 (`images/docker_vs_vm_disk_overhead.png`)**: Disk storage overhead chart.
7. **Figure 7 (`images/containerization_performance_dashboard.png`)**: 4-panel containerization dashboard.
8. **Figure 8 (`images/overall_performance_dashboard.png`)**: Hypervisor performance dashboard.
9. **Figure 9 (`images/k8s_wsl_status.png`)**: WSL 2 engine status and Docker Desktop distribution verification.
10. **Figure 10 (`images/k8s_nodes_docker_ps.png`)**: 3-node Kubernetes cluster status (`kubectl get nodes`) and backing Docker containers (`docker ps`).
11. **Figure 11 (`images/k8s_pods_3replicas.png`)**: Initial 3-replica NGINX deployment and pod-to-node placement.
12. **Figure 12 (`images/k8s_pods_6replicas.png`)**: Scaled 6-replica deployment demonstrating balanced multi-worker distribution.
13. **Figure 13 (`images/k8s_pod_delete_self_healing.png`)**: Deliberate pod deletion and immediate automated self-healing recreation (<5 seconds).
14. **Figure 14 (`images/k8s_self_healing_healed.png`)**: Final cluster pod inventory confirming steady-state 6/6 running pods.

---

## 8. Conclusion

This laboratory course suite confirms the distinct operational advantages of cloud virtualization and orchestration tiers:
1. **Hypervisors**: Type-1 bare-metal hypervisors (Proxmox VE) demonstrate clear CPU execution superiority over Type-2 hosted hypervisors (+25.90% throughput, -20.59% latency).
2. **Containers**: Docker containers deliver unmatched execution efficiency, dropping startup latency from tens of seconds to under 1 second, and reducing memory usage by 83x.
3. **Container Orchestration**: Kubernetes elevates containers into production-ready resilient cloud systems, providing automated declarative reconciliation, multi-node compute distribution, horizontal elasticity, and self-healing fault tolerance.
