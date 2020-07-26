import json
import boto3

api = boto3.client("apigatewaymanagementapi", endpoint_url="https://s4tdw93cwd.execute-api.us-east-1.amazonaws.com/default/")

box_suffix = "-boxed"

def lambda_handler(event, context):
    for message in event["Records"]:
        output = message["body"][:-len(box_suffix)]
        attributes = message["messageAttributes"]
        destination = attributes["client"]["stringValue"] + "="
        container_id = attributes["containerId"]["stringValue"]
        
        api.post_to_connection(
            Data=bytes(json.dumps({"output": output, "containerId": container_id}), "utf-8"),
            ConnectionId=destination
        )
