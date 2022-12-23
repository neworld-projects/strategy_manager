#!/bin/bash

if [[ $(cat /etc/hostname) == celery ]]; then
    /usr/local/bin/celery -A strategy_manager worker -l info -Q celery --concurrency=1 -n celery@najva
fi
if [[ $(cat /etc/hostname) == celery-beat ]]; then
   /usr/local/bin/celery -A strategy_manager beat -l info -S django
fi
if [[ $(cat /etc/hostname) == tradingview-strategy-check ]]; then
   /usr/local/bin/celery -A strategy_manager worker -l info -Q tradingview_strategy_check --concurrency=1 -n tradingview_strategy_check@neworld
fi
if [[ $(cat /etc/hostname) == third-party-manager ]]; then
   /usr/local/bin/celery -A strategy_manager worker -l info -Q third_party_manager --concurrency=1 -n third_party_manager@neworld
fi
if [[ $(cat /etc/hostname) == app ]]; then
      mkdir /tmp/prom_metrics_uwsgi/najva/uwsgi
      /usr/local/bin/uwsgi --ini /usr/src/app/uwsgi/app.ini
fi
