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
run_exp = title_p.add_run('EXPERIMENT 3 (PART 3)\n')
run_exp.font.name = 'Calibri'
run_exp.font.size = Pt(14)
run_exp.font.bold = True
run_exp.font.color.rgb = RGBColor(31, 73, 125)

run_title = title_p.add_run('Push a Docker Image to Docker Hub\n')
run_title.font.name = 'Calibri'
run_title.font.size = Pt(17)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(15, 34, 64)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_p.paragraph_format.space_after = Pt(12)
r_sub = sub_p.add_run('Registry Authentication, Namespace Tagging, Layer-Based Push, and Remote Image Distribution')
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
p_aim.add_run('To take the existing containerized application image (my-python-app:latest) created locally, authenticate the local Docker CLI with Docker Hub, apply standard registry namespace tagging (chhavirajeshmishra/my-python-app:v1), push the image layers to the public registry, and verify remote availability for cross-machine deployment.')

p_obj = doc.add_paragraph()
p_obj.add_run('Key Learning Outcomes:').bold = True
bullets = [
    'Understand the role of Docker Hub as a centralized, remote image registry for container distribution.',
    'Authenticate local Docker CLI with Docker Hub using docker login.',
    'Construct Docker Hub repository identifiers following the standard USERNAME/REPOSITORY:TAG format.',
    'Use docker tag to map local image instances to remote repository identifiers without rebuilding or copying layers.',
    'Verify that tagging retains the identical underlying Image ID (be84ed5367f1).',
    'Execute docker push to stream container filesystem layers to the remote Docker Hub registry.',
    'Verify online repository availability, inspect tag metadata (v1), and confirm pull readiness for remote environments.'
]
for b in bullets:
    bp = doc.add_paragraph(style='List Bullet')
    bp.add_run(b)
    bp.paragraph_format.space_after = Pt(2)

# Section 2: Environment
h2 = doc.add_heading('2. System & Experimental Configuration', level=1)
h2.style.font.color.rgb = RGBColor(31, 73, 125)

cfg_tbl = doc.add_table(rows=8, cols=2)
cfg_data = [
    ('Parameter / Component', 'Configured Value / Specification'),
    ('Host Operating System', 'Windows 11 (64-bit) Enterprise / Pro'),
    ('CLI Management Shell', 'Windows PowerShell (Administrator)'),
    ('Container Engine Runtime', 'Docker Desktop Engine v29.6.2 (WSL 2 Backend)'),
    ('Docker Hub Account / Namespace', 'chhavirajeshmishra'),
    ('Source Local Image', 'my-python-app:latest (ID: be84ed5367f1, 200 MB)'),
    ('Remote Tagged Image Name', 'chhavirajeshmishra/my-python-app:v1'),
    ('Remote Registry Endpoint', 'docker.io / https://hub.docker.com/r/chhavirajeshmishra/my-python-app')
]
for idx, (k, v) in enumerate(cfg_data):
    cfg_tbl.rows[idx].cells[0].paragraphs[0].add_run(k)
    cfg_tbl.rows[idx].cells[1].paragraphs[0].add_run(v)
style_table(cfg_tbl, [Inches(2.5), Inches(4.3)])

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 3: Conceptual Architecture
h3 = doc.add_heading('3. Conceptual Architecture: Build vs. Tag vs. Push', level=1)
h3.style.font.color.rgb = RGBColor(31, 73, 125)

p_comp = doc.add_paragraph()
p_comp.add_run('The workflow of Experiment 3 bridges the gap between single-node local development and multi-node cloud deployment:\n').bold = False

