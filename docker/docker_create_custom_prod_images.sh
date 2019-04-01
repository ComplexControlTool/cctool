#!/bin/sh

# source "${CCTOOL}/docker/docker_cleanup_custom_images_containers.sh"
echo $'\n\t>> Creating docker images for prod cctool...\n'
docker-compose -f "${CCTOOL}/docker/docker-compose.prod.yml" build