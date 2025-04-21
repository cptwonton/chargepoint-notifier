#!/bin/bash

# Check if credentials are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <credentials_json>"
    echo "Example: $0 '{\"AccessKeyId\":\"ASIA...\",\"SecretAccessKey\":\"...\",\"SessionToken\":\"...\"}'"
    exit 1
fi

# Parse credentials from JSON
CREDS=$1
ACCESS_KEY=$(echo $CREDS | grep -o '"AccessKeyId":"[^"]*' | sed 's/"AccessKeyId":"//')
SECRET_KEY=$(echo $CREDS | grep -o '"SecretAccessKey":"[^"]*' | sed 's/"SecretAccessKey":"//')
SESSION_TOKEN=$(echo $CREDS | grep -o '"SessionToken":"[^"]*' | sed 's/"SessionToken":"//')

# Check if parsing was successful
if [ -z "$ACCESS_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$SESSION_TOKEN" ]; then
    echo "Failed to parse credentials. Make sure the JSON format is correct."
    exit 1
fi

# Export AWS credentials
export AWS_ACCESS_KEY_ID=$ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=$SECRET_KEY
export AWS_SESSION_TOKEN=$SESSION_TOKEN

# Load environment variables for region
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
  export AWS_REGION=$DEV_AWS_REGION
  export AWS_DEFAULT_REGION=$DEV_AWS_REGION
fi

# Verify credentials
echo "Verifying AWS credentials..."
aws sts get-caller-identity

# Run deploy script if credentials are valid
if [ $? -eq 0 ]; then
    echo "Credentials verified. Running deployment..."
    ./deploy.sh
else
    echo "Failed to verify credentials."
    exit 1
fi
