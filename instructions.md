# ⚡️ChargePoint Notifier — Project Context and Progress

## 🎯 Ultimate Goal

Build a Python-based, AWS-hosted web app that notifies me (via email or SMS) **when a ChargePoint charger becomes available at my work building**. I only care about stations with names like **BNA12** at a specific lat/lon (Nashville).

This project should:
- Be deployable using **AWS CDK**
- Use **secure, engineer-friendly practices**
- Be **extendable later** (e.g. UI, analytics, multiple locations, etc.)

---

## ✅ Project Breakdown

### 1. **Data Collection**
- [x] Reverse engineered the ChargePoint map API by inspecting browser traffic.
- [x] Verified that no auth/session cookie is required (tested via Safari).
- [x] Identified a usable API: `https://mc.chargepoint.com/map-prod/v2`

### 2. **Polling System**
- [x] Designed an AWS Lambda to poll the endpoint.
- [x] Filters for `status_available: true` and station names containing "BNA12".
- [ ] Posts matching stations to SNS for downstream notifications (in progress).
- [ ] Only notify when state changes (planned future improvement).

### 3. **AWS Setup**
- [x] CDK Python project initialized via `cdk init app --language python`
- [x] Stack includes:
  - Lambda function (`poller.py`) polling ChargePoint
  - SNS topic
  - EventBridge rule triggering the Lambda every N minutes
  - Lambda environment variables:
    - `SNS_TOPIC_ARN`
    - `STATION_NAME_FILTER`
    - `BOUND_BOX_JSON`
- [x] Environment variables securely passed through CDK
- [ ] SNS subscriptions (email/SMS) not yet configured
- [ ] Future state caching to avoid redundant alerts

---

## 📍 Current Status

### Deployed Components:
- Python AWS CDK app with one stack
- `poller.py` inside `/lambda` directory
- Lambda triggers every 5 minutes
- Parses ChargePoint response
- Filters for `BNA12` stations
- Logs availability to CloudWatch

### Next Steps:
1. Add an SNS subscription for real notifications.
2. Implement caching (DynamoDB or S3) to detect changes in availability.
3. (Optional) Add retry/backoff logic to the request handling.
4. (Future) Expand to multi-building support, web UI, or analytics dashboard.

---

## 🔐 Security Practices
- AWS credentials are stored locally, not checked into GitHub.
- Using `.gitignore` to exclude `.venv`, `.env`, and sensitive files.
- CDK deploys infrastructure securely using AWS-managed IAM roles.

