#!/usr/bin/env python3
"""
Simple API Test

Test the FastAPI application without Docker.
"""

import sys
import subprocess
import time
import requests
import json
from pathlib import Path

def install_requirements():
    """Install basic requirements for testing."""
    requirements = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "python-multipart==0.0.6"
    ]
    
    print("📦 Installing API requirements...")
    for req in requirements:
        print(f"   Installing {req}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", req
        ])

def test_api():
    """Test the API endpoints."""
    print("\n🧪 Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test endpoints
    endpoints = [
        "/",
        "/health",
        "/docs",
        "/api/v1/auth/me"
    ]
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"   Testing {url}...")
            
            if endpoint == "/api/v1/auth/me":
                # This requires auth, so we expect 401
                response = requests.get(url, timeout=5)
                if response.status_code == 401:
                    print(f"   ✅ {endpoint} - Authentication required (expected)")
                else:
                    print(f"   ⚠️  {endpoint} - Status: {response.status_code}")
            else:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {endpoint} - OK")
                else:
                    print(f"   ❌ {endpoint} - Status: {response.status_code}")
                    
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {endpoint} - Connection failed (API not running?)")
        except Exception as e:
            print(f"   ❌ {endpoint} - Error: {str(e)}")

def start_api_server():
    """Start the API server."""
    print("\n🚀 Starting API server...")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop")
    
    try:
        # Change to api directory and start server
        import os
        os.chdir("api")
        
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app",
            "--reload",
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 API server stopped")
    except FileNotFoundError:
        print("❌ Could not find API files. Make sure you're in the project root.")
    except Exception as e:
        print(f"❌ Error starting API server: {str(e)}")

def main():
    print("🧪 AgenticAI Lab API Test")
    print("=" * 30)
    
    # Install requirements
    install_requirements()
    
    # Check if we should start the server or test it
    import sys
    if "--start" in sys.argv:
        start_api_server()
    elif "--test" in sys.argv:
        test_api()
    else:
        print("\nOptions:")
        print("  --start    Start the API server")
        print("  --test     Test API endpoints (server must be running)")
        print("\nExample:")
        print("  python test_api.py --start")

if __name__ == "__main__":
    main()
