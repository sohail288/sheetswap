#!/bin/bash
source /home/ubuntu/sheetswap/.env_production && /home/ubuntu/sheetswap/web/bin/gunicorn  wsgi:application
