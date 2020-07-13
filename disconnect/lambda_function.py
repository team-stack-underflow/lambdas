import json
import boto3

sqs = boto3.client('sqs')
lmb = boto3.client('lambda')

def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"][:-1]

    queues = sqs.list_queues(QueueNamePrefix=connection_id)
    if "QueueUrls" in queues:
        for url in queues["QueueUrls"]:
            queue_arn = sqs.get_queue_attributes(
                QueueUrl=url,
                AttributeNames=["QueueArn"]
            )["Attributes"]["QueueArn"]

            # Delete mapping (for output queue only)
            out_queue_mappings = lmb.list_event_source_mappings(
                EventSourceArn=queue_arn,
                FunctionName="runnable-output"
            )["EventSourceMappings"]

            try:
                for mapping in out_queue_mappings:
                    lmb.delete_event_source_mapping(UUID=mapping["UUID"])
            except ResourceInUseException:
                print("Mapping still creating or updating")

            # Delete queue
            sqs.delete_queue(QueueUrl=url)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
