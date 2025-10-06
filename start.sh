#!/bin/bash

echo "🚀 Starting Chest X-Ray AI Analyzer..."
echo "=================================="

cd "$(dirname "$0")"

# Kill ALL processes on ALL ports
lsof -ti:3000,3001,5000,5001,5002 | xargs kill -9 2>/dev/null || true
sleep 3

# Install dependencies
npm install --silent 2>/dev/null || true
pip3 install -r requirements_enhanced.txt --quiet 2>/dev/null || true

echo "🔧 Starting servers..."

# Start final Node.js server on port 5002
node final_server.js &
SERVER_PID=$!
echo "🖥️ Backend started on port 5002"
sleep 3

# Start React on port 3001
PORT=3001 BROWSER=none npm start &
REACT_PID=$!
echo "🌐 Frontend started on port 3001"

echo "✅ All servers running!"
echo "🌐 Access: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop all servers"

trap 'kill $SERVER_PID $REACT_PID 2>/dev/null; lsof -ti:3001,5002 | xargs kill -9 2>/dev/null || true; exit' INT TERM

wait