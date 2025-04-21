#!/usr/bin/env python3
import os

import aws_cdk as cdk

from chargepoint_notifier.chargepoint_notifier_stack import ChargepointNotifierStack


app = cdk.App()
ChargepointNotifierStack(app, "ChargepointNotifierStack",
    # Use environment variables for AWS account and region
    # This allows you to keep your AWS account details out of your code
    env=cdk.Environment(
        account=os.environ.get('CDK_DEPLOY_ACCOUNT', os.environ.get('CDK_DEFAULT_ACCOUNT')),
        region=os.environ.get('CDK_DEPLOY_REGION', os.environ.get('CDK_DEFAULT_REGION'))
    ),
    )

app.synth()
