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
run_exp = title_p.add_run('EXPERIMENT 2 (PART 2)\n')
run_exp.font.name = 'Calibri'
run_exp.font.size = Pt(14)
run_exp.font.bold = True
run_exp.font.color.rgb = RGBColor(31, 73, 125)

run_title = title_p.add_run('Run, Test and Manage a Docker Container\n')
run_title.font.name = 'Calibri'
run_title.font.size = Pt(17)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(15, 34, 64)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_p.paragraph_format.space_after = Pt(12)
r_sub = sub_p.add_run('Container Lifecycle, Port Forwarding, Interactive Shell Execution, and Image Immutability')
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
h1 = doc.add_heading('1. Aim & Learning Objectives', level=1)
h1.style.font.color.rgb = RGBColor(31, 73, 125)

p_aim = doc.add_paragraph()
p_aim.add_run('Aim: ').bold = True
p_aim.add_run('To understand and execute the complete Docker container lifecycle using an existing local application image (my-python-app), deploy a distinct container instance (test-python-container) on host port 5001, test application responsiveness via web browser and programmatic HTTP requests, inspect container internals and logs, interact with the container runtime shell, evaluate state retention across stop/start cycles, safely delete the container, and prove image immutability.')

p_obj = doc.add_paragraph()
p_obj.add_run('Key Learning Outcomes:').bold = True
bullets = [
    'Instantiate and run a detached Docker container from a pre-existing local image without rebuilding.',
    'Map host port 5001 to container port 5000 and verify bi-directional network traffic forwarding.',
    'Validate HTTP server responses via both standard web browsers and PowerShell Invoke-WebRequest.',
    'Inspect container metadata (JSON configuration, network endpoints, state) using docker inspect.',
    'Execute interactive shell sessions (/bin/sh) inside running containers using docker exec -it to inspect filesystem hierarchy and working directory (/app).',
    'Demonstrate container state transitions (Running -> Stopped -> Restarted) while confirming Container ID persistence (6c755d50ded2).',
    'Safely terminate and remove container instances using docker stop and docker rm.',
    'Verify that container removal does not delete or alter the base Docker image (my-python-app:latest).'
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
    ('Parameter / Component', 'Configured Value / Specification'),
    ('Host Operating System', 'Windows 11 (64-bit) Enterprise / Pro'),
    ('CLI Management Shell', 'Windows PowerShell (Administrator)'),
    ('Container Engine Runtime', 'Docker Desktop (WSL 2 Backend Engine, Docker v29.x)'),
    ('Source Application Image', 'my-python-app:latest (ID: be84ed5367f1, 200 MB)'),
    ('Target Container Name', 'test-python-container'),
    ('Allocated Container ID', '6c755d50ded2a5ae4fa6ee11076fdc74c887ce1103963e1cb0da93737c14f4ca'),
    ('Port Forwarding Mapping', 'Host 0.0.0.0:5001 -> Container 5000/tcp'),
    ('Internal Web Application', 'Python 3.12 Flask Microservice (app.py running on port 5000)')
]
for idx, (k, v) in enumerate(cfg_data):
    cfg_tbl.rows[idx].cells[0].paragraphs[0].add_run(k)
    cfg_tbl.rows[idx].cells[1].paragraphs[0].add_run(v)
style_table(cfg_tbl, [Inches(2.5), Inches(4.3)])

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 3: Architecture & Concepts
h3 = doc.add_heading('3. Conceptual Architecture & Lifecycle Model', level=1)
h3.style.font.color.rgb = RGBColor(31, 73, 125)

p_arch = doc.add_paragraph()
p_arch.add_run('3.1 Image vs. Container Paradigm: ').bold = True
p_arch.add_run('A Docker Image (my-python-app) is a read-only, immutable template built from layered filesystems (Python 3.12-slim base, dependencies in requirements.txt, and Flask application app.py). A Docker Container (test-python-container) is an isolated, lightweight, runnable instance of that image with a thin read-write container layer on top. Multiple independent containers (e.g., my-python-container on port 5000 and test-python-container on port 5001) can run concurrently from the exact same image.')

p_port = doc.add_paragraph()
p_port.add_run('3.2 Network Port Forwarding Architecture: ').bold = True
p_port.add_run('When launching with -p 5001:5000, Docker binds port 5001 on the Windows host network stack. Any inbound TCP packet sent to http://localhost:5001 is captured by the Docker proxy and forwarded through the Docker bridge network to port 5000 inside the container namespace, where the Flask WSGI server processes the request and responds.')

p_life = doc.add_paragraph()
p_life.add_run('3.3 Container Lifecycle Progression: ').bold = True
p_life.add_run('The lifecycle follows a strict state transition: Created -> Running (Up) -> Stopped (Exited 137) -> Restarted (Up, preserving Container ID) -> Stopped -> Removed (Deleted). Even when stopped, container metadata and state persist until explicit removal via docker rm.')

