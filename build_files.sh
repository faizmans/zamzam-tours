#!/bin/bash
echo "Building the project..."
# Use uv instead of pip
uv pip install -r requirements.txt --system

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear
