import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

doc = docx.Document()

# Margins
for s in doc.sections:
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
                set_cell_background(cell, '5C4EE5') # Terraform Purple Accent
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, 'F7F6FD')
                else:
                    set_cell_background(cell, 'FFFFFF')

# Title
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(2)
run_exp = title_p.add_run('EXPERIMENT 5 — PART 2\n')
run_exp.font.name = 'Calibri'
run_exp.font.size = Pt(14)
run_exp.font.bold = True
run_exp.font.color.rgb = RGBColor(92, 78, 229)

run_title = title_p.add_run('Deploy Multiple Docker Containers Using HashiCorp Terraform\n')
run_title.font.name = 'Calibri'
run_title.font.size = Pt(17)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(26, 20, 64)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_p.paragraph_format.space_after = Pt(12)
r_sub = sub_p.add_run('Declarative Multi-Service Orchestration, Docker Provider Integration, Resource Dependencies, and Web Verification')
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

# Section 1: Aim & Learning Objectives
h1 = doc.add_heading('1. Aim & Learning Objectives', level=1)
h1.style.font.color.rgb = RGBColor(92, 78, 229)

p_aim = doc.add_paragraph()
p_aim.add_run('Aim: ').bold = True
p_aim.add_run('To provision, deploy, manage, and verify multiple heterogeneous Docker containers using HashiCorp Terraform by defining infrastructure resources through declarative Infrastructure as Code (IaC), leveraging the kreuzwerker/docker provider plugin on Windows PowerShell.')

p_obj = doc.add_paragraph()
p_obj.add_run('Key Learning Objectives:').bold = True
bullets = [
    'Configure HashiCorp Terraform to interface directly with Docker Desktop Engine via the kreuzwerker/docker provider plugin (~> 3.0).',
    'Declare multi-tier container resources comprising an NGINX Alpine Web Server and a Python 3.12 HTTP Server within a single unified manifest (main.tf).',
    'Demonstrate implicit dependency graph resolution where Terraform ensures Docker images are fetched prior to container instantiation via image_id interpolation.',
    'Configure host-to-container port mapping bridging container ports 80 and 8000 to distinct host ports (8082 and 8081).',
    'Execute the complete IaC lifecycle: terraform init, validate, plan, and apply.',
    'Verify live multi-container execution through the Docker CLI (docker ps) and HTTP browser endpoints (localhost:8082 and localhost:8081).'
]
for b in bullets:
    bp = doc.add_paragraph(style='List Bullet')
    bp.add_run(b)

# Section 2: Architectural Overview & System Specifications
h2 = doc.add_heading('2. Architectural Overview & System Specifications', level=1)
h2.style.font.color.rgb = RGBColor(92, 78, 229)

p_arch = doc.add_paragraph()
p_arch.add_run('The experiment deploys two independent Docker containers managed by Terraform through the Docker daemon API over the local Windows named pipe (npipe:////./pipe/docker_engine). The NGINX web server serves static web traffic on host port 8082, while the Python container serves a directory listing on host port 8081.')

