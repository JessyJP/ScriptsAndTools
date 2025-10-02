#!/bin/bash

# Check if the correct number of arguments was provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <volume_name> <target_symlink_path>"
    exit 1
fi

# Assign arguments to variables
VOLUME_NAME="$1"
TARGET_SYMLINK_PATH="$2"

# Query the mountpoint of the specified Docker volume
MOUNTPOINT=$(docker volume inspect --format '{{ .Mountpoint }}' "$VOLUME_NAME")

# Check if the docker volume inspect command was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to query the mountpoint of the Docker volume '$VOLUME_NAME'."
    exit 1
fi

# Check if the target symlink path already exists
if [ -e "$TARGET_SYMLINK_PATH" ] || [ -L "$TARGET_SYMLINK_PATH" ]; then
    echo "NOTE: The target symlink path '$TARGET_SYMLINK_PATH' already exists."
    exit 1
fi

# Create a symbolic link from the mountpoint to the specified location
ln -s "$MOUNTPOINT" "$TARGET_SYMLINK_PATH"

# Verify and report success
if [ $? -eq 0 ]; then
    echo "Successfully created a symlink from '$MOUNTPOINT' to '$TARGET_SYMLINK_PATH'."
else
    echo "Error: Failed to create the symlink."
    exit 1
fi
