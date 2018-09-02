#!/bin/sh

echo $'\n\t>> Stopping and Removing docker containers...\n'
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
echo $'\n\t>> Removing docker images...\n'
docker rmi $(docker images -a -q)
echo $'\n\t>> Removing docker volumes\n'
docker volume rm $(docker volume ls -f dangling=true -q)