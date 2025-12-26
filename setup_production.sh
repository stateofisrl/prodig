#!/bin/bash
# Quick Production Setup Script for Linux/Mac
# Tesla Investment Platform

set -e

echo "========================================"
echo "Tesla Investment Platform"
echo "Production Setup Script"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Please install Python 3.14.0"
    exit 1
fi

echo "[1/8] Checking Python version..."
python3 --version

echo ""
echo "[2/8] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

echo ""
echo "[3/8] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[4/8] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "[5/8] Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found!"
    echo "Please create .env from .env.example and configure:"
    echo "- SECRET_KEY"
    echo "- DEBUG=False"
    echo "- ALLOWED_HOSTS=yourdomain.com"
    echo "- Database credentials"
    read -p "Press enter to continue..."
else
    echo ".env file exists"
fi

echo ""
echo "[6/8] Running migrations..."
python manage.py migrate

echo ""
echo "[7/8] Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "[8/8] Running deployment checks..."
python check_deployment.py

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Review check_deployment.py results"
echo "2. Create superuser: python manage.py createsuperuser"
echo "3. Test locally: python manage.py runserver"
echo "4. Configure web server (Nginx)"
echo "5. Set up Gunicorn"
echo "6. Enable SSL"
echo ""
echo "See DEPLOYMENT.md for detailed instructions"
echo ""
