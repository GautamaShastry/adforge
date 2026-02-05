import os
import json
import boto3

s3 = boto3.client("s3")
OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]

def generate_presigned_url(key, expiration=3600):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": OUTPUT_BUCKET, "Key": key},
        ExpiresIn=expiration
    )

def handler(event, context):
    audio_url = generate_presigned_url(event["audio"])
    image_url = generate_presigned_url(event["image"])
    
    manifest = {
        "script": event["script"],
        "audioUrl": audio_url,
        "imageUrl": image_url
    }
    
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=f"{event['jobId']}/manifest.json",
        Body=json.dumps(manifest, indent=2),
        ContentType="application/json"
    )
    
    return event