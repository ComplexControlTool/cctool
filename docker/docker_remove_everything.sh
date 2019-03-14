#!/bin/sh

echo $'\n\t>> Stopping and Removing docker containers...\n'
docker stop $(docker ps -a -q)
docker rm -f $(docker ps -a -q)
echo $'\n\t>> Removing docker images...\n'
docker rmi -f $(docker images -a -q)
echo $'\n\t>> Removing docker volumes\n'
docker volume rm -f $(docker volume ls -q)
echo $'\n\t>> Removing docker networks\n'
docker network rm -f $(docker network ls -q)
echo $'\n\t>> Removing any docker unused data\n'
docker system prune -f -a