#!/bin/bash
# Startup script for Render deployment
# Generates synthetic data before starting Streamlit

echo "YottaFlex Startup: Generating synthetic data..."
python generator.py

if [ $? -eq 0 ]; then
    echo "✅ Data generation successful!"
    echo "Starting Streamlit dashboard..."
    streamlit run yottaflex_unified_dashboard.py --server.port=8501 --server.address=0.0.0.0
else
    echo "❌ Data generation failed!"
    exit 1
fi
