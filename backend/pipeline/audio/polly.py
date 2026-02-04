import boto3

polly = boto3.client("polly")
s3 = boto3.client("s3")

OUTPUT_BUCKET = "adforge-output-bucket"

def handler(event, context):
    audio = polly.synthesize_speech(
        Text=event["script"],
        VoiceId="Matthew",
        OutputFormat="mp3",
        Engine="neural"
    )
    
    job_id = event["jobId"]
    key = f"{job_id}/audio.mp3"
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=key,
        Body=audio["AudioStream"].read(),
        ContentType="audio/mpeg"
    )
    
    event["audio"] = key
    return event