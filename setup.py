#!/usr/bin/env python3
"""
Setup script for Mental Health Companion Bot
This script checks for required dependencies and sets up the initial environment
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is at least 3.7"""
    required_version = (3, 7)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current Python version is {current_version[0]}.{current_version[1]}.{current_version[2]}")
        sys.exit(1)
    
    print(f"✓ Python version {current_version[0]}.{current_version[1]}.{current_version[2]} detected")

def check_pip():
    """Check if pip is installed"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        print("✓ pip is installed")
        return True
    except subprocess.CalledProcessError:
        print("✗ pip is not installed")
        print("Please install pip before continuing.")
        return False

def install_requirements():
    """Install required packages from requirements.txt"""
    if not os.path.exists("requirements.txt"):
        print("✗ requirements.txt not found")
        return False
    
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All required packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install required packages")
        print("Please install packages manually with: pip install -r requirements.txt")
        return False

def initialize_data_files():
    """Create initial data files if they don't exist"""
    data_files = ["journal_entries.json", "mood_entries.json"]
    
    for file in data_files:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump({}, f)
            print(f"✓ Created {file}")
        else:
            print(f"✓ {file} already exists")

def main():
    """Main setup function"""
    print("Setting up Mental Health Companion Bot...")
    print("-" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check for pip
    if not check_pip():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("Setup may be incomplete. Please resolve package installation issues.")
    
    # Initialize data files
    initialize_data_files()
    
    print("-" * 50)
    print("Setup complete!")
    print("To run the application, use: streamlit run app.py")

if __name__ == "__main__":
    main()