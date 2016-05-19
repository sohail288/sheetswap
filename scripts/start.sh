#!/bin/bash

source ROOT_DIRECTORY/.env_production && VIRTUALENV_DIRECTORY/bin/gunicorn  wsgi:application
