#!/bin/sh

echo $'\n\t>> Retrieving required Docker images...\n'

run_dev()
{
  echo $'\n\t>> Running cctool as local...\n'
  if [ "$(uname)" == "Darwin" ]; then
    docker-compose -f "${CCTOOL}/docker/docker-compose.local.yml" -f "${CCTOOL}/docker/docker-compose.local.override.yml" up -d
  else
    docker-compose -f "${CCTOOL}/docker/docker-compose.local.yml" up -d
  fi
}

cctool_set=$(docker images -a | awk '{ print $1,$3 }' | grep cctool_local | awk '{ print $2 }' | wc -l)
if [ "$cctool_set" -eq "6" ]; then
  run_dev
else
  source "${CCTOOL}/docker/docker_create_custom_images.sh"
  run_dev
fi
