#!/bin/sh

echo $'\n\t>> Retrieving required Docker images...\n'

run_prod()
{
  echo $'\n\t>> Running cctool for production...\n'
  docker-compose -f "${CCTOOL}/docker/docker-compose.prod.yml" up -d
}

cctool_set=$(docker images -a | awk '{ print $1,$3 }' | grep cctool_prod | awk '{ print $2 }' | wc -l)
if [ "$cctool_set" -eq "6" ]; then
  run_prod
else
  source "${CCTOOL}/docker/docker_create_custom_prod_images.sh"
  run_prod
fi
