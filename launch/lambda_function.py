import os
import json
import boto3

ecs = boto3.client('ecs')
sqs = boto3.client('sqs')
lmb = boto3.client('lambda')

def lambda_handler(event, context):
    connection_id = event["requestContext"]["connectionId"][:-1]
    body = json.loads(event["body"])
    
    task_name = body["lang"] + "-" + body["mode"]
    container_id = event["requestContext"]["requestId"][:-1]
    queue_id = connection_id + "-" + container_id
    
    in_queue = sqs.create_queue(
        QueueName=queue_id+"-input.fifo",
        Attributes={
            "FifoQueue": "true"
        }
    )
    
    out_queue = sqs.create_queue(
        QueueName=queue_id+"-output.fifo",
        Attributes={
            "FifoQueue": "true"
        }
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

    if body["mode"] == "compile":
        src_queue = sqs.create_queue(
            QueueName=queue_id+"-src.fifo",
            Attributes={
                "FifoQueue": "true"
            }
        )
        sqs.send_message(
            QueueUrl=src_queue["QueueUrl"],
            MessageBody=body["prog"],
            MessageDeduplicationId="ProgramSrc",
            MessageGroupId="ProgramSrc"
        )
    
    ecs_response = ecs.run_task(
        count=1,
        cluster="runnable",
        launchType="FARGATE",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": [os.environ["SUBNET"]],
                "assignPublicIp": "ENABLED"
            }
        },
        overrides={
            "containerOverrides": [
                {
                    "name": "sandbox",
                    "environment": [
                        {
                            "name": "AWS_ACCESS_KEY_ID",
                            "value": os.environ["AWS_ACCESS_KEY_ID"]
                        },
                        {
                            "name": "AWS_SECRET_ACCESS_KEY",
                            "value": os.environ["AWS_SECRET_ACCESS_KEY"]
                        },
                        {
                            "name": "AWS_SESSION_TOKEN",
                            "value": os.environ["AWS_SESSION_TOKEN"]
                        },
                        {
                            "name": "USER_ID",
                            "value": os.environ["USER_ID"]
                        },
                        {
                            "name": "CLIENT_ID",
                            "value": connection_id,
                        },
                        {
                            "name": "RUN_ID",
                            "value": container_id,
                        }
                        ]
                    
                }
                ]
        },
        taskDefinition=task_name
    )

    # currently unused
    task_id = ecs_response["tasks"][0]["taskArn"].split("/")[1]
    
    return {
        "statusCode": 200,
        "body": json.dumps({"containerId": container_id})
    }
