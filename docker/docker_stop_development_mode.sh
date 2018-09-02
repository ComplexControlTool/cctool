#!/bin/sh

echo $'\n\t>> Stopping cctool container in development serving mode...\n'
cd "${CCTOOL}/docker" && docker-compose stop