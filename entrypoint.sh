#!/bin/sh
set -e

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Docker entrypoint..."

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Migrating Beanie..."
if ! python migrate_beanie.py; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Failed to migrate Beanie"
    exit 1
fi
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Beanie migrated successfully"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Launching the application..."
if ! python launch_app.py; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Failed to launch the application"
    exit 1
fi
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Application launched successfully"
