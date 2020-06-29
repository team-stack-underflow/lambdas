import os
import json
import boto3

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    id = event["requestContext"]["connectionId"][:-1]
    event = json.loads(event["body"])
    msg = event["input"]
    url = "https://sqs.us-east-1.amazonaws.com/%s/%s-input" % (os.environ["USER_ID"], id)
    
    response = sqs.send_message(
        QueueUrl=url,
        MessageBody=msg
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
