import json
import uuid
import base64
import os
import boto3

s3 = boto3.client("s3")
sf = boto3.client("stepfunctions")

INPUT_BUCKET = os.environ["INPUT_BUCKET"]
STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST,OPTIONS"
}

def handler(event, context):
    body = json.loads(event["body"])
    image_b64 = body["image"].split(",")[1]
    
    job_id = str(uuid.uuid4())
    key = f"uploads/{job_id}.jpg"
    
    s3.put_object(
        Bucket=INPUT_BUCKET,
        Key=key,
        Body=base64.b64decode(image_b64),
        ContentType="image/jpeg"
    )
    
    sf.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps({
            "jobId": job_id,
            "bucket": INPUT_BUCKET,
            "key": key
        })
    )
    
    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "jobId": job_id
        })
    }