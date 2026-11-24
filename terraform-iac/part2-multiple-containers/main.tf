terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Nginx Docker image
resource "docker_image" "nginx" {
  name = "nginx:alpine"
}

# Python Docker image
resource "docker_image" "python" {
  name = "python:3.12-slim"
}

# Nginx container
resource "docker_container" "webserver" {
  name  = "terraform-nginx"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = 8082
  }
}

# Python HTTP server container
resource "docker_container" "python_app" {
  name  = "terraform-python"
  image = docker_image.python.image_id

  command = [
    "python",
    "-m",
    "http.server",
    "8000"
  ]

  ports {
    internal = 8000
    external = 8081
  }
}