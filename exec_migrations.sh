#!/bin/bash

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Deactivate the virtual environment if applicable
# Uncomment the following line if you activated a virtual environment
# deactivate

echo "Migrations executed successfully."

