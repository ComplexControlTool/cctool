#!/bin/sh

echo $'\n\t>> Stopping and Removing cctool containers and images...\n'
docker ps -a | awk '{ print $1,$2 }' | grep cctool-backend | awk '{print $1 }' | xargs -I {} docker stop {}
docker ps -a | awk '{ print $1,$2 }' | grep cctool-backend | awk '{print $1 }' | xargs -I {} docker rm {}
docker rmi cctool-backend
echo $'\n\t>> Stopping and Removing cctool-dashboard containers and images...\n'
docker ps -a | awk '{ print $1,$2 }' | grep cctool-frontend | awk '{print $1 }' | xargs -I {} docker stop {}
docker ps -a | awk '{ print $1,$2 }' | grep cctool-frontend | awk '{print $1 }' | xargs -I {} docker rm {}
docker rmi cctool-frontend