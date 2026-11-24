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
run_exp = title_p.add_run('EXPERIMENT 5\n')
run_exp.font.name = 'Calibri'
run_exp.font.size = Pt(14)
run_exp.font.bold = True
run_exp.font.color.rgb = RGBColor(92, 78, 229)

run_title = title_p.add_run('Infrastructure as Code (IaC) with HashiCorp Terraform on Windows\n')
run_title.font.name = 'Calibri'
run_title.font.size = Pt(17)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(26, 20, 64)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_p.paragraph_format.space_after = Pt(12)
r_sub = sub_p.add_run('Declarative Configuration, Provider Ecosystem, State Management, and Resource Lifecycle')
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
h1.style.font.color.rgb = RGBColor(92, 78, 229)

p_aim = doc.add_paragraph()
p_aim.add_run('Aim: ').bold = True
p_aim.add_run('To understand and apply the principles of Infrastructure as Code (IaC) on Windows PowerShell using HashiCorp Terraform without requiring cloud credentials or Linux/WSL. The experiment demonstrates declaring local resources, provider resolution, syntax validation, execution planning, state-driven resource convergence, drift detection, and automated resource destruction.')

p_obj = doc.add_paragraph()
p_obj.add_run('Key Learning Outcomes:').bold = True
bullets = [
    'Understand declarative Infrastructure as Code (IaC) vs traditional imperative scripting.',
    'Install and configure HashiCorp Terraform on Windows 11 using winget.',
    'Author declarative HashiCorp Configuration Language (HCL) manifests (main.tf) specifying providers and managed resources.',
    'Initialize working directories (terraform init) and resolve external provider plugins (hashicorp/local).',
    'Verify configuration grammar and attribute schema using terraform validate.',
    'Generate speculative execution plans (terraform plan) to preview resource modifications before applying them.',
    'Apply changes (terraform apply) to create managed infrastructure and inspect recorded state (terraform.tfstate).',
    'Perform in-place infrastructure modification, verify convergence, and detect zero-change drift.',
    'Cleanly de-provision and destroy managed infrastructure using terraform destroy.'
]
for b in bullets:
    bp = doc.add_paragraph(style='List Bullet')
    bp.add_run(b)
    bp.paragraph_format.space_after = Pt(2)

# Section 2: Environment
h2 = doc.add_heading('2. System & Experimental Configuration', level=1)
h2.style.font.color.rgb = RGBColor(92, 78, 229)

cfg_tbl = doc.add_table(rows=8, cols=2)
cfg_data = [
    ('Parameter / Component', 'Configured Value / Specification'),
    ('Host Operating System', 'Windows 11 (64-bit) Enterprise / Pro'),
    ('Execution Shell', 'Windows PowerShell (Administrator)'),
    ('IaC Orchestration Tool', 'HashiCorp Terraform v1.17.2 (amd64)'),
    ('Provider Plugin', 'hashicorp/local v2.9.0 (~> 2.9)'),
    ('Managed Resource Type', 'local_file (Resource instance: student_file)'),
    ('Target Output Path', './student.txt (path.module relative)'),
    ('Working Directory', 'C:\\Terraform-Lab')
]
for idx, (k, v) in enumerate(cfg_data):
    cfg_tbl.rows[idx].cells[0].paragraphs[0].add_run(k)
    cfg_tbl.rows[idx].cells[1].paragraphs[0].add_run(v)
style_table(cfg_tbl, [Inches(2.5), Inches(4.3)])

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 3: Configuration Manifest
h3 = doc.add_heading('3. Declarative Configuration Manifest (main.tf)', level=1)
h3.style.font.color.rgb = RGBColor(92, 78, 229)

p_hcl = doc.add_paragraph()
p_hcl.add_run('The following declarative HCL manifest was authored in C:\\Terraform-Lab\\main.tf to instruct Terraform to manage the local resource:')

p_code = doc.add_paragraph()
p_code.paragraph_format.left_indent = Inches(0.4)
p_code.paragraph_format.space_before = Pt(4)
p_code.paragraph_format.space_after = Pt(6)
r_code = p_code.add_run('''terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
  }
}

resource "local_file" "student_file" {
  filename = "${path.module}/student.txt"

  content = <<-EOT
    Welcome to Infrastructure as Code!
    Created using Terraform.
    This file is managed by Terraform.
  EOT
}''')
r_code.font.name = 'Consolas'
r_code.font.size = Pt(9.5)

# Section 4: Execution Log
h4 = doc.add_heading('4. Step-by-Step Execution Log (Curriculum Steps)', level=1)
h4.style.font.color.rgb = RGBColor(92, 78, 229)

