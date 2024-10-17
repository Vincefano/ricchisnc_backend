#!/bin/bash

MANAGEMENT="src/manage.py"

echo "Waiting for db..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo "Colleting statics..."
python $MANAGEMENT collectstatic --noinput

echo "Generating migrations"
python $MANAGEMENT makemigrations

echo "Applying migrations"
python $MANAGEMENT migrate

echo "Creating default oauth app"
python $MANAGEMENT default_oauth_app

echo "Avvio del server Django..."
python $MANAGEMENT runserver 0.0.0.0:8000
