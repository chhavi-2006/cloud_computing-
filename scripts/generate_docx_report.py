import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

doc = docx.Document()

# Page margins
sections = doc.sections
for s in sections:
    s.top_margin = Inches(0.8)
    s.bottom_margin = Inches(0.8)
    s.left_margin = Inches(0.8)
    s.right_margin = Inches(0.8)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def style_table(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        for j, cell in enumerate(row.cells):
            cell.paragraphs[0].paragraph_format.space_before = Pt(3)
            cell.paragraphs[0].paragraph_format.space_after = Pt(3)
            if col_widths and j < len(col_widths):
                cell.width = col_widths[j]
            if i == 0:
                set_cell_background(cell, '1F497D')
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, 'F2F5F8')
                else:
                    set_cell_background(cell, 'FFFFFF')

# Title
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(2)
run_exp = title_p.add_run('EXPERIMENT 4\n')
run_exp.font.name = 'Calibri'
run_exp.font.size = Pt(14)
run_exp.font.bold = True
run_exp.font.color.rgb = RGBColor(31, 73, 125)

run_title = title_p.add_run('Multi-Node Kubernetes Cluster Orchestration, Workload Scheduling, Scaling, and Automated Self-Healing on Windows')
run_title.font.name = 'Calibri'
run_title.font.size = Pt(17)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(15, 34, 64)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_p.paragraph_format.space_after = Pt(14)
r_sub = sub_p.add_run('Laboratory Study on KinD, Multi-Worker Pod Placement, and ReplicaSet Fault Recovery')
r_sub.font.name = 'Calibri'
r_sub.font.size = Pt(11)
r_sub.font.italic = True
r_sub.font.color.rgb = RGBColor(89, 89, 89)

# Metadata Table
meta_tbl = doc.add_table(rows=5, cols=2)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ('Student Name', 'Chhavi Mishra'),
    ('USN', '01fe24bci066'),
    ('Roll Number / Division', 'Roll No: 136 | Division: A'),
    ('Department / Program', 'Computer Science and Engineering (Artificial Intelligence)'),
    ('Course & Institution', 'Cloud Computing Laboratory (CS401) | KLE Technological University, Hubballi')
]
for idx, (k, v) in enumerate(meta_data):
    meta_tbl.rows[idx].cells[0].paragraphs[0].add_run(k).bold = True
    meta_tbl.rows[idx].cells[1].paragraphs[0].add_run(v)
