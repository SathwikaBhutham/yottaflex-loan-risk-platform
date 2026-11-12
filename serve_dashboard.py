#!/usr/bin/env python3
"""
Serve YottaFlex responsive HTML dashboard
Generates synthetic data, then serves dashboard via HTTP server
"""

import subprocess
import sys
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

def get_free_port():
    """Get a free port on localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    print("=" * 70)
    print("YottaFlex Dashboard Server")
    print("=" * 70)

    # Step 1: Generate synthetic data
    print("\n📊 Step 1: Generating synthetic data...")
    print("-" * 70)
    result = subprocess.run([sys.executable, "generator.py"], cwd=os.getcwd())

    if result.returncode != 0:
        print("\n❌ Data generation failed!")
        sys.exit(1)

    print("\n✅ Data generation successful!")

    # Step 2: Validate data
    print("\n✅ Step 2: Data validation skipped (validation done on generation)")

    # Step 3: Start HTTP server
    print("\n🌐 Step 3: Starting HTTP server...")
    print("-" * 70)

    # For Render, use port 8080 (or environment variable)
    port = int(os.environ.get('PORT', 8080))

    # Change to project directory
    os.chdir(os.getcwd())

    class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
        """HTTP handler that serves files from current directory"""

        def log_message(self, format, *args):
            """Log HTTP requests"""
            if '404' not in format:
                print(f"  {self.client_address[0]} - {format % args}")

        def do_GET(self):
            """Handle GET requests - serve HTML dashboard by default"""
            if self.path == '/' or self.path == '':
                self.path = '/yottaflex_responsive_dashboard.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    try:
        server = HTTPServer(('0.0.0.0', port), QuietHTTPRequestHandler)
        print(f"\n{'=' * 70}")
        print(f"✅ Dashboard Server Running!")
        print(f"{'=' * 70}")
        print(f"\n🌐 Dashboard URL: http://0.0.0.0:{port}")
        print(f"📱 Local Access: http://localhost:{port}")
        print(f"🔗 On Render: https://yottaflex-loan-risk-platform.onrender.com")
        print(f"\nPress CTRL+C to stop server")
        print(f"{'=' * 70}\n")

        server.serve_forever()

    except KeyboardInterrupt:
        print("\n\n✅ Server stopped gracefully")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
