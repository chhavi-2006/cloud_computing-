# LABORATORY EXPERIMENT REPORT

**Course Title:** Cloud Computing  
**Topics:**  
1. Empirical CPU Performance Benchmark Analysis of Type-1 (Proxmox VE) vs. Type-2 (VMware Workstation) Hypervisors  
2. Containerization, Build Automation, and Lifecycle Management of a Python Web Application using Docker  
3. Multi-Node Kubernetes Cluster Provisioning, Workload Scheduling, Horizontal Scaling, and ReplicaSet Self-Healing Fault Tolerance using KinD on Windows  
4. Declarative Infrastructure as Code (IaC) Automation, State Management, and Resource Lifecycle using HashiCorp Terraform on Windows  
**Author / Repository Owner:** `chhavi-2006` (Chhavi Mishra)  
**USN:** `01fe24bci066` | **Roll No:** `136`  
**Repository:** [https://github.com/chhavi-2006/cloud_computing-](https://github.com/chhavi-2006/cloud_computing-)  
**Academic Term:** 5th Semester, 2026  

---

## 1. Abstract

This laboratory report presents an end-to-end performance and architectural investigation across three foundational cloud virtualization and orchestration tiers: **Hardware Virtualization (Hypervisors)**, **OS-Level Virtualization (Docker Containers)**, and **Container Orchestration (Kubernetes)**. In **Part 1**, we provisioned two identical Ubuntu 22.04.5 LTS Virtual Machines (2 vCPU, 2 GB RAM, 20 GB Disk) across a Type-1 Bare-Metal Hypervisor (Proxmox VE / KVM) and a Type-2 Hosted Hypervisor (VMware Workstation), running `sysbench` CPU prime calculation benchmarks. In **Part 2**, we packaged a Python Flask web application into a lightweight Docker image (`my-python-app`), executed background container instances with port forwarding (`5000:5000` and `5001:5000`), explored internal filesystems via interactive shell (`docker exec -it /bin/sh`), evaluated state retention across stop/start cycles (`6c755d50ded2`), verified clean container deletion (`docker rm`), proved Docker image immutability, and profiled container resource overhead against virtual machines. In **Part 3**, we orchestrated a production-mode 3-node Kubernetes cluster (1 control-plane, 2 worker nodes) using KinD over WSL 2 on Windows, deployed an NGINX web service, performed horizontal scaling from 3 to 6 replicas with automated 50/50 multi-worker pod distribution, and experimentally validated declarative self-healing recovery (<5 seconds) upon deliberate pod failure injection.

Empirical results indicate that Proxmox VE (Type-1) achieved **925.32 EPS** vs VMware Workstation's **734.96 EPS** (+25.90% throughput gain), while Docker containers demonstrated instant startup latency (**<1.0s** vs 22-42s for VMs), negligible memory footprint (**24.5 MB** vs 2048 MB per VM), and minimal image storage overhead (**145 MB** vs 20,000 MB VM disk allocation). Kubernetes container orchestration successfully decoupled workload lifecycle from physical/virtual node constraints, maintaining desired replica counts automatically and distributing compute load evenly across worker nodes.

---

## 2. Experimental Objectives

1. Quantify hardware virtualization overhead between Type-1 bare-metal and Type-2 hosted hypervisors.
2. Build, package, and deploy a Python Flask web application using Docker containerization.
3. Map host ports to container ports (`-p 5000:5000` and `-p 5001:5000`) and verify HTTP responses via web browser and PowerShell `Invoke-WebRequest`.
4. Perform end-to-end container lifecycle operations (`build`, `run`, `ps`, `logs`, `inspect`, interactive shell `exec`, `stop`, `start`, `rm`) and prove base image immutability.
5. Evaluate performance, storage, and memory overhead differences between Docker containers and Virtual Machines.
6. Provision a multi-node Kubernetes cluster (1 control plane, 2 workers) on Windows using KinD and Docker Desktop WSL 2.
7. Deploy, schedule, horizontally scale (3 to 6 replicas), and validate automated self-healing fault tolerance in Kubernetes.
8. Declare, validate, plan, apply, modify, and destroy local infrastructure resources using HashiCorp Terraform on Windows PowerShell.

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

## 4. Part 2: Docker Containerization of Python Web Application & Lifecycle Management

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

### 4.3 Phase 1: Build & Initial Deployment (Port 5000:5000)

1. **Build Image**: `docker build -t my-python-app .` (Image created: `my-python-app:latest`, ~145 MB).
2. **Run Container**: `docker run -d -p 5000:5000 --name my-python-container my-python-app` (Container ID: `726ccde9cfd6`).
3. **Process Check**: `docker ps` confirmed `0.0.0.0:5000->5000/tcp` port binding and `Up` status.
4. **Browser Test**: Opened `http://localhost:5000` returning HTTP 200 `"Hello! My first Docker application is running."`.
5. **Resource Profiling**: Docker container memory footprint was **24.5 MB** vs **2048 MB** for VMs (83x smaller), starting in **<1.0s** vs 22-42s for hypervisors.

### 4.4 Phase 2: Container Lifecycle Operations, Port Forwarding (5001:5000) & Interactive Shell

Following the curriculum lab manual (*Experiment 2: Run, Test and Manage a Docker Container*), the pre-existing image `my-python-app` was reused to demonstrate container lifecycle management without rebuilding (documented in detail in [`docker-python-app/PART_2_README.md`](docker-python-app/PART_2_README.md)):

1. **Detached Run with Custom Port Binding**: `docker run -d -p 5001:5000 --name test-python-container my-python-app` instantiated container `6c755d50ded2`, mapping host port `5001` to internal Flask port `5000`.
2. **Multi-Channel HTTP Testing**: Verified service responsiveness via Google Chrome (`http://localhost:5001`) and PowerShell `Invoke-WebRequest http://localhost:5001`, both confirming HTTP 200 OK.
3. **Interactive Debugging Shell**: Attached to the active container via `docker exec -it test-python-container /bin/sh`. Executed `ls` (confirming `app.py` and `requirements.txt`) and `pwd` (confirming `WORKDIR /app`). Exited shell cleanly without stopping container.
4. **Graceful Stop & State Inspection**: Executed `docker stop test-python-container`. Inspected stopped state via `docker ps -a`, revealing `Exited (137)` while retaining container configuration and ID.
5. **Restart & ID Persistence**: Ran `docker start test-python-container`. Verified instant service recovery on port `5001` and confirmed Container ID `6c755d50ded2` was identical.
6. **Container Removal & Image Immutability**: Cleanly deallocated container via `docker stop` and `docker rm test-python-container`. Subsequent `docker images` query verified `my-python-app:latest` (200 MB) remained intact in the local repository.

### 4.5 Phase 3: Docker Hub Remote Registry Distribution (`chhavirajeshmishra/my-python-app:v1`)

Following the curriculum lab manual (*Experiment 3: Push a Docker Image to Docker Hub*), the local container image was published to Docker Hub to enable cross-machine deployment (documented in detail in [`docker-python-app/PART_3_README.md`](docker-python-app/PART_3_README.md)):

1. **CLI Authentication**: Executed `docker login` verifying credentials for user `chhavirajeshmishra` (`Login Succeeded`).
2. **Registry Namespace Tagging**: Executed `docker tag my-python-app chhavirajeshmishra/my-python-app:v1`. Verified that both tags shared the identical Image ID (`be84ed5367f1`), confirming zero additional disk usage.
3. **Layer-Based Push**: Executed `docker push chhavirajeshmishra/my-python-app:v1`. Common base layers were recognized as `Layer already exists`, streaming compressed application layers (49.1 MB) with final manifest digest `sha256:be84ed5367f1be082b4b991defdf9c5a4d1c7c62d30b774123f28d8ef5a123be`.
4. **Cloud Verification**: Verified online repository availability at `https://hub.docker.com/r/chhavirajeshmishra/my-python-app` with active tag `v1` ready for remote pulling (`docker pull chhavirajeshmishra/my-python-app:v1`).

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

## 6. Part 4: Infrastructure as Code (IaC) with HashiCorp Terraform

### 6.1 Architecture & Declarative Manifest (`main.tf`)
Terraform v1.17.2 was configured in `C:\Terraform-Lab` to manage local infrastructure using the `hashicorp/local` provider plugin (~> 2.9). The declarative HCL configuration declared a managed resource `local_file.student_file`:

```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
  }
}

resource "local_file" "student_file" {
  filename = "${path.module}/student.txt"
  content  = <<-EOT
    Welcome to Infrastructure as Code!
    Created using Terraform.
    This file is managed by Terraform.
  EOT
}
```

### 6.2 Execution Lifecycle Log & State Convergence (Part 1)
1. **Initialization (`terraform init`)**: Downloaded and cached provider plugin `hashicorp/local v2.9.0` and generated `.terraform.lock.hcl`.
2. **Validation (`terraform validate`)**: Validated configuration syntax returning `"Success! The configuration is valid."`.
3. **Speculative Planning (`terraform plan`)**: Evaluated real-world state vs desired state; generated plan: `1 to add, 0 to change, 0 to destroy`.
4. **Provisioning (`terraform apply`)**: Applied execution plan, created `student.txt` (`id=06e6ae35c344...`), and wrote state to `terraform.tfstate`.
5. **Modification & Drift Convergence**: Updated `main.tf` with a 4-line confirmation message and applied in-place updates (`id=926632173084...`). A subsequent `terraform apply` confirmed zero configuration drift (`No changes. Your infrastructure matches the configuration`).
6. **Automated Destruction (`terraform destroy`)**: De-provisioned resource; `Test-Path .\student.txt` returned `False`, confirming complete resource reclamation (documented in detail in [`terraform-iac/README.md`](terraform-iac/README.md)).

### 6.3 Part 2: Multi-Container Orchestration with Docker Provider
To extend IaC to real-world container runtimes, Terraform was configured in `C:\terraform-multiple-containers` using the `kreuzwerker/docker` provider plugin (`~> 3.0`, resolved to `v3.9.0`). The configuration declared two heterogeneous containerized microservices:
1. **NGINX Web Server**: Pulled `nginx:alpine` and instantiated container `terraform-nginx` mapping container port `80` to host port `8082`.
2. **Python HTTP File Server**: Pulled `python:3.12-slim` and instantiated container `terraform-python`, executing `["python", "-m", "http.server", "8000"]` with port mapping `8081 -> 8000`.

```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}
provider "docker" {}

resource "docker_image" "nginx" { name = "nginx:alpine" }
resource "docker_image" "python" { name = "python:3.12-slim" }

resource "docker_container" "webserver" {
  name  = "terraform-nginx"
  image = docker_image.nginx.image_id
  ports { internal = 80; external = 8082 }
}

resource "docker_container" "python_app" {
  name    = "terraform-python"
  image   = docker_image.python.image_id
  command = ["python", "-m", "http.server", "8000"]
  ports { internal = 8000; external = 8081 }
}
```

### 6.4 Implicit DAG Dependencies & Empirical Verification
1. **Implicit Dependency Ordering**: By declaring `image = docker_image.nginx.image_id`, Terraform constructed a Directed Acyclic Graph (DAG) ensuring images are fetched before container creation starts.
2. **Speculative Plan**: `terraform plan` computed 4 additions (`Plan: 4 to add, 0 to change, 0 to destroy`).
3. **Execution & Port Resolution**: Applied plan via `terraform apply`. Port conflict avoidance was achieved by binding NGINX to external port `8082`.
4. **Runtime & Browser Verification**: Executed `docker ps`, confirming steady-state execution. Verified endpoints in browser: `http://localhost:8082` (NGINX "Welcome to nginx!") and `http://localhost:8081` (Python directory listing). Full documentation is available in [`terraform-iac/PART_2_README.md`](terraform-iac/PART_2_README.md).

---

## 7. Comprehensive Comparative Analysis

| Feature / Metric | Type-2 Hosted VM (VMware) | Type-1 Bare-Metal VM (Proxmox) | Docker Container | Kubernetes Cluster Orchestration | HashiCorp Terraform IaC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Virtualization / Abstraction Level** | Host OS Application | Hardware Hypervisor | OS Kernel Namespaces/cgroups | Distributed Container Cluster | Declarative Infrastructure Engine |
| **Target / Guest Kernel** | Complete Guest OS | Complete Guest OS | Shared Host Linux Kernel | Shared Node Kernel via CNI SDN | Target System / Cloud API Resources |
| **Startup / Provisioning Time**| ~42.0 seconds | ~22.5 seconds | **< 1.0 second** | **< 5.0 seconds (Self-Healing)** | **< 0.1 second (Local file) / API-driven** |
| **Memory Allocation** | 2048 MB | 2048 MB | **24.5 MB** | Dynamic pod requests/limits | Minimal CLI runtime (~35 MB) |
| **Disk Image / Footprint** | 20,000 MB | 20,000 MB | **145 MB** | Layer-shared node container image | Compact binary (~90 MB) + state file |
| **Fault Recovery & Convergence** | Manual intervention | High-availability cluster restart | Restart policy / manual | **Automated Zero-Touch Self-Healing** | **State Refresh & Reconciliation (`apply`)** |
| **Elasticity & Scalability** | Slow VM cloning | Automated VM templates | Scripted container run | **Declarative `kubectl scale` / HPA** | Declarative `count` / `for_each` replication |

---

## 8. Experimental Visualizations & Evidence

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
15. **Figure 15 (`images/docker_run_browser_localhost5001.png`)**: Detached container run (`test-python-container`) on port 5001 and browser verification (`http://localhost:5001`).
16. **Figure 16 (`images/docker_invoke_webrequest_port5001.png`)**: Programmatic HTTP verification via PowerShell `Invoke-WebRequest`.
17. **Figure 17 (`images/docker_exec_interactive_shell.png`)**: Interactive shell session (`docker exec -it /bin/sh`), `ls`, and working directory check (`pwd` -> `/app`).
18. **Figure 18 (`images/docker_stop_container.png`)**: Graceful container stop operation (`docker stop`) and running filter check (`docker ps`).
19. **Figure 19 (`images/docker_ps_all_stopped_exited.png`)**: Stopped container state verification (`docker ps -a`, status `Exited (137)`).
20. **Figure 20 (`images/docker_start_and_rm_lifecycle.png`)**: Container restart (`docker start`) and safe removal (`docker rm`).
21. **Figure 21 (`images/docker_images_persistence_check.png`)**: Base Docker image persistence and immutability check (`docker images`).
22. **Figure 22 (`images/docker_part3_login_succeeded.png`)**: Docker CLI authentication with Docker Hub (`docker login` -> `Login Succeeded`).
23. **Figure 23 (`images/docker_part3_tag_verification.png`)**: Image namespace tagging and Image ID consistency check (`docker tag` & `docker images`).
24. **Figure 24 (`images/docker_part3_push_terminal.png`)**: Layer push execution and SHA256 digest output (`docker push`).
25. **Figure 25 (`images/docker_part3_hub_portal_verification.png`)**: Docker Hub online web console repository verification (`chhavirajeshmishra/my-python-app`).
26. **Figure 26 (`images/terraform_validate_and_plan.png`)**: Configuration syntax validation (`terraform validate`) and execution plan generation (`terraform plan`).
27. **Figure 27 (`images/terraform_apply_creation.png`)**: Managed resource provisioning and state creation (`terraform apply`).
28. **Figure 28 (`images/terraform_modify_drift_no_changes.png`)**: Configuration update verification and state drift convergence check (`0 added, 0 changed, 0 destroyed`).
29. **Figure 29 (`images/terraform_destroy_plan_prompt.png`)**: Teardown plan preview and destruction confirmation prompt (`terraform destroy`).
30. **Figure 30 (`images/terraform_destroy_complete_test_path.png`)**: Resource de-provisioning confirmation and filesystem clean verification (`Test-Path .\student.txt` -> `False`).
31. **Figure 31 (`images/terraform_p2_init_validate.png`)**: Docker provider initialization (`kreuzwerker/docker v3.9.0`) and syntax validation (`terraform validate` -> `Success!`).
32. **Figure 32 (`images/terraform_p2_plan_python_command.png`)**: Speculative execution plan for Python container specifying custom runtime command (`python -m http.server 8000`).
33. **Figure 33 (`images/terraform_p2_plan_python_ports.png`)**: Container network port binding for Python service (internal `8000` to external host `8081`).
34. **Figure 34 (`images/terraform_p2_plan_nginx_container.png`)**: Speculative execution plan for NGINX web server container (`terraform-nginx`).
35. **Figure 35 (`images/terraform_p2_plan_images_summary.png`)**: Docker image resource declarations (`nginx:alpine`, `python:3.12-slim`) and 4-resource addition plan summary.
36. **Figure 36 (`images/terraform_p2_apply_refresh_state.png`)**: Real-time state refresh against Docker Engine daemon during `terraform apply`.
37. **Figure 37 (`images/terraform_p2_apply_complete.png`)**: Creation completion in 3 seconds (`id=82e487287240...`) and `Apply complete! Resources: 1 added, 0 changed, 0 destroyed.`
38. **Figure 38 (`images/terraform_p2_docker_ps.png`)**: Docker process table inspection (`docker ps`) confirming `terraform-nginx` and `terraform-python` running healthy.
39. **Figure 39 (`images/terraform_p2_browser_nginx_8082.png`)**: Live HTTP web browser verification of NGINX on `http://localhost:8082` ("Welcome to nginx!").
40. **Figure 40 (`images/terraform_p2_browser_python_8081.png`)**: Live HTTP web browser verification of Python HTTP server on `http://localhost:8081` (Directory listing for `/`).

---

## 9. Conclusion

This laboratory course suite confirms the distinct operational advantages of cloud virtualization, orchestration, and infrastructure automation tiers:
1. **Hypervisors**: Type-1 bare-metal hypervisors (Proxmox VE) demonstrate clear CPU execution superiority over Type-2 hosted hypervisors (+25.90% throughput, -20.59% latency).
2. **Containers**: Docker containers deliver unmatched execution efficiency, dropping startup latency from tens of seconds to under 1 second, and reducing memory usage by 83x.
3. **Container Orchestration**: Kubernetes elevates containers into production-ready resilient cloud systems, providing automated declarative reconciliation, multi-node compute distribution, horizontal elasticity, and self-healing fault tolerance.
4. **Infrastructure as Code (IaC)**: HashiCorp Terraform enforces declarative infrastructure lifecycle automation across both local OS resources and containerized microservices. Through provider plugins (`hashicorp/local`, `kreuzwerker/docker`), Terraform manages dependency graphs (DAG), tracks state persistence (`terraform.tfstate`), guarantees idempotency, detects configuration drift, and ensures automated clean teardown.
