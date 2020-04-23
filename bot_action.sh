#!/bin/bash

. $(pipenv --venv)/bin/activate
(cd api_generic/ && gunicorn -w 4 api_generic.wsgi) &
python bot/runner.py
