from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_iam as iam,
)
from constructs import Construct
import os
import json

class ChargepointNotifierStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # SNS Topic (optional for now)
        topic = sns.Topic(self, "ChargerAlertTopic")

        # Lambda function
        lambda_fn = _lambda.Function(
            self, "ChargepointPoller",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="poller.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                "SNS_TOPIC_ARN": topic.topic_arn,
                "STATION_NAME_FILTER": "BNA12",
                "BOUND_BOX_JSON": json.dumps({
                    "ne_lat": 36.16047351072966,
                    "ne_lon": -86.78688390221902,
                    "sw_lat": 36.159961361555496,
                    "sw_lon": -86.788501274255,
                })
            }
        )

        topic.grant_publish(lambda_fn)

        # IAM permissions (for logging + SNS)
        lambda_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["logs:*"],
            resources=["*"]
        ))

        # Schedule
        events.Rule(self, "PollEvery5Minutes",
            schedule=events.Schedule.rate(Duration.minutes(5)),
            targets=[targets.LambdaFunction(lambda_fn)]
        )
