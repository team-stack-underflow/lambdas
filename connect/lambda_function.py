import json
import boto3

sqs = boto3.client('sqs')
lmb = boto3.client('lambda')

def lambda_handler(event, context):
    id = event["requestContext"]["connectionId"][:-1]
    
    in_queue = sqs.create_queue(
        QueueName=id+"-input"
    )
    
    out_queue = sqs.create_queue(
        QueueName=id+"-output"
    )
    
    out_queue_arn = sqs.get_queue_attributes(
        QueueUrl=out_queue["QueueUrl"],
        AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]
    
    out_queue_bind = lmb.create_event_source_mapping(
        EventSourceArn=out_queue_arn,
        FunctionName='runnable-output',
        Enabled=True
    )
    
    src_queue = sqs.create_queue(
        QueueName=id+"-src"
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
