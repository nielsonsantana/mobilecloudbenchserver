#!/bin/bash

if [ "$1" != "" ]; then
    exec "$@"
    exit
fi


exec gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 3
