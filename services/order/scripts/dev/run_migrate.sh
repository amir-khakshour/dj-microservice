#!/bin/sh

# wait for PSQL server to start
while ! curl --max-time 30 http://${POSTGRES_HOST}:5432/ 2>&1 | grep '52'
do
    echo "Waiting for database..."
    sleep 1
done

python3 manage.py makemigrations
python3 manage.py migrate --no-input
