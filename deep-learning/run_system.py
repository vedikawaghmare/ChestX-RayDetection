#!/usr/bin/env python3
"""
Complete Chest X-Ray Analysis System Launcher
"""

import subprocess
import sys
import time
import webbrowser
import os
import http.server
import socketserver
from threading import Thread
import signal

def start_backend():
    """Start Flask backend"""
    print("🔧 Starting Flask API server...")
    try:
        process = subprocess.Popen([sys.executable, "backend_api.py"])
        time.sleep(3)
        print("✅ API server running on http://localhost:5001")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_html_server():
    """Start simple HTTP server for HTML page"""
    print("🌐 Starting web server...")
    
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        PORT = 8080
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"✅ Web server running on http://localhost:{PORT}")
            
            # Open browser
            def open_browser():
                time.sleep(2)
                webbrowser.open(f"http://localhost:{PORT}")
            
            Thread(target=open_browser, daemon=True).start()
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")

def kill_existing_processes():
    """Kill any existing processes on our ports"""
    import subprocess
    
    ports = [5001, 8080, 3000, 5002, 5003]
    print("🧹 Cleaning up existing processes...")
    
    for port in ports:
        try:
            # Kill processes on port
            subprocess.run(["lsof", "-ti", f":{port}"], 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            subprocess.run(["lsof", "-ti", f":{port}"], 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = subprocess.run(["lsof", "-ti", f":{port}"], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        subprocess.run(["kill", "-9", pid], 
                                     stderr=subprocess.DEVNULL)
        except:
            pass  # Port not in use or kill failed
    
    print("✅ Ports cleaned up")

def main():
    """Main function"""
    print("🏥 Chest X-Ray Medical Diagnosis System")
    print("=" * 50)
    
    # Kill existing processes first
    kill_existing_processes()
    
    # Check if we're in the right directory
    if not os.path.exists("backend_api.py") or not os.path.exists("index.html"):
        print("❌ Missing required files. Please run from deep-learning directory.")
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    print()
    print("🚀 System Features:")
    print("   🧠 DenseNet-121 AI Model")
    print("   🔍 14 Pathological Conditions Detection")
    print("   📊 Professional Medical Reports")
    print("   🎨 Interactive Web Interface")
    print()
    print("⚠️  Educational Use Only - Not for Medical Diagnosis")
    print()
    print("🌐 Opening web interface...")
    
    try:
        # Start web server (this will block)
        start_html_server()
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        backend_process.terminate()
        print("✅ System stopped")

if __name__ == "__main__":
    main()