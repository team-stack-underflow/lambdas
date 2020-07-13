import os
import json
import boto3

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"][:-1]
    body = json.loads(event["body"])
    msg = body["input"]
    container_id = body["containerId"]
    url = "https://sqs.us-east-1.amazonaws.com/%s/%s-%s-input.fifo" % (os.environ["USER_ID"], connection_id, container_id)
    
    response = sqs.send_message(
        QueueUrl=url,
        MessageBody=msg,
        MessageDeduplicationId=event["requestContext"]["requestId"],
        MessageGroupId="ProgramInput"
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
