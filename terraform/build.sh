#!/bin/bash

# Build Lambda deployment package
echo "Building Lambda deployment package..."

# Create temp directory
rm -rf lambda_package
mkdir -p lambda_package

# Copy source code
cp -r ../src lambda_package/
cp lambda_handler.py lambda_package/

# Create zip
cd lambda_package
zip -r ../lambda_function.zip . -x "*.pyc" -x "__pycache__/*"
cd ..

# Cleanup
rm -rf lambda_package

echo "Lambda package created: lambda_function.zip"
