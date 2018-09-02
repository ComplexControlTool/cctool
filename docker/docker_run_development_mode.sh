#!/bin/sh

echo $'\n\t>> Retrieving required Docker images...\n'

run_dev()
{
  echo $'\n\t>> Running cctool container in development serving mode...\n'
  cd "${CCTOOL}/docker" && docker-compose up -d cctool-dev
}

backendexists=$(docker images -q cctool-backend)
frontendexists=$(docker images -q cctool-frontend)
if [ -n "$backendexists" ] && [ -n "$frontendexists" ]; then
  run_dev
else
  source "${CCTOOL}/docker/docker_create_custom_images.sh"
  run_dev
fi