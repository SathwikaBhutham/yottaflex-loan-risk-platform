#!/usr/bin/env python3
"""
Startup script for Render deployment
Generates synthetic data before starting Streamlit
"""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("YottaFlex Startup: Generating synthetic data...")
    print("=" * 60)

    # Run generator
    result = subprocess.run([sys.executable, "generator.py"], cwd=os.getcwd())

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ Data generation successful!")
        print("=" * 60)
        print("\nStarting Streamlit dashboard...")
        print("=" * 60)

        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "yottaflex_unified_dashboard.py",
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ])
    else:
        print("\n" + "=" * 60)
        print("❌ Data generation failed!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
