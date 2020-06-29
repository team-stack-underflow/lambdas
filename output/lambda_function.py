import json
import boto3

api = boto3.client("apigatewaymanagementapi", endpoint_url="https://s4tdw93cwd.execute-api.us-east-1.amazonaws.com/default/")

def lambda_handler(event, context):
    for message in event["Records"]:
        output = message["body"]
        destination = message["messageAttributes"]["client"]["stringValue"] + "="
        
        api.post_to_connection(
            Data=bytes(json.dumps({"output": output}), "utf-8"),
            ConnectionId=destination
        )
