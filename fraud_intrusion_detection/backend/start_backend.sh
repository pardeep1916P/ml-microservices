#!/bin/bash

# Start backend server
cd "$(dirname "$0")"

echo "🚀 Starting Fraud & Intrusion Detection Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if model exists
if [ ! -f "model.pkl" ]; then
    echo "⚠️  Model not found. Creating model..."
    python create_dummy_model.py
fi

echo "✓ Starting Flask server on http://localhost:5000"
echo "✓ Press Ctrl+C to stop the server"
echo ""

python app.py
