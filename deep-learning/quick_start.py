#!/usr/bin/env python3
"""
Quick Start Script for Chest X-Ray Analysis System
"""

import subprocess
import sys
import time
import webbrowser
import os
from threading import Timer

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python packages
    try:
        import flask
        import flask_cors
        import numpy
        import cv2
        import PIL
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python package: {e}")
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "numpy", "opencv-python", "pillow"])
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
        return False
    
    return True

def install_npm_packages():
    """Install npm packages if needed"""
    if not os.path.exists("node_modules"):
        print("📦 Installing React dependencies...")
        result = subprocess.run(["npm", "install"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ React dependencies installed")
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    else:
        print("✅ React dependencies already installed")
    return True

def start_backend():
    """Start the Flask backend"""
    print("🔧 Starting Flask API server...")
    try:
        process = subprocess.Popen([sys.executable, "backend_api.py"])
        time.sleep(3)  # Wait for server to start
        print("✅ API server started on http://localhost:5001")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend"""
    print("🎨 Starting React frontend...")
    try:
        process = subprocess.Popen(["npm", "start"])
        time.sleep(8)  # Wait for React to compile and start
        print("✅ Frontend started on http://localhost:3000")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def open_browser():
    """Open browser after delay"""
    time.sleep(2)
    try:
        webbrowser.open("http://localhost:3000")
        print("🌐 Browser opened automatically")
    except:
        print("🌐 Please manually open: http://localhost:3000")

def kill_ports():
    """Kill processes on common ports"""
    import subprocess
    
    ports = [5001, 8080, 3000, 5002, 5003]
    print("🧹 Cleaning up ports...")
    
    for port in ports:
        try:
            result = subprocess.run(["lsof", "-ti", f":{port}"], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        subprocess.run(["kill", "-9", pid], 
                                     stderr=subprocess.DEVNULL)
        except:
            pass
    
    print("✅ Ports cleaned")

def main():
    """Main function"""
    print("🏥 Chest X-Ray Medical Diagnosis System")
    print("=" * 50)
    print()
    
    # Clean up ports first
    kill_ports()
    
    # Check if we're in the right directory
    if not os.path.exists("backend_api.py"):
        print("❌ Please run this script from the deep-learning directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Install npm packages
    if not install_npm_packages():
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    # Open browser after delay
    Timer(3.0, open_browser).start()
    
    print()
    print("🚀 System is ready!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 API: http://localhost:5001")
    print()
    print("🔬 AI Model Features:")
    print("   • DenseNet-121 Deep Learning Architecture")
    print("   • Analyzes 14 Different Pathological Conditions")
    print("   • Professional Medical Reports with Confidence Scores")
    print("   • Interactive Web Interface with Visual Results")
    print()
    print("⚠️  Medical Disclaimer: Educational & Research Use Only")
    print()
    print("🛑 Press Ctrl+C to stop all servers")
    
    try:
        # Wait for user to stop
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ All servers stopped")

if __name__ == "__main__":
    main()