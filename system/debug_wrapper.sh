#!/bin/bash

# Check if the correct number of arguments was provided (expecting 1)
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 path_to_script"
    exit 1
fi

SCRIPT_PATH="$1"

# Ensure the script file exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Script file not found at $SCRIPT_PATH"
    exit 1
fi

# Run the script in debug mode, pausing after each line
while IFS= read -r line || [ -n "$line" ]; do
    # Print the line
    echo "+ $line"

    # Execute the line in a subshell
    bash -c "$line"

    # Wait for user input to continue
    read -p "Press [Enter] to continue..."
done < "$SCRIPT_PATH"
