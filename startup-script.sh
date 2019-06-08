#!/bin/bash
# startup-script.sh

set -e

>&2 echo "Beginning startup script"

# Setting up a delay to allow the postgres service to finish setting up before running Django commands.
>&2 echo "Starting sleep"
sleep 10
>&2 echo "Finished sleep"

python smilewidgets/manage.py makemigrations
python smilewidgets/manage.py migrate
python smilewidgets/manage.py loaddata 0001_fixtures.json
exec python smilewidgets/manage.py runserver 0.0.0.0:8000
