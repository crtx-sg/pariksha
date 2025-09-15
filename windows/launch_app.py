#!/usr/bin/env python3
"""
Launcher script for Pariksha - Question Paper Drafting System for Teachers
This script automatically opens the web browser and starts the Streamlit app
"""

import os
import sys
import subprocess
import webbrowser
import time
import socket
from threading import Timer

def find_free_port():
    """Find a free port to run the application"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def open_browser(url):
    """Open the web browser after a delay"""
    time.sleep(3)  # Wait 3 seconds for the server to start
    webbrowser.open(url)

def main():
    """Main launcher function"""
    print("🚀 Starting Pariksha - Question Paper Drafting System for Teachers...")
    print("📚 Loading application dependencies...")

    # Get the directory where this script is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(app_dir, 'app.py')

    # Find a free port
    port = find_free_port()
    url = f"http://localhost:{port}"

    print(f"🌐 Application will open at: {url}")
    print("⏳ Please wait while the application loads...")
    print("\n" + "="*50)
    print("📖 INSTRUCTIONS:")
    print("1. The application will open in your default web browser")
    print("2. If the browser doesn't open automatically, copy the URL above")
    print("3. To stop the application, close this window or press Ctrl+C")
    print("="*50 + "\n")

    # Schedule browser opening
    timer = Timer(3.0, open_browser, [url])
    timer.start()

    try:
        # Start the Streamlit app
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', app_file,
            '--server.port', str(port),
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false',
            '--server.enableCORS', 'false',
            '--server.enableXsrfProtection', 'false'
        ]

        # Change to app directory
        os.chdir(app_dir)

        # Run the application
        subprocess.run(cmd, check=True)

    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except FileNotFoundError:
        print("❌ Error: Python or Streamlit not found")
        print("Please ensure Python and Streamlit are properly installed")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()