spec_data = [
    ('System Component', 'Configuration / Tool Version', 'Operational Role'),
    ('Operating System', 'Microsoft Windows 11 Enterprise (64-bit)', 'Host Workstation Environment'),
    ('IaC Orchestrator', 'HashiCorp Terraform v1.17.2', 'Declarative Infrastructure Lifecycle Management'),
    ('Terraform Provider', 'kreuzwerker/docker v3.9.0', 'Docker Engine API Driver Plugin'),
    ('Container Runtime', 'Docker Desktop / Docker CE (WSL 2 Engine)', 'Container Virtualization & Process Isolation'),
    ('Service 1 (Web Server)', 'nginx:alpine (Host 8082 -> Container 80)', 'Static HTTP Web Server'),
    ('Service 2 (File Server)', 'python:3.12-slim (Host 8081 -> Container 8000)', 'Asynchronous Python HTTP File Server'),
    ('State Database', 'terraform.tfstate (Serial 7, Lineage 013ad275...)', 'Centralized State Synchronization')
]
spec_tbl = doc.add_table(rows=len(spec_data), cols=3)
for r_idx, r_vals in enumerate(spec_data):
    for c_idx, val in enumerate(r_vals):
        spec_tbl.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(spec_tbl, [Inches(2.0), Inches(2.6), Inches(2.2)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 3: Declarative HCL Manifest
h3 = doc.add_heading('3. Declarative HCL Configuration Manifest (main.tf)', level=1)
h3.style.font.color.rgb = RGBColor(92, 78, 229)

p_hcl = doc.add_paragraph()
p_hcl.add_run('The infrastructure is fully described in the declarative manifest below:')

code_text = (
    'terraform {\n'
    '  required_providers {\n'
    '    docker = {\n'
    '      source  = "kreuzwerker/docker"\n'
    '      version = "~> 3.0"\n'
    '    }\n'
    '  }\n'
    '}\n\n'
    'provider "docker" {}\n\n'
    '# Nginx Docker image resource\n'
    'resource "docker_image" "nginx" {\n'
    '  name = "nginx:alpine"\n'
    '}\n\n'
    '# Python Docker image resource\n'
    'resource "docker_image" "python" {\n'
    '  name = "python:3.12-slim"\n'
    '}\n\n'
    '# Nginx web server container resource\n'
    'resource "docker_container" "webserver" {\n'
    '  name  = "terraform-nginx"\n'
    '  image = docker_image.nginx.image_id\n'
    '  ports {\n'
    '    internal = 80\n'
    '    external = 8082\n'
    '  }\n'
    '}\n\n'
    '# Python HTTP server container resource\n'
    'resource "docker_container" "python_app" {\n'
    '  name  = "terraform-python"\n'
    '  image = docker_image.python.image_id\n'
    '  command = ["python", "-m", "http.server", "8000"]\n'
    '  ports {\n'
    '    internal = 8000\n'
    '    external = 8081\n'
    '  }\n'
    '}'
)
p_code = doc.add_paragraph()
r_c = p_code.add_run(code_text)
r_c.font.name = 'Consolas'
r_c.font.size = Pt(8.5)
p_code.paragraph_format.left_indent = Inches(0.3)

# Section 4: Implementation Steps
h4 = doc.add_heading('4. Step-by-Step Execution Lifecycle Log', level=1)
h4.style.font.color.rgb = RGBColor(92, 78, 229)

steps = [
    ('Step 1: Environment Verification', 'Verified Docker Desktop engine status (docker --version, docker ps) and HashiCorp Terraform binary availability in system PATH (terraform --version).'),
    ('Step 2: Provider Initialization (terraform init)', 'Initialized project workspace in C:\\terraform-multiple-containers. Terraform downloaded kreuzwerker/docker v3.9.0 and generated the dependency lock file .terraform.lock.hcl.'),
    ('Step 3: Manifest Validation (terraform validate)', 'Performed static syntax validation, confirming "Success! The configuration is valid."'),
    ('Step 4: Speculative Execution Planning (terraform plan)', 'Terraform calculated the delta between existing Docker state and main.tf, planning 4 additions: 2 images (nginx:alpine, python:3.12-slim) and 2 containers (terraform-nginx, terraform-python).'),
    ('Step 5: Resource Provisioning (terraform apply)', 'Applied execution plan with confirmation "yes". Terraform communicated with Docker daemon, pulled image layers, spawned containers, bound ports, and achieved Apply complete!'),
    ('Step 6: Docker Daemon Verification (docker ps)', 'Inspected active containers via Docker CLI, confirming terraform-nginx (port 8082->80) and terraform-python (port 8081->8000) running healthy in bridge network mode.'),
    ('Step 7: Browser Endpoint Verification', 'Accessed http://localhost:8082 in browser to verify Nginx "Welcome to nginx!" landing page, and http://localhost:8081 to verify Python root directory listing.')
]
for s_title, s_desc in steps:
    sp = doc.add_paragraph()
    sp.add_run(s_title + ': ').bold = True
    sp.add_run(s_desc)

# Section 5: Empirical Screenshots
h5 = doc.add_heading('5. Empirical Evidence & Terminal Verification', level=1)
h5.style.font.color.rgb = RGBColor(92, 78, 229)

figures = [
    ('terraform_p2_init_validate.png', 'Figure 1: Terraform Provider Initialization & Syntax Validation', 'PowerShell terminal executing terraform init downloading kreuzwerker/docker v3.9.0 and locking dependencies, followed by terraform validate returning "Success! The configuration is valid."'),
    ('terraform_p2_plan_python_command.png', 'Figure 2: Speculative Plan for Python Container', 'Execution plan output for docker_container.python_app specifying runtime command ["python", "-m", "http.server", "8000"] and image association.'),
    ('terraform_p2_plan_python_ports.png', 'Figure 3: Port Mapping Specification for Python App', 'Plan output detailing container port configuration: internal port 8000 mapped to host port 8081 on IP 0.0.0.0.'),
    ('terraform_p2_plan_nginx_container.png', 'Figure 4: Speculative Plan for NGINX Container', 'Plan output for docker_container.webserver with container name "terraform-nginx" and bridge network assignment.'),
    ('terraform_p2_plan_images_summary.png', 'Figure 5: Plan Summary & Image Declarations', 'Plan preview detailing docker_image.nginx and docker_image.python additions, concluding with "Plan: 4 to add, 0 to change, 0 to destroy."'),
    ('terraform_p2_apply_refresh_state.png', 'Figure 6: Terraform State Refresh During Apply', 'Executing terraform apply showing real-time state refresh against the Docker Engine API for existing resources.'),
    ('terraform_p2_apply_complete.png', 'Figure 7: Creation Completion & State Inception', 'Terminal prompt confirmation ("yes"), container instantiation in 3s (ID: 82e487287240...), and "Apply complete! Resources: 1 added, 0 changed, 0 destroyed."'),
    ('terraform_p2_docker_ps.png', 'Figure 8: Docker Daemon Runtime Process Inspection', 'Executing docker ps verifying containers terraform-nginx (port 8082) and terraform-python (port 8081) running concurrently in steady state.'),
    ('terraform_p2_browser_nginx_8082.png', 'Figure 9: Browser Verification — NGINX Web Server', 'Browser accessing http://localhost:8082 displaying the default "Welcome to nginx!" landing page.'),
    ('terraform_p2_browser_python_8081.png', 'Figure 10: Browser Verification — Python HTTP File Server', 'Browser accessing http://localhost:8081 displaying the root container directory listing (.dockerenv, bin, boot, etc.).')
]

img_dir = r'D:\5th sem\CC\cloud_computing-\images'
for img_name, fig_title, fig_desc in figures:
    img_path = os.path.join(img_dir, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_path, width=Inches(6.0))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_t = p_cap.add_run(fig_title + ': ')
        r_t.bold = True
        r_t.font.size = Pt(9.5)
        r_d = p_cap.add_run(fig_desc)
        r_d.font.size = Pt(9.5)
        r_d.font.italic = True

# Section 6: Comparative Analysis Table
h6 = doc.add_heading('6. Comparative Technical Analysis: IaC vs Container Composition', level=1)
h6.style.font.color.rgb = RGBColor(92, 78, 229)

comp_data = [
    ('Feature / Metric', 'HashiCorp Terraform (Docker Provider)', 'Docker Compose', 'Kubernetes (KinD / K8s)'),
    ('Primary Paradigm', 'Infrastructure as Code (IaC)', 'Multi-Container Composition', 'Container Orchestration Platform'),
    ('Target Scope', 'Cross-Cloud & Hybrid Infrastructure', 'Single-Node Host Environment', 'Distributed Multi-Node Cluster'),
    ('State Management', 'Explicit State Database (terraform.tfstate)', 'Implicit Daemon Inspection', 'Distributed Consensus (etcd)'),
    ('Drift Detection', 'Native Speculative Diff (terraform plan)', 'None (Recreates on execution)', 'Continuous Active Reconciliation Loop'),
    ('Dependency Graph', 'Explicit Directed Acyclic Graph (DAG)', 'depends_on Service Sequencing', 'Decoupled Probes & Service Mesh'),
    ('Teardown Model', 'Reverse-DAG Ordered De-provisioning', 'docker compose down', 'Cascading Object Garbage Collection')
]
comp_tbl = doc.add_table(rows=len(comp_data), cols=4)
for r_idx, r_vals in enumerate(comp_data):
    for c_idx, val in enumerate(r_vals):
        comp_tbl.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(comp_tbl, [Inches(1.6), Inches(1.8), Inches(1.7), Inches(1.7)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 7: Review Questions & Answers
h7 = doc.add_heading('7. Review Questions & Technical Answers', level=1)
h7.style.font.color.rgb = RGBColor(92, 78, 229)

qa_list = [
    ('Q1: What is the primary role of the kreuzwerker/docker provider in Terraform?',
     'Answer: It translates Terraform\'s declarative HCL resource models (docker_image, docker_container) into RESTful Docker Engine socket API calls, allowing Terraform to control image pulls, container runtimes, port forwards, and network attachments without manual Docker CLI commands.'),
    ('Q2: How does Terraform enforce resource dependency ordering between images and containers?',
     'Answer: By referencing the image attribute as docker_image.nginx.image_id inside the docker_container block, Terraform detects an implicit dependency edge and constructs a Directed Acyclic Graph (DAG) ensuring images are fetched before container creation begins.'),
    ('Q3: Why was the external port for NGINX mapped to 8082 instead of 8080?',
     'Answer: Host port 8080 is commonly utilized by local development proxies or prior services. Terraform allows immediate, declarative port remapping (external = 8082) without needing to alter internal container network configurations (internal = 80).'),
    ('Q4: What ensures idempotency when running terraform apply repeatedly?',
     'Answer: Terraform compares desired state in main.tf against real-world state refreshed from Docker Engine and recorded in terraform.tfstate. When no delta exists, Terraform outputs "0 added, 0 changed, 0 destroyed", leaving running workloads completely undisturbed.')
]
for q, a in qa_list:
    qp = doc.add_paragraph()
    qp.add_run(q).bold = True
    ap = doc.add_paragraph()
    ap.add_run(a)

# Section 8: Conclusion
h8 = doc.add_heading('8. Conclusion & Strategic Cloud Insights', level=1)
h8.style.font.color.rgb = RGBColor(92, 78, 229)

p_con = doc.add_paragraph()
p_con.add_run('This practical laboratory experiment successfully validates the power of HashiCorp Terraform for multi-container lifecycle automation on Windows PowerShell:\n')
c_bullets = [
    'Automated Multi-Service Provisioning: Successfully orchestrated heterogeneous NGINX and Python services through a unified, version-controlled HCL manifest.',
    'Deterministic Dependency Enforcement: Demonstrated DAG-based ordering guaranteeing that container runtimes depend on verified local image layers.',
    'State-Driven Convergence: Validated state persistence (serial: 7, lineage: 013ad275...), enabling safe, repeatable deployments without configuration drift.',
    'Live Service Operationality: Verified concurrent HTTP access to both workloads at localhost:8082 and localhost:8081 with zero port collisions.'
]
for cb in c_bullets:
    p_cb = doc.add_paragraph(style='List Bullet')
    p_cb.add_run(cb)

# Output destinations
out1 = r'D:\5th sem\CC\cloud_computing-\terraform-iac\Experiment_5_Part_2_Multiple_Docker_Containers_Report.docx'
out2 = r'D:\5th sem\CC\Experiment_5_Part_2_Multiple_Docker_Containers_Report.docx'
doc.save(out1)
doc.save(out2)
print(f'Successfully generated {out1}')
print(f'Successfully generated {out2}')
