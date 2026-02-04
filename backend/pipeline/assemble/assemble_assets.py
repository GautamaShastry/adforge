import json
import boto3

s3 = boto3.client("s3")
OUTPUT_BUCKET = "adforge-output-bucket"

def handler(event, context):
    manifest = {
        "script": event["script"],
        "audio": event["audio"],
        "image": event["image"]
    }
    
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=f"{event['jobId']}/manifest.json",
        Body=json.dumps(manifest, indent=2),
        ContentType="application/json"
    )
    
    return event