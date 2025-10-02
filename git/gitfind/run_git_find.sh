#!/bin/bash
# Convert files to Unix format
dos2unix gitfind.py
dos2unix visualization.py
dos2unix git_operations.py
dos2unix run_git_find.sh

# Ensure the Python script is executable (only if you intend to run it as an executable)
chmod +x gitfind.py

# Execute the Python script
./gitfind.py
