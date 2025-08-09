#!/usr/bin/env python3
"""
Smart Investment Recommendation System
Main entry point for the application
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main function to run the investment advisor system"""
    print("🚀 Welcome to Smart Investment Recommendation System!")
    print("=" * 50)
    
    # Check if Python version is compatible
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return 1
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected")
        print("It's recommended to run this in a virtual environment")
        print("Run: python -m venv venv && venv\\Scripts\\activate")
    
    print("\n📋 Project Setup Status:")
    print("✅ Project structure created")
    print("✅ Dependencies listed in requirements.txt")
    print("✅ Environment template (.env.example) ready")
    
    print("\n🔧 Next Steps:")
    print("1. Install Python 3.8+ (https://python.org/downloads/)")
    print("2. Install Git (https://git-scm.com/download/win)")
    print("3. Create virtual environment: python -m venv venv")
    print("4. Activate virtual environment: venv\\Scripts\\activate")
    print("5. Install dependencies: pip install -r requirements.txt")
    print("6. Copy .env.example to .env and add your API keys")
    print("7. Run the application: python main.py")
    
    print("\n🌟 Ready to start building your investment advisor!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 