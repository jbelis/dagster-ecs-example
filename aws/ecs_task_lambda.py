import logging
import boto3
import json
import os

# Initialize the ECS and S3 clients
ecs_client = boto3.client('ecs')
s3_client = boto3.client('s3')

# Define ECS Cluster and Task Definition
ecs_cluster = os.getenv("ECS_CLUSTER")
ecs_task_definition = os.getenv("ECS_TASK_DEFINITION")

ECS_LAUNCH_TYPE = 'FARGATE'  # Assuming Fargate, change to 'EC2' if needed

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event received: %s", json.dumps(event))

    # Get bucket name and file name from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
        
    logger.info(f"Triggering s3://{bucket}/{key} processing using cluster {ecs_cluster} and task {ecs_task_definition}")
    
    # Trigger the ECS task and pass the S3 file URL as an environment variable
    response = ecs_client.run_task(
        cluster=ecs_cluster,
        taskDefinition=ecs_task_definition,
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
                        },
                        {
                            'name': 'AWS_ACCESS_KEY_ID',
                            'value': os.getenv("AWS_ACCESS_KEY_ID")
                        },
                        {
                            'name': 'AWS_SECRET_ACCESS_KEY',
                            'value': os.getenv("AWS_SECRET_ACCESS_KEY")
                        }
                    ]
                }
            ]
        },
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [os.getenv("SUBNET_A"), os.getenv("SUBNET_B"), os.getenv("SUBNET_C")],  # Replace with your subnets
                'securityGroups': [os.getenv("SECURITY_GROUP")],  # Replace with your security groups
                'assignPublicIp': 'DISABLED'  # Set to DISABLED if you're using private subnets
            }
        }
    )
    
    # Log the ECS run task response for debugging
    logger.info("ECS task started: %s", json.dumps(response))
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"ECS task {ecs_task_definition} triggered for file {key}")
    }