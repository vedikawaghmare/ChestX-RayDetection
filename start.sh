#!/bin/bash

echo "🚀 Starting Chest X-Ray AI Analyzer..."
echo "=================================="

# Kill existing processes on ports
echo "🧹 Clearing ports..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:5000 | xargs kill -9 2>/dev/null || true
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
sleep 2

# Check dependencies
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not installed"
    exit 1
fi

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python not installed"
    exit 1
fi

if [ ! -f .env ]; then
    echo "❌ .env file not found"
    exit 1
fi

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

echo "🐍 Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements_enhanced.txt
else
    pip install -r requirements_enhanced.txt
fi

echo "🔧 Starting servers..."
echo "Python Backend: http://localhost:5001"
echo "Node.js Backend: http://localhost:5000"
echo "React Frontend: http://localhost:3000"
echo ""

# Start Python backend
echo "🐍 Starting Python backend..."
if command -v python3 &> /dev/null; then
    python3 python_backend_densenet.py &
else
    python python_backend_densenet.py &
fi
PYTHON_PID=$!
sleep 3

# Start Node.js backend
echo "🖥️ Starting Node.js backend..."
npm run server &
NODE_PID=$!
sleep 3

# Start React frontend
echo "🌐 Starting React frontend..."
npm start

# Cleanup on exit
echo "🛑 Stopping servers..."
kill $PYTHON_PID 2>/dev/null
kill $NODE_PID 2>/dev/null