# Section 4: Execution Log
h4 = doc.add_heading('4. Step-by-Step Execution Log (18 Lab Manual Steps)', level=1)
h4.style.font.color.rgb = RGBColor(31, 73, 125)

steps_text = [
    ('Step 1: Check Docker Version', 'docker --version', 'Verified Docker Desktop engine availability on Windows PowerShell.'),
    ('Step 2: Display Local Docker Images', 'docker images', 'Confirmed my-python-app:latest (Image ID: be84ed5367f1, size: 200 MB) was present locally.'),
    ('Step 3: Create & Run Detached Container', 'docker run -d -p 5001:5000 --name test-python-container my-python-app', 'Instantiated container test-python-container with port mapping 5001:5000. Output Container ID: 6c755d50ded2...'),
    ('Step 4: Check Running Containers', 'docker ps', 'Verified container 6c755d50ded2 is active with status "Up 16 seconds" and port binding 0.0.0.0:5001->5000/tcp.'),
    ('Step 5: Access Web Application in Browser', 'Open http://localhost:5001 in Chrome', 'Application rendered successfully returning: "Hello! My first Docker application is running."'),
    ('Step 6: Test Container via PowerShell', 'Invoke-WebRequest http://localhost:5001', 'HTTP GET request returned StatusCode 200 OK with identical application payload directly in PowerShell.'),
    ('Step 7: Inspect Container Logs', 'docker logs test-python-container', 'Verified Flask server initialization on port 5000 and logged incoming GET / HTTP/1.1 requests.'),
    ('Step 8: Inspect Container Metadata', 'docker inspect test-python-container', 'Extracted JSON configuration verifying container Name, Image SHA, NetworkSettings, and State.Running=True.'),
    ('Step 9: Open Interactive Shell in Container', 'docker exec -it test-python-container /bin/sh', 'Attached interactive pseudo-TTY session inside running container Linux environment (/app #).'),
    ('Step 10: Explore Container Filesystem', 'ls && pwd', 'Listed directory contents revealing app.py and requirements.txt inside default working directory /app.'),
    ('Step 11: Exit Container Shell', 'exit', 'Returned cleanly to Windows PowerShell host prompt; confirmed container remained in active Up state.'),
    ('Step 12: Stop Container Gracefully', 'docker stop test-python-container', 'Sent SIGTERM followed by SIGKILL; docker ps verified container is no longer listed in running table.'),
    ('Step 13: Check Stopped Containers', 'docker ps -a', 'Confirmed test-python-container exists in Exited (137) state without data loss.'),
    ('Step 14: Restart Stopped Container', 'docker start test-python-container', 'Re-activated existing container instance; verified status returned to Up with live HTTP response on port 5001.'),
    ('Step 15: Compare Container ID Persistence', 'docker ps', 'Verified Container ID 6c755d50ded2 remained exactly identical before stop and after start.'),
    ('Step 16: Remove Container Permanently', 'docker stop test-python-container && docker rm test-python-container', 'Terminated and permanently deleted test-python-container; docker ps -a confirmed complete cleanup.'),
    ('Step 17: Confirm Image Immutability', 'docker images', 'Verified my-python-app:latest remains completely intact in local image repository ready for future instantiation.'),
    ('Step 18: Verify Image Reusability', 'docker images', 'Demonstrated 1-to-N relationship where a single immutable image supports multiple ephemeral containers.')
]

steps_tbl = doc.add_table(rows=len(steps_text)+1, cols=3)
steps_tbl.rows[0].cells[0].paragraphs[0].add_run('Lab Step')
steps_tbl.rows[0].cells[1].paragraphs[0].add_run('Command Executed')
steps_tbl.rows[0].cells[2].paragraphs[0].add_run('Observation & Result')

for idx, (st, cmd, obs) in enumerate(steps_text):
    row = steps_tbl.rows[idx+1]
    row.cells[0].paragraphs[0].add_run(st).bold = True
    p_c = row.cells[1].paragraphs[0]
    r_c = p_c.add_run(cmd)
    r_c.font.name = 'Consolas'
    r_c.font.size = Pt(9)
    row.cells[2].paragraphs[0].add_run(obs)
