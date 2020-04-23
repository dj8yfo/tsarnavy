#!/bin/bash

pipenv install
pushd api_generic/
. $(pipenv --venv)/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py test post_liker


