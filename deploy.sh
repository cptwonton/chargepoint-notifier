#!/bin/bash

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
  echo "Environment variables loaded from .env"
else
  echo "No .env file found. Please create one based on .env.example"
  exit 1
fi

# Check if required environment variables are set
if [ -z "$DEV_AWS_ACCOUNT" ] || [ -z "$DEV_AWS_REGION" ]; then
  echo "Required environment variables DEV_AWS_ACCOUNT and/or DEV_AWS_REGION are not set"
  exit 1
fi

# Deploy the stack
echo "Deploying to AWS account $DEV_AWS_ACCOUNT in region $DEV_AWS_REGION"
cdk deploy "$@"
