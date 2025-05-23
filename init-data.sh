#!/bin/bash

# Check if unzip is installed, install it if not
if ! command -v unzip &> /dev/null; then
    echo "unzip is not installed. Installing unzip..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y unzip
    elif command -v yum &> /dev/null; then
        sudo yum install -y unzip
    elif command -v brew &> /dev/null; then
        brew install unzip
    else
        echo "Cannot install unzip. Please install unzip manually and rerun the script."
        exit 1
    fi
fi

# Path to the ZIP file
ZIP_FILE="./backup/images-for-path-in-db.zip"
# Destination directory
DEST_DIR="be/static/images"

# Check if destination directory exists, create it if not
if [ ! -d "$DEST_DIR" ]; then
    echo "Directory $DEST_DIR does not exist. Creating it..."
    mkdir -p "$DEST_DIR"
fi

# Unzip the ZIP file into the destination directory without creating subdirectories
if [ -f "$ZIP_FILE" ]; then
    echo "Unzipping $ZIP_FILE into $DEST_DIR..."
    unzip -j "$ZIP_FILE" -d "$DEST_DIR"
    if [ $? -eq 0 ]; then
        echo "Unzipped successfully."
    else
        echo "Error unzipping the ZIP file."
        exit 1
    fi
else
    echo "File $ZIP_FILE does not exist."
    exit 1
fi

echo "Init data successfully!"