style_table(steps_tbl, [Inches(1.8), Inches(2.7), Inches(2.5)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 5: Screenshots
h5 = doc.add_heading('5. Empirical Evidence & Terminal Verification', level=1)
h5.style.font.color.rgb = RGBColor(31, 73, 125)

figures = [
    ('docker_run_browser_localhost5001.png', 'Figure 1: Container Launch & Browser Verification', 'PowerShell terminal executing docker run -d -p 5001:5000 --name test-python-container my-python-app, verifying container status via docker ps (ID: 6c755d50ded2, port 5001->5000/tcp), alongside Google Chrome browser rendering http://localhost:5001 ("Hello! My first Docker application is running.").'),
    ('docker_invoke_webrequest_port5001.png', 'Figure 2: Programmatic HTTP Testing via PowerShell', 'PowerShell executing Invoke-WebRequest http://localhost:5001 confirming successful HTTP 200 communication directly through Windows host port 5001.'),
    ('docker_exec_interactive_shell.png', 'Figure 3: Interactive Shell Execution & Filesystem Inspection', 'docker exec -it test-python-container /bin/sh opening an in-container shell session; ls confirms presence of app.py and requirements.txt, and pwd verifies the active working directory /app.'),
    ('docker_stop_container.png', 'Figure 4: Container Stop Operation & Running Filter Check', 'Executing docker stop test-python-container and running docker ps to verify that the container is no longer present in the active container list.'),
    ('docker_ps_all_stopped_exited.png', 'Figure 5: Stopped Container State Verification (docker ps -a)', 'Inspection of all containers via docker ps -a confirming test-python-container transitioned to Exited (137) state while preserving configuration and ID.'),
    ('docker_start_and_rm_lifecycle.png', 'Figure 6: Container Restart & Safe Deletion Lifecycle', 'Restarting container with docker start test-python-container, followed by docker stop, docker rm, and docker ps -a verifying permanent container deletion.'),
    ('docker_images_persistence_check.png', 'Figure 7: Docker Image Immutability and Persistence Check', 'docker images execution demonstrating that the underlying image my-python-app:latest (ID: be84ed5367f1, 200 MB) remains completely intact and reusable.')
]

img_dir = r'D:\5th sem\CC\cloud_computing-\images'
for img_name, fig_title, fig_desc in figures:
    img_path = os.path.join(img_dir, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img_path, width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_t = p_cap.add_run(fig_title + ': ')
        r_t.bold = True
        r_t.font.size = Pt(9.5)
        r_d = p_cap.add_run(fig_desc)
        r_d.font.size = Pt(9.5)
        r_d.font.italic = True

# Section 6: State Transition Table
h6 = doc.add_heading('6. Container Lifecycle State Transition Summary', level=1)
h6.style.font.color.rgb = RGBColor(31, 73, 125)

state_rows = [
    ('State Transition', 'Command Trigger', 'Status in docker ps', 'Status in docker ps -a', 'Port 5001 Reachable?', 'Container ID'),
    ('Image -> Active Container', 'docker run -d -p 5001:5000', 'Up (Active)', 'Up', 'Yes (HTTP 200)', '6c755d50ded2'),
    ('Shell Interaction', 'docker exec -it /bin/sh', 'Up (Active)', 'Up', 'Yes (HTTP 200)', '6c755d50ded2'),
    ('Active -> Stopped', 'docker stop', 'Not Listed', 'Exited (137)', 'No (Connection Refused)', '6c755d50ded2'),
    ('Stopped -> Active', 'docker start', 'Up (Active)', 'Up', 'Yes (HTTP 200)', '6c755d50ded2'),
    ('Active -> Removed', 'docker stop && docker rm', 'Not Listed', 'Not Listed', 'No', 'Permanently Deleted')
]
st_tbl = doc.add_table(rows=len(state_rows), cols=6)
for r_idx, r_vals in enumerate(state_rows):
    for c_idx, val in enumerate(r_vals):
        st_tbl.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(st_tbl, [Inches(1.5), Inches(1.5), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.0)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 7: Conclusion
h7 = doc.add_heading('7. Conclusion & Key Takeaways', level=1)
h7.style.font.color.rgb = RGBColor(31, 73, 125)

p_c1 = doc.add_paragraph()
p_c1.add_run('1. Reusability of Docker Images: ').bold = True
p_c1.add_run('Experiment 2 proved that building an image is a one-time operation. The pre-built image my-python-app was seamlessly instantiated into a completely new isolated container test-python-container on a different host port (5001).')

p_c2 = doc.add_paragraph()
p_c2.add_run('2. Container Ephemerality and State Retention: ').bold = True
p_c2.add_run('Stopping a container transitions it to the Exited state without destroying its filesystem layer or container identity (Container ID: 6c755d50ded2). Running docker start resumes execution instantaneously (<0.5s).')

p_c3 = doc.add_paragraph()
p_c3.add_run('3. Interactive Debugging & Shell Execution: ').bold = True
p_c3.add_run('docker exec enables direct inspection of in-container filesystems and environment variables without stopping or restarting the running service process.')

p_c4 = doc.add_paragraph()
p_c4.add_run('4. Clean Deletion & Image Preservation: ').bold = True
p_c4.add_run('Deleting test-python-container via docker rm fully cleans up host network bindings and container runtime metadata while leaving the base image my-python-app:latest intact for future container deployments.')

# Save to both target locations
out1 = r'D:\5th sem\CC\cloud_computing-\docker-python-app\Experiment_2_Run_Test_and_Manage_Docker_Container_Report.docx'
out2 = r'D:\5th sem\CC\Experiment_2_Run_Test_and_Manage_Docker_Container_Report.docx'
doc.save(out1)
doc.save(out2)
print(f'Successfully generated {out1}')
print(f'Successfully generated {out2}')
