#!/bin/bash

# Setup script for Fraud & Intrusion Detection System
echo "🚀 Setting up Fraud & Intrusion Detection System..."

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create the ML model
echo "🤖 Creating ML model..."
python create_dummy_model.py

if [ $? -eq 0 ]; then
    echo "✓ Model created successfully"
else
    echo "❌ Failed to create model"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Run backend: ./start_backend.sh"
echo "  2. Open frontend: Open frontend/index.html in your browser"
echo ""
