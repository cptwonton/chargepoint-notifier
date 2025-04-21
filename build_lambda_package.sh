#!/bin/bash

# Create a temporary directory for the package
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Copy Lambda code to the temp directory
cp -r lambda/* $TEMP_DIR/
echo "Copied Lambda code to temporary directory"

# Install dependencies
echo "Installing dependencies..."
pip install -r $TEMP_DIR/requirements.txt --target $TEMP_DIR --platform manylinux2014_x86_64 --only-binary=:all:

# Create a zip file
ZIP_FILE="lambda_package.zip"
echo "Creating zip file: $ZIP_FILE"
cd $TEMP_DIR
zip -r ../$ZIP_FILE .
cd ..

# Clean up
echo "Cleaning up temporary directory"
rm -rf $TEMP_DIR

echo "Lambda package created: $ZIP_FILE"
