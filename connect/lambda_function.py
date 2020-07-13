import json
import boto3

sqs = boto3.client('sqs')
lmb = boto3.client('lambda')

def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"][:-1]
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
