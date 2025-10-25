#!/usr/bin/env python3
"""
Startup script for the hybrid Amazon scraper system
This script will:
1. Install Python dependencies
2. Start the Flask server
3. Build the browser extension
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Starting Hybrid Amazon Scraper System")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('flask_server.py'):
        print("❌ Please run this script from the codemuse directory")
        sys.exit(1)
    
    # Step 1: Install Python dependencies
    print("\n📦 Step 1: Installing Python dependencies")
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("❌ Failed to install dependencies. Please check your Python installation.")
        sys.exit(1)
    
    # Step 2: Build the browser extension
    print("\n🔨 Step 2: Building browser extension")
    if not run_command("npm run build:extension", "Building React extension"):
        print("❌ Failed to build extension. Please check your Node.js installation.")
        sys.exit(1)
    
    # Step 3: Start the Flask server
    print("\n🌐 Step 3: Starting Flask server")
    print("The Flask server will start in the background...")
    print("You can access it at: http://localhost:5000")
    
    try:
        # Start Flask server in background
        flask_process = subprocess.Popen([
            sys.executable, 'flask_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get('http://localhost:5000/api/health', timeout=5)
            if response.status_code == 200:
                print("✅ Flask server started successfully!")
            else:
                print("⚠️ Flask server may not be running properly")
        except:
            print("⚠️ Could not verify Flask server status")
        
        print("\n" + "=" * 60)
        print("🎉 Setup Complete!")
        print("=" * 60)
        print("\n📋 Next Steps:")
        print("1. Load the extension:")
        print("   - Go to chrome://extensions/")
        print("   - Enable 'Developer mode'")
        print("   - Click 'Load unpacked'")
        print("   - Select the 'build' folder")
        print("\n2. Test the extension:")
        print("   - Visit an Amazon product page")
        print("   - Click the extension icon")
        print("   - Click 'Add Amazon Product'")
        print("\n3. View comparison:")
        print("   - Click 'View Full Comparison' in the extension")
        print("\n🔧 Server Info:")
        print("   - Flask API: http://localhost:5000")
        print("   - Health check: http://localhost:5000/api/health")
        print("   - Products API: http://localhost:5000/api/products")
        
        print(f"\n🔄 Flask server is running (PID: {flask_process.pid})")
        print("Press Ctrl+C to stop the server")
        
        # Keep the script running
        try:
            flask_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping Flask server...")
            flask_process.terminate()
            flask_process.wait()
            print("✅ Server stopped")
            
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
