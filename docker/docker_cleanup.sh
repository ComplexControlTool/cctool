#!/bin/sh

echo $'\n\t>> Stopping and Removing custom containers and images...\n'
source "${CCTOOL}/docker/docker_cleanup_custom_images_containers.sh"