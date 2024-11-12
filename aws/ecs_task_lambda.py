import logging
import boto3
import json
import os
import re
from datetime import date, datetime

# Initialize the ECS and S3 clients
ecs_client = boto3.client('ecs')
s3_client = boto3.client('s3')

# initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ECS_LAUNCH_TYPE = 'FARGATE'  # Assuming Fargate, change to 'EC2' if needed

def custom_json_serializer(obj):
    """JSON serializer for objects not serializable by default json dumps serializer"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
    
    
def lambda_handler(event, context):
    logger.info("Event received: %s", json.dumps(event))
    
    # Get bucket name and file name from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    cluster = os.getenv("ECS_CLUSTER")
    task_definition = os.getenv("ECS_TASK_DEFINITION")
        
    logger.info(f"Triggering s3://{bucket}/{key} processing using cluster {cluster} and task {task_definition}")
    
    # Trigger the ECS task and pass the S3 file URL as an environment variable
    response = ecs_client.run_task(
        cluster=cluster,
        taskDefinition=task_definition,
        launchType=ECS_LAUNCH_TYPE,
        overrides={
            'containerOverrides': [
                {
                    'name': os.getenv("ECS_CONTAINER_NAME"),  # The name of the container in your task definition
                    'environment': [
                        {
                            'name': 'SOURCE_FILENAME',
                            'value': key
                        },
                        {
                            'name': 'AWS_BUCKET',
                            'value': bucket
                        }
                    ]
                }
            ]
        },
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': re.split(r"[ ,]+", os.getenv("SUBNETS")),
                'securityGroups': [os.getenv("SECURITY_GROUP")],
                'assignPublicIp': 'ENABLED'  # Set to DISABLED if you're using private subnets
            }
        }
    )
    
    # Log the ECS run task response for debugging
    logger.info("ECS task started: %s", json.dumps(response, default=custom_json_serializer))
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Task {task_definition} started for file {key}")
    }