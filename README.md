# ⚡️ ChargePoint Notifier

A Python-based, AWS-hosted application that notifies you when a ChargePoint charger becomes available at a specific location.

## 🎯 Project Overview

This project uses AWS CDK to deploy a serverless infrastructure that:
- Polls the ChargePoint API every 5 minutes
- Filters for available chargers at a specific location (currently BNA12 stations in Nashville)
- Sends notifications via SNS when chargers become available

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- AWS CLI configured with appropriate credentials
- AWS CDK installed

### Setup

1. Clone the repository
```
git clone https://github.com/cptwonton/chargepoint-notifier.git
cd chargepoint-notifier
```

2. Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Set up environment variables
```
cp .env.example .env
```
Edit the `.env` file with your AWS account details and configuration preferences.

5. Set up AWS credentials
   
   Option 1: Use existing credentials
   ```
   aws sts get-caller-identity
   ```
   If this fails, you may need to refresh your credentials.
   
   Option 2: Set credentials from JSON (useful with temporary credentials)
   ```
   ./set-aws-creds.sh '{"AccessKeyId":"ASIA...","SecretAccessKey":"...","SessionToken":"..."}'
   ```
   This will set the credentials and run the deployment automatically.

6. Deploy the stack (if using Option 1 for credentials)
```
./deploy.sh
```
The deployment script will use the `cloudauth-role` IAM role for deployment.

## 📋 Project Structure

- `app.py` - CDK application entry point
- `chargepoint_notifier/` - CDK stack definition
  - `chargepoint_notifier_stack.py` - Main stack definition
- `lambda/` - Lambda function code
  - `poller.py` - Main Lambda function that polls the ChargePoint API
- `deploy.sh` - Deployment script that loads environment variables
- `set-aws-creds.sh` - Helper script to set AWS credentials from JSON

## 🔧 Configuration

The application uses the following environment variables:
- `DEV_AWS_ACCOUNT` - AWS account ID for deployment
- `DEV_AWS_REGION` - AWS region for deployment
- `STATION_NAME_FILTER` - Filter for station names (default: "BNA12")
- `BOUND_BOX_JSON` - Geographic bounding box for the API query

## 📝 Future Enhancements

- Add state caching to avoid redundant notifications
- Implement a web UI for configuration
- Support multiple locations
- Add analytics dashboard

## 📚 Useful CDK Commands

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `./deploy.sh`     deploy this stack using environment variables
* `cdk diff`        compare deployed stack with current state
* `cdk docs`        open CDK documentation
