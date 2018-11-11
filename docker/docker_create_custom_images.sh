#!/bin/sh

source "${CCTOOL}/docker/docker_cleanup_custom_images_containers.sh"
echo $'\n\t>> Creating docker images for cctool...\n'
docker-compose -f "${CCTOOL}/docker/docker-compose.local.yml" build
# docker-compose -f docker-compose.prod.yml build