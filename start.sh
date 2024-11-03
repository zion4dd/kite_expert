#! /usr/bin/env sh
set -e 

# python manage.py migrate

python3 /app/manage.py collectstatic --noinput

# gunicorn --workers 2 kite_expert.wsgi --bind 0.0.0.0:8000
gunicorn --workers 2 kite_expert.wsgi --bind unix:/var/run/kite/kite.sock
