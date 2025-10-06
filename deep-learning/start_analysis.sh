#!/bin/bash

echo "🏥 Chest X-Ray Medical Diagnosis System"
echo "======================================="
echo ""

# Check if we're in the right directory
if [ ! -f "densenet.hdf5" ] && [ ! -f "backend_api.py" ]; then
    echo "❌ Please run this script from the deep-learning directory"
    exit 1
fi

# Kill any existing processes on our ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
lsof -ti:5002 | xargs kill -9 2>/dev/null || true
lsof -ti:5003 | xargs kill -9 2>/dev/null || true
echo "✅ Ports cleaned up"

# Start backend API
echo "🔧 Starting Flask API server..."
python3 backend_api.py &
API_PID=$!
echo "✅ API server started (PID: $API_PID) on http://localhost:5001"

# Wait for API to start
sleep 3

# Check if npm is available and node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing React dependencies..."
    npm install
fi

# Start React frontend
echo "🎨 Starting React frontend..."
npm start &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID) on http://localhost:3000"

# Wait for frontend to start
sleep 5

echo ""
echo "🚀 Enhanced System is ready!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 API: http://localhost:5001"
echo "📈 New Features: Visual Charts + PDF Reports"
echo ""
echo "🌐 Opening browser..."
# Try to open browser automatically
if command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
else
    echo "Please manually open: http://localhost:3000"
fi
echo ""
echo "📋 Enhanced Features Available:"
echo "   🔬 DenseNet-121 AI Model for Medical Analysis"
echo "   📸 Upload & Analyze Chest X-Ray Images"
echo "   🏥 Detect 14 Pathological Conditions:"
echo "      • Atelectasis, Cardiomegaly, Consolidation"
echo "      • Edema, Effusion, Emphysema, Fibrosis"
echo "      • Hernia, Infiltration, Mass, Nodule"
echo "      • Pleural Thickening, Pneumonia, Pneumothorax"
echo "   📊 Professional Medical Reports with Confidence Scores"
echo "   📈 Interactive Visual Charts (Bar, Pie, Radar, Severity)"
echo "   📄 PDF Report Generation with Charts & Analysis"
echo "   🎨 Interactive Web Interface with Visual Results"
echo ""
echo "⚠️  Medical Disclaimer: Educational & Research Use Only"
echo "    Always consult healthcare professionals for medical decisions"
echo ""
echo "🛑 Press Ctrl+C to stop all servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $API_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✅ All servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait