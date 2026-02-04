import json
import uuid
import base64
import boto3 # AWS SDK for Python(let's you call AWS services without explicit authentication)


s3 = boto3.client("s3")
sf = boto3.client("stepfunctions")

account_id = boto3.client("sts").get_caller_identity()["Account"]

INPUT_BUCKET = "adforge-input-bucket"
STATE_MACHINE_ARN = f"arn:aws:states:us-east-1:{account_id}:stateMachine:adforge-pipeline"

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
        "body": json.dumps({
            "jobId": job_id
        })
    }