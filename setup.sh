#!/bin/sh

# Build images for the web app
docker build -t ki-ujep/facilities .

# Copy media file to mount point
cp -ar ./facility/media ./media
chown 1000:1000 -R ./media

docker compose -f docker-compose-prod.yml up -d

# Run migrations
docker compose -f docker-compose-prod.yml exec webapp sh -c "python manage.py migrate"

# Populate database
docker compose -f docker-compose-prod.yml exec webapp sh -c "cd / && sh /populate_db.sh"

