#!/bin/bash
echo "Perform operations with db"
python manage.py makemigrations
python manage.py migrate

echo "Work with static files"
python manage.py collectstatic --noinput
python manage.py compress
