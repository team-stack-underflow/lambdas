import json
import boto3

ecs = boto3.client('ecs')
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]
    event = json.loads(event["body"])
    
    stop_response = ecs.stop_task(
        cluster='runnable',
        task=event["containerId"],
        reason="Killed by API call"
    )
    
    in_queue_name = connection_id + "-input.fifo"
    out_queue_name = connection_id + "-output.fifo"
    src_queue_name = connection_id + "-src.fifo"
    
    try:
        in_queue_url = sqs.get_queue_url(QueueName=in_queue_name)["QueueUrl"]
        out_queue_url = sqs.get_queue_url(QueueName=out_queue_name)["QueueUrl"]
        src_queue_url = sqs.get_queue_url(QueueName=src_queue_name)["QueueUrl"]
        
        sqs.purge_queue(QueueUrl=in_queue_url)
        sqs.purge_queue(QueueUrl=out_queue_url)
        sqs.purge_queue(QueueUrl=src_queue_url)
    except:
        pass
    
    return {
        'statusCode': 200,
        'body': json.dumps({"output": "Program stopped!"})
    }
