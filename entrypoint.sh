#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Ensure default admin user exists for container startup.
echo "Ensuring default superuser exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
password = 'admin'
user, created = User.objects.get_or_create(username=username, defaults={'is_staff': True, 'is_superuser': True, 'role': 'admin'})
if created:
    user.set_password(password)
    user.save()
    print('Created superuser: admin')
else:
    user.is_staff = True
    user.is_superuser = True
    if hasattr(user, 'role'):
        user.role = 'admin'
    user.set_password(password)
    user.save()
    print('Updated superuser password: admin')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting application..."
exec "$@"
