#!/bin/bash
# Setup script for Phishing URL Detector - Backend

echo "================================"
echo "Setting up Phishing URL Detector Backend"
echo "================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python $(python --version) found"

# Navigate to backend directory
cd "$(dirname "$0")"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    echo "✓ Virtual environment activated"
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "❌ Could not activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create dummy model
echo "Creating dummy ML model..."
python create_dummy_model.py

echo ""
echo "================================"
echo "✓ Setup complete!"
echo "================================"
echo ""
echo "To start the backend server, run:"
echo "  source venv/Scripts/activate  (Windows Git Bash)"
echo "  source venv/bin/activate      (macOS/Linux)"
echo "  python app.py"
echo ""
