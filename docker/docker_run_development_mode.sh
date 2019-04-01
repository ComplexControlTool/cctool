#!/bin/sh

echo $'\n\t>> Retrieving required Docker images...\n'

run_dev()
{
  echo $'\n\t>> Running cctool as local...\n'
  docker-compose -f "${CCTOOL}/docker/docker-compose.local.yml" up -d
}

cctool_set=$(docker images -a | awk '{ print $1,$3 }' | grep cctool_local | awk '{ print $2 }' | wc -l)
if [ "$cctool_set" -eq "6" ]; then
  run_dev
else
  source "${CCTOOL}/docker/docker_create_custom_local_images.sh"
  run_dev
fi
