import aws_cdk as core
import aws_cdk.assertions as assertions

from chargepoint_notifier.chargepoint_notifier_stack import ChargepointNotifierStack

# example tests. To run these tests, uncomment this file along with the example
# resource in chargepoint_notifier/chargepoint_notifier_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ChargepointNotifierStack(app, "chargepoint-notifier")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
