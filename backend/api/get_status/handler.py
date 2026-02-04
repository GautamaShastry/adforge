import json
import boto3

s3 = boto3.client("s3")
OUTPUT_BUCKET = "adforge-output-bucket"

def handler(event, context):
    job_id = event["queryStringParameters"]["jobId"]
    key = f"{job_id}/manifest.json"
    
    try:
        obj = s3.get_object(Bucket=OUTPUT_BUCKET, Key=key)
        manifest = json.loads(obj["Body"].read())
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "COMPLETED",
                "data": manifest
            })
        }
    except s3.exceptions.NoSuchKey:
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "IN_PROGRESS"})
        }