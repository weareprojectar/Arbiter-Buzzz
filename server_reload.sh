#! /bin/bash

python manage.py makemigrations
python manage.py migrate

systemctl restart uwsgi
systemctl restart nginx
