#!/bin/sh

source "${CCTOOL}/docker/docker_cleanup_custom_images_containers.sh"
echo $'\n\t>> Creating docker images for cctool...\n'
docker build -f "${CCTOOL}/docker/Dockerfile_backend" -t cctool-backend .
docker build -f "${CCTOOL}/docker/Dockerfile_frontend" -t cctool-frontend .