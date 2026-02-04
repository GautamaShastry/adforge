import boto3
import json
import base64

bedrock = boto3.client("bedrock-runtime")
s3 = boto3.client("s3")

MODEL_ID = "amazon.titan-image-generator-v1"
OUTPUT_BUCKET = "adforge-output-bucket"

def handler(event, context):
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": f"Lifestyle product photography: {event['scene']}"
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 512,
                "width": 512
            }
        })
    )
    
    body = json.loads(response["body"].read())
    image = base64.b64decode(body["images"][0])
    
    key = f"{event['jobId']}/image.png"
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=key,
        Body=image,
        ContentType="image/png"
    )
    
    event["image"] = key
    return event