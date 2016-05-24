#!/bin/bash
source ROOT_DIRECTORY/.env_production && VIRTUALENV_DIRECTORY/bin/celery -A app.celery_creator worker -l info