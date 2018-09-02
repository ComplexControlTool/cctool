#!/usr/bin/env bash

echo $'\n\t C C T O O L  D A S H B O A R D  D E V \n'
sleep 5
echo $'\n\t>> Checking for updates in the project environment...\n'
npm install
bower install --config.interactive=false --allow-root
echo $'\n\t>> Running dashboard in development mode...\n'
gulp watch:django