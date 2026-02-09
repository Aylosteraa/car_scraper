#!/bin/sh
set -e

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL is up"

echo "Initializing database"
python init_db.py

echo "Starting scraper"
python main.py
echo "Finish scraper"
