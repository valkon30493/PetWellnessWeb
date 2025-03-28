#!/usr/bin/env bash
# render-build.sh

echo "🛠 Collecting static files..."
python manage.py collectstatic --no-input
