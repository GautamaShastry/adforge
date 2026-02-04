import boto3

rekognition = boto3.client("rekognition")

def handler(event, context):
    response = rekognition.detect_labels(
        Image={
            "S3Object": {
                "Bucket": event["bucket"],
                "Name": event["key"]
            }
        },
        MaxLabels=10
    )
    
    labels = [
        l["Name"]
        for l in response["Labels"]
        if l["Confidence"] >= 80
    ]
    
    event["labels"] = labels
    return event