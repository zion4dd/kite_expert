#!/bin/bash

source /var/www/kite/venv/bin/activate

python3 /var/www/kite/kite_expert/manage.py collectstatic

echo ">> static collected. restarting 'kite' 3..2..1.."

systemctl restart kite.service

sleep 3

systemctl status kite

# ручной запуск сбора статики
