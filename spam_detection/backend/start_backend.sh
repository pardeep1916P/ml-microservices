#!/bin/bash

# Start backend server
cd "$(dirname "$0")"

echo "🚀 Starting Spam Detection Backend..."

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

source venv/bin/activate

if [ ! -f "model.pkl" ]; then
    echo "⚠️  Model not found. Creating model..."
    python create_dummy_model.py
fi

echo "✓ Starting Flask server on http://localhost:5000"
echo "✓ Press Ctrl+C to stop the server"
echo ""

python app.py
