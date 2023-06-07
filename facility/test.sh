#!/bin/sh

DJANGO_SETTINGS_MODULE=facility.settings_test python manage.py wait_for_db
DJANGO_SETTINGS_MODULE=facility.settings_test python manage.py test
