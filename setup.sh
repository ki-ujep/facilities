#!/bin/bash

# Ask for superadmin username into variable
echo -n "Enter superadmin username: "
read superadmin_username

# Ask for superuser password into variable
echo -n "Enter superadmin password: "
read -s superadmin_password
echo ""

# Copy media file to mount point
echo "Copying media files to mount point..."
cp -ar ./facility/media ./media
chown 1000:1000 -R ./media

# Start docker compose
echo "Starting docker compose..."
docker compose -f docker-compose-prod.yml up -d

# Run migrations
echo "Running migrations..."
docker compose -f docker-compose-prod.yml exec webapp sh -c "python manage.py migrate"

# Create superuser
echo "Creating superuser..."
PYCMD="from django.contrib.auth.models import User; User.objects.create_superuser('$superadmin_username', '', '$superadmin_password')"
docker compose -f docker-compose-prod.yml exec webapp sh -c "echo \"$PYCMD\" | python manage.py shell"

# Populate database
echo "Populating database..."
docker compose -f docker-compose-prod.yml cp ./fixtures webapp:/fixtures
docker compose -f docker-compose-prod.yml cp ./populate_db.sh webapp:/populate_db.sh
docker compose -f docker-compose-prod.yml exec webapp sh -c "cd / && sh /populate_db.sh"
