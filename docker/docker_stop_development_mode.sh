#!/bin/sh

echo $'\n\t>> Stopping cctool as local...\n'
docker-compose -f "${CCTOOL}/docker/docker-compose.local.yml" stop
