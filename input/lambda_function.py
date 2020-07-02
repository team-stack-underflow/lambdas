import os
import json
import boto3

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    id = event["requestContext"]["connectionId"][:-1]
    msg = json.loads(event["body"])["input"]
    url = "https://sqs.us-east-1.amazonaws.com/%s/%s-input.fifo" % (os.environ["USER_ID"], id)
    
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
