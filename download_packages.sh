#!/bin/bash

# Execute the python script to download packages with fallback logic
if command -v python3 &>/dev/null; then
    python3 download_packages.py
elif command -v python &>/dev/null; then
    python download_packages.py
else
    echo "Error: Python is not installed. Please install Python to run this script." >&2
    exit 1
fi