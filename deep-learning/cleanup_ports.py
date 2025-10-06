#!/usr/bin/env python3
"""
Port Cleanup Utility for Chest X-Ray Analysis System
"""

import subprocess
import sys

def kill_port_processes():
    """Kill all processes on commonly used ports"""
    ports = [5001, 8080, 3000, 5002, 5003, 8000, 8888]
    
    print("🧹 Cleaning up ports for Chest X-Ray Analysis System...")
    print("=" * 50)
    
    killed_any = False
    
    for port in ports:
        try:
            # Find processes using the port
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"], 
                capture_output=True, 
                text=True
            )
            
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid:
                        try:
                            # Get process info before killing
                            proc_info = subprocess.run(
                                ["ps", "-p", pid, "-o", "comm="],
                                capture_output=True,
                                text=True
                            )
                            
                            process_name = proc_info.stdout.strip() if proc_info.stdout else "unknown"
                            
                            # Kill the process
                            subprocess.run(["kill", "-9", pid], stderr=subprocess.DEVNULL)
                            print(f"🔴 Killed process {pid} ({process_name}) on port {port}")
                            killed_any = True
                            
                        except Exception as e:
                            print(f"⚠️  Failed to kill process {pid}: {e}")
            else:
                print(f"✅ Port {port} is free")
                
        except FileNotFoundError:
            print("❌ 'lsof' command not found. Install it or run on macOS/Linux")
            return False
        except Exception as e:
            print(f"⚠️  Error checking port {port}: {e}")
    
    if not killed_any:
        print("\n🎉 All ports were already free!")
    else:
        print(f"\n✅ Port cleanup completed!")
    
    return True

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("Port Cleanup Utility")
        print("Usage: python3 cleanup_ports.py")
        print("Kills processes on ports: 5001, 8080, 3000, 5002, 5003, 8000, 8888")
        return
    
    success = kill_port_processes()
    
    if success:
        print("\n🚀 Ready to start Chest X-Ray Analysis System!")
        print("   Run: python3 run_system.py")
    else:
        print("\n❌ Port cleanup failed. You may need to manually kill processes.")

if __name__ == "__main__":
    main()