style_table(meta_tbl, [Inches(2.2), Inches(4.6)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 1: Aim & Objectives
h1 = doc.add_heading('1. Aim & Objectives', level=1)
h1.style.font.color.rgb = RGBColor(31, 73, 125)
p = doc.add_paragraph()
p.add_run('Aim: ').bold = True
p.add_run('To build and orchestrate a multi-node Kubernetes cluster on a Windows machine using KinD (Kubernetes IN Docker) over WSL 2, deploy a containerized NGINX web application, evaluate pod scheduling across worker nodes, scale the deployment horizontally, and validate automated self-healing fault tolerance upon pod failure.')

p_obj = doc.add_paragraph()
p_obj.add_run('Key Learning Outcomes:\n').bold = True
bullets = [
    'Configure and verify WSL 2 and Docker Desktop to host containerized Kubernetes nodes.',
    'Author a declarative YAML configuration (kind-config.yaml) to instantiate a 3-node cluster (1 control-plane, 2 workers).',
    'Verify Kubernetes control plane components, node readiness, and examine backing Docker container runtimes.',
    'Deploy an NGINX web server deployment and observe how kube-scheduler assigns pods across distinct worker nodes.',
    'Scale the workload from 3 to 6 replicas and observe dynamic load distribution across available compute nodes.',
    'Deliberately delete an active pod to test declarative state reconciliation and automated zero-touch self-healing by the ReplicaSet controller.'
]
for b in bullets:
    bp = doc.add_paragraph(style='List Bullet')
    bp.add_run(b)
    bp.paragraph_format.space_after = Pt(2)

# Section 2: Environment
h2 = doc.add_heading('2. System & Experimental Configuration', level=1)
h2.style.font.color.rgb = RGBColor(31, 73, 125)
cfg_tbl = doc.add_table(rows=9, cols=2)
cfg_data = [
    ('Parameter', 'Configured / Observed Value'),
    ('Host Operating System', 'Windows 11 (64-bit) Enterprise/Pro'),
    ('Execution Shell', 'Windows PowerShell (Administrator)'),
    ('Linux Subsystem', 'WSL 2 (Ubuntu distribution default, Version 2)'),
    ('Container Engine', 'Docker Desktop (WSL 2 Backend Engine)'),
    ('Kubernetes Orchestrator', 'KinD (Kubernetes IN Docker) v0.33.0'),
    ('Kubernetes Client CLI', 'kubectl v1.37.0 (Client)'),
    ('Kubernetes Node Image', 'kindest/node:v1.37.0'),
    ('Application Workload', 'NGINX (Official Web Server Container)')
]
for idx, (k, v) in enumerate(cfg_data):
    cfg_tbl.rows[idx].cells[0].paragraphs[0].add_run(k)
    cfg_tbl.rows[idx].cells[1].paragraphs[0].add_run(v)
style_table(cfg_tbl, [Inches(2.5), Inches(4.3)])

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 3: Cluster Configuration File
h3 = doc.add_heading('3. Multi-Node Cluster Configuration Manifest (kind-config.yaml)', level=1)
h3.style.font.color.rgb = RGBColor(31, 73, 125)
p_yaml = doc.add_paragraph()
p_yaml.add_run('To instruct KinD to instantiate a multi-node cluster with dedicated roles rather than a single-node cluster, the following declarative YAML manifest was authored and saved in C:\\WINDOWS\\system32\\k8s-lab\\kind-config.yaml:')

p_code = doc.add_paragraph()
p_code.paragraph_format.left_indent = Inches(0.4)
p_code.paragraph_format.space_before = Pt(4)
p_code.paragraph_format.space_after = Pt(6)
r_code = p_code.add_run('kind: Cluster\napiVersion: kind.x-k8s.io/v1alpha4\nnodes:\n  - role: control-plane\n  - role: worker\n  - role: worker')
r_code.font.name = 'Courier New'
r_code.font.size = Pt(9.5)

p_expl = doc.add_paragraph()
p_expl.add_run('Architectural Role Breakdown:\n').bold = True
p_expl.add_run('• kind-control-plane: Acts as the cluster brain, hosting kube-apiserver, etcd key-value store, kube-scheduler, and kube-controller-manager.\n• kind-worker & kind-worker2: Serve as the compute execution pool where user pods and application containers are scheduled, managed by kubelet and kube-proxy.')

# Section 4: Experimental Procedure and Evidence
h4 = doc.add_heading('4. Step-by-Step Procedure, Evidence & Terminal Outputs', level=1)
h4.style.font.color.rgb = RGBColor(31, 73, 125)

img_dir = r'D:\5th sem\CC\cloud_computing-\images'

# 4.1 WSL & Docker
h41 = doc.add_heading('4.1 Step 1: WSL 2 and Docker Engine Verification', level=2)
p_s1 = doc.add_paragraph('Before initializing Kubernetes, the underlying WSL 2 virtualization layer was verified using wsl --status and wsl -l -v. As shown below, Ubuntu and docker-desktop are installed with Version 2, confirming that Docker Desktop is functioning with full hardware-assisted virtualization.')
doc.add_picture(os.path.join(img_dir, 'k8s_wsl_status.png'), width=Inches(5.8))
cap1 = doc.add_paragraph('Figure 1: PowerShell output showing WSL 2 status and running docker-desktop backend.')
cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap1.runs[0].font.size = Pt(9)
cap1.runs[0].font.italic = True

# 4.2 Cluster Nodes & Containers
h42 = doc.add_heading('4.2 Step 2: Cluster Creation, Node Verification & Docker Container Mapping', level=2)
p_s2 = doc.add_paragraph('The cluster was created using kind create cluster --config kind-config.yaml. Running kubectl get nodes verified all three nodes in Ready status. In addition, docker ps revealed that each Kubernetes node operates inside an independent Docker container directly visible from Windows.')
doc.add_picture(os.path.join(img_dir, 'k8s_nodes_docker_ps.png'), width=Inches(5.8))
cap2 = doc.add_paragraph('Figure 2: kubectl get nodes showing 3 Ready nodes and docker ps showing the backing containers.')
cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap2.runs[0].font.size = Pt(9)
cap2.runs[0].font.italic = True

# Table of Nodes
node_tbl = doc.add_table(rows=4, cols=5)
node_data = [
    ('Node Name', 'Kubernetes Role', 'Status', 'Version', 'Docker Container ID'),
    ('kind-control-plane', 'control-plane', 'Ready', 'v1.37.0', '6b16706fc603'),
    ('kind-worker', '<none> (worker)', 'Ready', 'v1.37.0', '317ce8f4adcf'),
    ('kind-worker2', '<none> (worker)', 'Ready', 'v1.37.0', 'fe5c2984d1b3')
]
for idx, row in enumerate(node_data):
    for c_idx, val in enumerate(row):
        node_tbl.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(node_tbl, [Inches(1.8), Inches(1.3), Inches(0.9), Inches(1.0), Inches(1.8)])

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# 4.3 Deployment of NGINX
h43 = doc.add_heading('4.3 Step 3: NGINX Web Application Deployment (3 Replicas)', level=2)
p_s3 = doc.add_paragraph('An NGINX web application deployment was initiated with 3 replicas using kubectl create deployment web --image=nginx --replicas=3. Executing kubectl get pods -o wide demonstrated that the Kubernetes scheduler assigned the three pods across both worker nodes to ensure high availability.')
doc.add_picture(os.path.join(img_dir, 'k8s_pods_3replicas.png'), width=Inches(5.8))
cap3 = doc.add_paragraph('Figure 3: kubectl get pods -o wide displaying 3 NGINX replicas distributed across kind-worker and kind-worker2.')
cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap3.runs[0].font.size = Pt(9)
cap3.runs[0].font.italic = True

# Table of 3 pods
p3_tbl = doc.add_table(rows=4, cols=5)
p3_data = [
    ('Pod Name', 'Status', 'Restarts', 'Assigned IP', 'Scheduled Worker Node'),
    ('web-5fc9f4bf66-lrvv7', 'Running', '0', '10.244.2.3', 'kind-worker'),
    ('web-5fc9f4bf66-w9rd5', 'Running', '0', '10.244.2.2', 'kind-worker'),
    ('web-5fc9f4bf66-rrnwx', 'Running', '0', '10.244.1.2', 'kind-worker2')
]
for idx, row in enumerate(p3_data):
    for c_idx, val in enumerate(row):
        p3_tbl.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(p3_tbl, [Inches(2.0), Inches(0.9), Inches(0.8), Inches(1.2), Inches(1.9)])

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# 4.4 Horizontal Scaling
h44 = doc.add_heading('4.4 Step 4: Horizontal Scaling to 6 Replicas & Load Balancing', level=2)
p_s4 = doc.add_paragraph('The application was scaled horizontally to 6 replicas using kubectl scale deployment web --replicas=6. The scheduler dynamically placed the 3 newly spawned pods such that each worker node hosted exactly 3 pods, achieving a perfect 50% / 50% compute balance.')
doc.add_picture(os.path.join(img_dir, 'k8s_pods_6replicas.png'), width=Inches(5.8))
cap4 = doc.add_paragraph('Figure 4: kubectl get pods -o wide showing 6 pods evenly balanced between kind-worker (3 pods) and kind-worker2 (3 pods).')
cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap4.runs[0].font.size = Pt(9)
cap4.runs[0].font.italic = True

# Table of 6 pods
p6_tbl = doc.add_table(rows=7, cols=5)
p6_data = [
    ('Pod Name', 'Status', 'Age', 'Assigned IP', 'Scheduled Worker Node'),
    ('web-5fc9f4bf66-hpncv', 'Running', '50s', '10.244.2.4', 'kind-worker'),
    ('web-5fc9f4bf66-lrvv7', 'Running', '12m', '10.244.2.3', 'kind-worker'),
    ('web-5fc9f4bf66-w9rd5', 'Running', '12m', '10.244.2.2', 'kind-worker'),
    ('web-5fc9f4bf66-9jr2v', 'Running', '50s', '10.244.1.3', 'kind-worker2'),
    ('web-5fc9f4bf66-j5dv4', 'Running', '50s', '10.244.1.4', 'kind-worker2'),
    ('web-5fc9f4bf66-rrnwx', 'Running', '12m', '10.244.1.2', 'kind-worker2')
]
for idx, row in enumerate(p6_data):
    for c_idx, val in enumerate(row):
        p6_tbl.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(p6_tbl, [Inches(2.0), Inches(0.9), Inches(0.8), Inches(1.2), Inches(1.9)])

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# 4.5 Self Healing Trigger
h45 = doc.add_heading('4.5 Step 5: Fault Injection & Automated Self-Healing Trigger', level=2)
p_s5 = doc.add_paragraph('To validate self-healing capabilities, pod web-5fc9f4bf66-lrvv7 was deleted using kubectl delete pod web-5fc9f4bf66-lrvv7. The Kubernetes ReplicaSet controller detected that active replicas (5) differed from desired replicas (6) and automatically launched replacement pod web-5fc9f4bf66-49nq9 within 5 seconds.')
doc.add_picture(os.path.join(img_dir, 'k8s_pod_delete_self_healing.png'), width=Inches(5.8))
cap5 = doc.add_paragraph('Figure 5: Deletion of pod lrvv7 and rapid automated recreation of replacement pod 49nq9 within 5 seconds.')
cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap5.runs[0].font.size = Pt(9)
cap5.runs[0].font.italic = True

# 4.6 Steady-state Recovery
h46 = doc.add_heading('4.6 Step 6: Steady-State Recovery & Healed Cluster State', level=2)
p_s6 = doc.add_paragraph('Following the transient image pull and container startup, kubectl get pods verified that replacement pod web-5fc9f4bf66-49nq9 reached 1/1 Running status (observed at age 23m), restoring all 6 pods to healthy operation without any manual administrative action.')
doc.add_picture(os.path.join(img_dir, 'k8s_self_healing_healed.png'), width=Inches(5.8))
cap6 = doc.add_paragraph('Figure 6: Final kubectl get pods output confirming steady-state 6/6 Running pods including the healed pod 49nq9.')
cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap6.runs[0].font.size = Pt(9)
cap6.runs[0].font.italic = True

# Section 5: Technical Analysis
h5 = doc.add_heading('5. In-Depth Technical Analysis', level=1)
h5.style.font.color.rgb = RGBColor(31, 73, 125)

p_t1 = doc.add_paragraph()
p_t1.add_run('1. Declarative Control Loop (Reconciliation):\n').bold = True
p_t1.add_run('Unlike imperative VM systems where administrators must manually restart crashed services, Kubernetes operates on a declarative reconciliation loop. The Deployment manages a ReplicaSet that continuously calculates:\n   Discrepancy = Desired Replicas (6) - Active Healthy Replicas (5) = +1\nThe instant a discrepancy is identified, the controller issues API calls to schedule and launch an identical pod.')

p_t2 = doc.add_paragraph()
p_t2.add_run('2. Workload Placement & Scheduling Algorithms:\n').bold = True
p_t2.add_run('The kube-scheduler uses a two-phase process: Filtering (ensuring nodes satisfy port, compute, and taint conditions) and Scoring (ranking candidates based on resource balance and spreading rules). In this experiment, the scoring algorithm distributed 6 pods equally (3 on kind-worker, 3 on kind-worker2), effectively guarding against single-node blast radius.')

p_t3 = doc.add_paragraph()
p_t3.add_run('3. Software-Defined Networking (SDN) and IP Allocation:\n').bold = True
p_t3.add_run('The KinD CNI allocates non-overlapping /24 subnets to each worker container:\n• kind-worker: 10.244.2.0/24 (Pods received 10.244.2.2, 10.244.2.3, 10.244.2.4)\n• kind-worker2: 10.244.1.0/24 (Pods received 10.244.1.2, 10.244.1.3, 10.244.1.4)\nThis design guarantees unique IP addresses per pod, enabling transparent pod-to-pod east-west communication without port collisions.')

# Section 6: Commands Used
h6 = doc.add_heading('6. Summary of Important Commands Used', level=1)
h6.style.font.color.rgb = RGBColor(31, 73, 125)
cmd_tbl = doc.add_table(rows=9, cols=2)
cmd_data = [
    ('Command', 'Functional Purpose'),
    ('wsl --status / wsl -l -v', 'Verify WSL 2 virtualization status and registered distributions.'),
    ('kind create cluster --config kind-config.yaml', 'Instantiate 3-node Kubernetes cluster from declarative manifest.'),
    ('kubectl get nodes', 'Display cluster node inventory, roles, status, and version.'),
    ('docker ps', 'Inspect underlying Docker containers executing each Kubernetes node.'),
    ('kubectl create deployment web --image=nginx --replicas=3', 'Deploy 3 initial NGINX web server pods.'),
    ('kubectl get pods -o wide', 'Inspect pod IPs, readiness, restart counts, and node placement.'),
    ('kubectl scale deployment web --replicas=6', 'Horizontally scale deployment from 3 to 6 replicas.'),
    ('kubectl delete pod <pod-name>', 'Deliberately delete pod to trigger automated self-healing.')
]
for idx, (k, v) in enumerate(cmd_data):
    cmd_tbl.rows[idx].cells[0].paragraphs[0].add_run(k)
    cmd_tbl.rows[idx].cells[1].paragraphs[0].add_run(v)
style_table(cmd_tbl, [Inches(3.2), Inches(3.6)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 7: Result & Conclusion
h7 = doc.add_heading('7. Result & Conclusion', level=1)
h7.style.font.color.rgb = RGBColor(31, 73, 125)

p_res = doc.add_paragraph()
p_res.add_run('Result: ').bold = True
p_res.add_run('A 3-node Kubernetes cluster (1 control-plane, 2 workers) was successfully built on Windows using KinD and Docker Desktop over WSL 2. The NGINX application was deployed with 3 replicas, successfully scaled horizontally to 6 replicas with balanced multi-worker distribution (3 pods per node), and verified for self-healing resilience when pod web-5fc9f4bf66-lrvv7 was deleted and automatically replaced by web-5fc9f4bf66-49nq9 within 5 seconds.')

p_con = doc.add_paragraph()
p_con.add_run('Conclusion: ').bold = True
p_con.add_run('This experiment conclusively demonstrates the power of container orchestration over traditional manual virtualization. Kubernetes abstracts underlying hardware infrastructure into a unified compute pool, automates pod placement through intelligent scheduling, achieves high elasticity through dynamic horizontal scaling, and guarantees high service availability via continuous declarative self-healing.')

# Save to both locations
doc_path_cc = r'D:\5th sem\CC\Experiment_4_Kubernetes_Cluster_Scheduling_and_Self_Healing_Report.docx'
doc_path_repo = r'D:\5th sem\CC\cloud_computing-\kubernetes-cluster\Experiment_4_Kubernetes_Cluster_Scheduling_and_Self_Healing_Report.docx'

doc.save(doc_path_cc)
print('Saved to:', doc_path_cc)
doc.save(doc_path_repo)
print('Saved to:', doc_path_repo)
