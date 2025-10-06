#!/bin/bash

echo "🏥 Starting Chest X-Ray Analysis System"
echo "======================================"

# Start backend server
echo "🔧 Starting Flask backend server..."
cd backend
python3 app.py &
BACKEND_PID=$!
echo "✅ Backend server started (PID: $BACKEND_PID) on http://localhost:5002"

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting React frontend server..."
cd ../frontend
npm start &
FRONTEND_PID=$!
echo "✅ Frontend server started (PID: $FRONTEND_PID) on http://localhost:3000"

echo ""
echo "🚀 System is ready!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5002"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user to stop
wait