steps_text = [
    ('Step 1: Verify Installation', 'terraform --version', 'Confirmed Terraform v1.17.2 installed and accessible on Windows PATH.'),
    ('Step 2: Create Working Folder', 'mkdir C:\\Terraform-Lab && cd C:\\Terraform-Lab', 'Created and navigated to dedicated lab workspace.'),
    ('Step 3: Define Infrastructure', 'notepad main.tf', 'Authored HCL manifest declaring provider hashicorp/local and resource local_file.student_file.'),
    ('Step 4: Initialize Directory', 'terraform init', 'Downloaded provider plugin hashicorp/local v2.9.0 and generated .terraform.lock.hcl.'),
    ('Step 5: Validate Grammar', 'terraform validate', 'Verified syntax correctness returning: \"Success! The configuration is valid.\"'),
    ('Step 6: Preview Execution Plan', 'terraform plan', 'Evaluated declarative state against empty real-world state; generated plan: 1 to add, 0 to change, 0 to destroy.'),
    ('Step 7: Apply Configuration', 'terraform apply -auto-approve=false', 'Created local_file.student_file (ID: 06e6ae35c344...) and generated terraform.tfstate.'),
    ('Step 8: Verify Output File', 'Get-Content .\\student.txt', 'Verified student.txt created on filesystem containing declared multi-line string.'),
    ('Step 9: Modify Configuration', 'Updated content block in main.tf', 'Replaced text with updated 4-line confirmation message; saved main.tf.'),
    ('Step 10: In-Place Modification', 'terraform apply', 'Terraform detected in-place change, updated resource (ID: 926632173084...), and updated state file.'),
    ('Step 11: Drift Detection Check', 'terraform apply (re-run)', 'Terraform compared real infrastructure against configuration and confirmed: \"No changes. Your infrastructure matches the configuration.\"'),
    ('Step 12: Destroy Infrastructure', 'terraform destroy', 'Cleanly de-provisioned resource; Test-Path .\\student.txt returned False confirming complete cleanup.')
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
h5.style.font.color.rgb = RGBColor(92, 78, 229)

figures = [
    ('terraform_validate_and_plan.png', 'Figure 1: Configuration Validation & Execution Planning', 'PowerShell terminal executing terraform validate confirming syntax validity (\"Success! The configuration is valid\"), followed by terraform plan previewing the addition of local_file.student_file (+ create).'),
    ('terraform_apply_creation.png', 'Figure 2: Infrastructure Provisioning & State Inception', 'Executing terraform apply, confirming with \"yes\", creating resource local_file.student_file (ID: 06e6ae35c344...), and achieving \"Apply complete! Resources: 1 added, 0 changed, 0 destroyed.\"'),
    ('terraform_modify_drift_no_changes.png', 'Figure 3: Content Verification & State Convergence (No Drift)', 'Inspecting updated student.txt with Get-Content, followed by terraform apply demonstrating zero-drift state reconciliation: \"No changes. Your infrastructure matches the configuration.\"'),
    ('terraform_destroy_plan_prompt.png', 'Figure 4: Speculative Destruction Plan & Confirmation', 'Executing terraform destroy previewing destruction of local_file.student_file (- destroy), displaying plan: 0 to add, 0 to change, 1 to destroy, and prompting confirmation.'),
    ('terraform_destroy_complete_test_path.png', 'Figure 5: Resource Destruction Complete & Filesystem Verification', 'Terminal showing \"Destroy complete! Resources: 1 destroyed.\" followed by Test-Path .\\student.txt returning False, verifying total resource reclamation.')
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

# Section 6: State Management Table
h6 = doc.add_heading('6. Terraform State Lifecycle & Drift Detection Matrix', level=1)
h6.style.font.color.rgb = RGBColor(92, 78, 229)

st_data = [
    ('Phase / Operation', 'Target State in main.tf', 'Real-World Filesystem State', 'Recorded State in terraform.tfstate', 'Terraform Action Taken'),
    ('1. Pre-Apply', 'Declared student.txt', 'Absent (Does not exist)', 'Empty / Non-existent', 'Creates resource (+ create)'),
    ('2. Post-Apply', 'Declared student.txt', 'Present (Initial content)', 'Synced (ID: 06e6ae35...)', 'None (Fully converged)'),
    ('3. Modify main.tf', 'Updated 4-line text', 'Present (Initial content)', 'Old content recorded', 'In-place update (~ update)'),
    ('4. Re-run Apply', 'Updated 4-line text', 'Present (Updated content)', 'Synced (ID: 92663217...)', 'Zero changes (No drift detected)'),
    ('5. Destroy', 'Configuration remains', 'Resource deleted (False)', 'Purged (Instances: [])', 'Destroys resource (- destroy)')
]
st_tbl = doc.add_table(rows=len(st_data), cols=5)
for r_idx, r_vals in enumerate(st_data):
    for c_idx, val in enumerate(r_vals):
        st_tbl.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)
style_table(st_tbl, [Inches(1.3), Inches(1.5), Inches(1.5), Inches(1.4), Inches(1.3)])

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Section 7: Conclusion
h7 = doc.add_heading('7. Conclusion & Key Technical Takeaways', level=1)
h7.style.font.color.rgb = RGBColor(92, 78, 229)

p_c1 = doc.add_paragraph()
p_c1.add_run('1. Declarative Idempotency: ').bold = True
p_c1.add_run('Terraform ensures that running terraform apply multiple times against an unchanged configuration produces zero side-effects. The engine continuously drives real-world state toward the declared state without unneeded recreation.')

p_c2 = doc.add_paragraph()
p_c2.add_run('2. The Central Role of State (terraform.tfstate): ').bold = True
p_c2.add_run('The state file acts as the single source of truth, mapping declarative HCL identifiers (local_file.student_file) to concrete physical instances (file hashes, IDs). This allows Terraform to detect configuration drift and determine minimal delta actions.')

p_c3 = doc.add_paragraph()
p_c3.add_run('3. Predictable Safety via Speculative Planning: ').bold = True
p_c3.add_run('The separation between planning (terraform plan) and execution (terraform apply) provides guaranteed predictability, allowing engineers to audit additions, updates, or destructions before changes are executed.')

p_c4 = doc.add_paragraph()
p_c4.add_run('4. Clean Lifecycle De-Provisioning: ').bold = True
p_c4.add_run('Unlike manual deletions, terraform destroy leverages dependency graphs to systematically tear down managed assets in reverse order, ensuring zero orphaned resources.')

# Save to both target locations
out1 = r'D:\5th sem\CC\cloud_computing-\terraform-iac\Experiment_5_Terraform_IaC_Report.docx'
out2 = r'D:\5th sem\CC\Experiment_5_Terraform_IaC_Report.docx'
doc.save(out1)
doc.save(out2)
print(f'Successfully generated {out1}')
print(f'Successfully generated {out2}')
