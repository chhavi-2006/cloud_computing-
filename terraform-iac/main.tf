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

  content = <<-EOT
    Welcome to Terraform!
    Infrastructure as Code is powerful.
    Modified using Terraform.
    Experiment completed successfully.
  EOT
}
