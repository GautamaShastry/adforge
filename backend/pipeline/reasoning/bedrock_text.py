import boto3
import json

bedrock = boto3.client("bedrock-runtime")
MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

def handler(event, context):
    labels = event.get("labels", [])
    
    prompt = f"""You are a senior advertising creative director.

Product attributes:
{", ".join(labels)}

Write a 60-second ad script and a scene description.
Return STRICT JSON only, no markdown:
{{"script": "...", "scene": "..."}}"""
    
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0.7
        })
    )
    
    body = json.loads(response["body"].read())
    raw_text = body["content"][0]["text"]
    
    # Handle potential markdown code blocks in response
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
    raw_text = raw_text.strip()
    
    content = json.loads(raw_text)
    
    event["script"] = content["script"]
    event["scene"] = content["scene"]
    return event