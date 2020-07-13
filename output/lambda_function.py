import json
import boto3

api = boto3.client("apigatewaymanagementapi", endpoint_url="https://s4tdw93cwd.execute-api.us-east-1.amazonaws.com/default/")

def lambda_handler(event, context):
    for message in event["Records"]:
        output = message["body"]
        attributes = message["messageAttributes"]
        destination = attributes["client"]["stringValue"] + "="
        container_id = attributes["containerId"]["stringValue"]
        
        api.post_to_connection(
            Data=bytes(json.dumps({"output": output, "containerId": container_id}), "utf-8"),
            ConnectionId=destination
        )
