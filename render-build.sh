#!/usr/bin/env bash
# render-build.sh

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🛠 Running database migrations..."
python manage.py migrate

echo "⚙️ Collecting static files..."
python manage.py collectstatic --noinput
