#!/bin/sh

# source "${CCTOOL}/docker/docker_cleanup_custom_images_containers.sh"
echo $'\n\t>> Creating docker images for local cctool...\n'
docker-compose -f "${CCTOOL}/docker/docker-compose.local.yml" build
