#!/bin/bash

# Setup script for Recommendation System
echo "🚀 Setting up Recommendation System..."

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "🤖 Creating recommendation data..."
python create_dummy_model.py

if [ $? -eq 0 ]; then
    echo "✓ Recommendation data created successfully"
else
    echo "❌ Failed to create data"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  Backend: ./start_backend.sh"
echo "  Frontend: cd ../frontend && npm install && npm start"
echo ""
