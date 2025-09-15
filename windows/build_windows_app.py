#!/usr/bin/env python3
"""
Build script for creating Windows executable
This script automates the process of creating a standalone Windows application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller found: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        return run_command("pip install pyinstaller", "Installing PyInstaller")

def build_application():
    """Build the Windows application"""
    print("🚀 Building Pariksha for Windows...")
    print("="*60)

    # Check requirements
    if not check_requirements():
        print("❌ Failed to install required dependencies")
        return False

    # Get current directory
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")

    # Clean previous builds
    build_dirs = ['build', 'dist', '__pycache__']
    for dir_name in build_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            print(f"🧹 Cleaning {dir_name}...")
            shutil.rmtree(dir_path)

    # Build with PyInstaller
    if not run_command("pyinstaller app.spec --clean", "Building executable with PyInstaller"):
        return False

    # Create distribution folder
    dist_dir = current_dir / "Pariksha_Windows_App"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    dist_dir.mkdir()
    print(f"📦 Created distribution directory: {dist_dir}")

    # Copy built application
    app_source = current_dir / "dist" / "Pariksha"
    app_dest = dist_dir / "Pariksha"

    if app_source.exists():
        shutil.copytree(app_source, app_dest)
        print("✅ Application files copied to distribution folder")
    else:
        print("❌ Built application not found")
        return False

    # Copy additional files
    additional_files = [
        "README.md",
        "requirements.txt"
    ]

    for file_name in additional_files:
        source_file = current_dir / file_name
        if source_file.exists():
            shutil.copy2(source_file, dist_dir)
            print(f"📋 Copied {file_name}")

    # Create launcher batch file
    batch_content = '''@echo off
title Pariksha - Question Paper Drafting System for Teachers
echo Starting Pariksha - Question Paper Drafting System for Teachers...
echo.
echo The application will open in your web browser.
echo To stop the application, close this window.
echo.
cd /d "%~dp0"
"Pariksha\\Pariksha.exe"
pause
'''

    batch_file = dist_dir / "Start_Pariksha.bat"
    batch_file.write_text(batch_content)
    print("🚀 Created launcher batch file")

    # Create user guide
    user_guide = '''# Quick Start Guide

## Running the Application

1. Double-click "Start_Pariksha.bat"
2. Wait for the application to load (may take 30-60 seconds on first run)
3. The application will open in your default web browser
4. Start creating your question papers!

## Stopping the Application

- Close the command window that opened, OR
- Press Ctrl+C in the command window

## Troubleshooting

- If the browser doesn't open automatically, look for the URL in the command window
- Make sure no antivirus is blocking the executable
- For Windows Defender, you may need to "Allow" the application
- Ensure you have sufficient disk space (app requires ~200MB)

## System Requirements

- Windows 7 or later
- At least 4GB RAM
- 500MB free disk space
- Internet connection for initial setup

## Files and Folders

- `Pariksha/` - Main application files
- `Start_Pariksha.bat` - Double-click this to start
- `papers/` - Your saved question papers (created automatically)
- `metadata/` - Configuration files (created automatically)
- `downloads/` - Downloaded images and assets (created automatically)

For detailed usage instructions, see README.md
'''

    guide_file = dist_dir / "USER_GUIDE.txt"
    guide_file.write_text(user_guide)
    print("📖 Created user guide")

    # Create folders that will be needed
    folders_to_create = ['papers', 'metadata', 'downloads']
    for folder in folders_to_create:
        folder_path = dist_dir / folder
        folder_path.mkdir(exist_ok=True)

        # Create a placeholder file to keep the folder in version control
        placeholder = folder_path / ".gitkeep"
        placeholder.write_text("# This folder is used by the application\n")

    print("📁 Created necessary application folders")

    print("\n" + "="*60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print(f"📦 Distribution folder: {dist_dir}")
    print("\n📋 Next steps:")
    print("1. Test the application by running Start_Pariksha.bat")
    print("2. Zip the Pariksha_Windows_App folder for distribution")
    print("3. Share the zip file with users")
    print("\n💡 Tips:")
    print("- The first run may take longer as Windows extracts files")
    print("- Users may need to allow the app through Windows Defender")
    print("- Include the USER_GUIDE.txt in your distribution")

    return True

def main():
    """Main build function"""
    try:
        success = build_application()
        if success:
            input("\n✅ Build completed! Press Enter to exit...")
        else:
            input("\n❌ Build failed! Press Enter to exit...")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Build cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()