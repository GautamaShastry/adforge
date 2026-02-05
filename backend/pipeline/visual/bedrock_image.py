import os
import json
import base64
import boto3

bedrock = boto3.client("bedrock-runtime")
s3 = boto3.client("s3")

MODEL_ID = "amazon.titan-image-generator-v2:0"
OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]

def handler(event, context):
    # Truncate scene to fit within 512 char limit
    scene = event.get('scene', 'Product showcase')[:400]
    prompt = f"Professional product photography: {scene}"
    
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt
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