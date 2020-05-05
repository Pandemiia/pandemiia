#!/usr/bin/env sh
python manage.py migrate       
python manage.py collectstatic --noinput
/usr/sbin/nginx
exec gunicorn config.wsgi --bind=0.0.0.0:8000

