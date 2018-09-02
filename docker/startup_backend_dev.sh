#!/usr/bin/env bash

echo $'\n\t C C T O O L  D E V \n'
sleep 5
echo $'\n\t>> Checking for updates in the project environment...\n'
ls -ll
pip install --no-cache-dir -r requirements.txt
echo $'\n\t>> Removing any python cache...\n'
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
echo $'\n\t>> Setting up django web app...\n'
python manage.py migrate auth
python manage.py migrate
python manage.py makemigrations
echo $'\n\t>> Running django web app (0.0.0.0:8000)...\n'
python manage.py runserver 0.0.0.0:8000