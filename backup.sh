#!/bin/sh
set -e

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

pg_dump \
  -h db \
  -U "$POSTGRES_USER" \
  "$POSTGRES_DB" \
  > /app/dumps/backup_$TIMESTAMP.sql
