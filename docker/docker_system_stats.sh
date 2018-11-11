#!/bin/sh

echo $'\n\t>> Docker system info...\n'
docker system info
echo $'\n\t>> Docker disk usage...\n'
docker system df
echo $'\n\t>> Docker system events...\n'
docker system events