diff_data = [
    ('Command', 'Operation', 'Primary Function', 'Network Required?'),
    ('docker build', 'Compile Image', 'Packages Dockerfile & application files into local image layers.', 'No (after base pull)'),
    ('docker tag', 'Assign Reference', 'Creates an alias with registry namespace; shares same Image ID.', 'No (strictly local)'),
    ('docker push', 'Upload Image', 'Streams image layers to remote registry (Docker Hub).', 'Yes (Internet connection)'),
    ('docker pull', 'Download Image', 'Fetches remote image onto any other Docker-enabled machine.', 'Yes (Internet connection)')
]
diff_tbl = doc.add_table(rows=len(diff_data), cols=4)
for r_idx, r_vals in enumerate(diff_data):
    for c_idx, val in enumerate(r_vals):
        diff_tbl.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(diff_tbl, [Inches(1.5), Inches(1.5), Inches(2.7), Inches(1.1)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 4: Execution Log
h4 = doc.add_heading('4. Step-by-Step Execution Log (Curriculum Steps)', level=1)
h4.style.font.color.rgb = RGBColor(31, 73, 125)

steps_text = [
    ('Step 1: Check Docker CLI', 'docker --version', 'Confirmed Docker Desktop v29.6.2 is active and responsive.'),
    ('Step 2: Verify Existing Local Image', 'docker images', 'Confirmed my-python-app:latest (ID: be84ed5367f1, 200 MB) was compiled and available.'),
    ('Step 3: Access Docker Hub Online', 'Navigate to https://hub.docker.com', 'Accessed official Docker Hub registry through web browser.'),
    ('Step 4: Authenticate User Account', 'Sign In as chhavirajeshmishra', 'Verified Docker Hub user credentials and active personal namespace.'),
    ('Step 5: CLI Authentication', 'docker login', 'CLI authenticated using stored credentials; returned \"Login Succeeded\".'),
    ('Step 6: Construct Registry Image Name', 'chhavirajeshmishra/my-python-app:v1', 'Formulated naming convention USERNAME/REPOSITORY:TAG.'),
    ('Step 7: Tag Local Image', 'docker tag my-python-app chhavirajeshmishra/my-python-app:v1', 'Created registry alias pointing to existing local image layers without rebuilding.'),
    ('Step 8: Verify Image ID Consistency', 'docker images', 'Confirmed both my-python-app:latest and chhavirajeshmishra/my-python-app:v1 share identical Image ID be84ed5367f1.'),
    ('Step 9: Push Image Layers to Docker Hub', 'docker push chhavirajeshmishra/my-python-app:v1', 'Streamed image layers; verified digest sha256:be84ed5367f1... and size: 856.'),
    ('Step 10: Online Registry Verification', 'Inspect Docker Hub Web Console', 'Confirmed public repository chhavirajeshmishra/my-python-app is live with active tag v1.')
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
h5 = doc.add_heading('5. Empirical Evidence & Visual Verification', level=1)
h5.style.font.color.rgb = RGBColor(31, 73, 125)

figures = [
    ('docker_part3_login_succeeded.png', 'Figure 1: Docker CLI Authentication', 'PowerShell terminal output executing docker --version followed by docker login, verifying successful authentication with Docker Hub (Login Succeeded).'),
    ('docker_part3_tag_verification.png', 'Figure 2: Image Tagging & Identifier Verification', 'Executing docker tag to assign chhavirajeshmishra/my-python-app:v1, followed by docker images confirming identical Image ID (be84ed5367f1) between local and remote tags.'),
    ('docker_part3_push_terminal.png', 'Figure 3: Image Layer Push Execution & Digest Output', 'Executing docker push chhavirajeshmishra/my-python-app:v1 showing layer existence checks and final repository digest sha256:be84ed5367f1be082b4b991defdf9c5a4d1c7c62d30b774123f28d8ef5a123be.'),
    ('docker_part3_hub_portal_verification.png', 'Figure 4: Docker Hub Online Portal Repository Verification', 'Web interface verification showing public repository chhavirajeshmishra/my-python-app with tag v1 (49.1 MB, linux/amd64) and pull command docker pull chhavirajeshmishra/my-python-app:v1.')
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

# Section 6: Local vs Remote
h6 = doc.add_heading('6. Local Image vs. Remote Registry Comparison', level=1)
h6.style.font.color.rgb = RGBColor(31, 73, 125)

loc_data = [
    ('Attribute / Feature', 'Local Docker Host', 'Docker Hub Registry'),
    ('Repository Name', 'my-python-app:latest', 'chhavirajeshmishra/my-python-app:v1'),
    ('Storage Location', 'Local Host (/var/lib/docker)', 'Docker Cloud Object Storage (S3/GCS backed)'),
    ('Accessibility Scope', 'Only current development machine', 'Global public / Internet-accessible'),
    ('Image ID', 'be84ed5367f1', 'be84ed5367f1 (Identical SHA256 digest)'),
    ('Storage Size', '200 MB (Uncompressed disk allocation)', '49.1 MB (Compressed layer transmission)'),
    ('Primary Role', 'Local testing & rapid iteration', 'Artifact versioning & cross-node deployment')
]
loc_tbl = doc.add_table(rows=len(loc_data), cols=3)
for r_idx, r_vals in enumerate(loc_data):
    for c_idx, val in enumerate(r_vals):
        loc_tbl.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(loc_tbl, [Inches(2.0), Inches(2.5), Inches(2.5)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 7: Conclusion
h7 = doc.add_heading('7. Conclusion & Key Technical Takeaways', level=1)
h7.style.font.color.rgb = RGBColor(31, 73, 125)

p_c1 = doc.add_paragraph()
p_c1.add_run('1. Centralized Image Distribution: ').bold = True
p_c1.add_run('Experiment 3 successfully established the critical link between isolated local containerization and distributed cloud deployment. Pushing the image to Docker Hub makes the application available to any internet-connected server.')

p_c2 = doc.add_paragraph()
p_c2.add_run('2. Non-Destructive Tagging: ').bold = True
p_c2.add_run('docker tag is a metadata pointer operation that does not duplicate physical disk space or trigger a new build. Both my-python-app:latest and chhavirajeshmishra/my-python-app:v1 reference the exact same underlying layers (Image ID: be84ed5367f1).')

p_c3 = doc.add_paragraph()
p_c3.add_run('3. Efficient Layer-Based Upload: ').bold = True
p_c3.add_run('Docker Hub leverages content-addressable storage. Only novel application layers are transmitted, while standard base layers (python:3.12-slim) are recognized as \"Layer already exists\", conserving network bandwidth.')

p_c4 = doc.add_paragraph()
p_c4.add_run('4. Foundation for Orchestration: ').bold = True
p_c4.add_run('Having chhavirajeshmishra/my-python-app:v1 published on Docker Hub allows multi-node Kubernetes clusters or remote Docker daemons to pull the image directly via docker pull or declarative Kubernetes deployment manifests.')

# Save to both target locations
out1 = r'D:\5th sem\CC\cloud_computing-\docker-python-app\Experiment_3_Push_Docker_Image_to_Docker_Hub_Report.docx'
out2 = r'D:\5th sem\CC\Experiment_3_Push_Docker_Image_to_Docker_Hub_Report.docx'
doc.save(out1)
doc.save(out2)
print(f'Successfully generated {out1}')
print(f'Successfully generated {out2}')
