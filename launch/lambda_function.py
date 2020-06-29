import os
import json
import boto3

ecs = boto3.client('ecs')
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    id = event["requestContext"]["connectionId"][:-1]
    event = json.loads(event["body"])
    
    task_name = event["lang"] + "-" + event["mode"]
    
    if event["mode"] == "compile":
        src_queue = sqs.get_queue_url(QueueName=id+"-src")
        sqs.send_message(
            QueueUrl=src_queue["QueueUrl"],
            MessageBody=event["prog"],
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
                            "name": "RUN_ID",
                            "value": id,
                        }
                        ]
                    
                }
                ]
        },
        taskDefinition=task_name
    )
    
    container_id = ecs_response["tasks"][0]["taskArn"].split("/")[1]
    
    return {
        "statusCode": 200,
        "body": json.dumps({"containerId": container_id})
    }
