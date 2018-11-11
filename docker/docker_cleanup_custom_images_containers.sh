#!/bin/sh

echo $'\n\t>> Stopping and Removing cctool containers and images...\n'
docker ps -a | awk '{ print $1,$2 }' | grep cctool | awk '{ print $1 }' | xargs -I {} docker stop {}
docker ps -a | awk '{ print $1,$2 }' | grep cctool | awk '{ print $1 }' | xargs -I {} docker rm {}
docker images -a | awk '{ print $1,$3 }' | grep cctool | awk '{ print $2 }' | xargs -I {} docker rmi {}
