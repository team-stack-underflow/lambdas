import json
import boto3

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    id = event["requestContext"]["connectionId"][:-1]
    
    in_queue_name = id + "-input.fifo"
    out_queue_name = id + "-output.fifo"
    src_queue_name = id + "-src.fifo"
    
    in_queue_url = sqs.get_queue_url(QueueName=in_queue_name)["QueueUrl"]
    out_queue_url = sqs.get_queue_url(QueueName=out_queue_name)["QueueUrl"]
    src_queue_url = sqs.get_queue_url(QueueName=src_queue_name)["QueueUrl"]
    
    sqs.delete_queue(QueueUrl=in_queue_url)
    sqs.delete_queue(QueueUrl=out_queue_url)
    sqs.delete_queue(QueueUrl=src_queue_url)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
