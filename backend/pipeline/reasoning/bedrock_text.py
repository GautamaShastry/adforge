import boto3
import json

bedrock = boto3.client("bedrock-runtime")
MODEL_ID = "amazon.nova-lite-v1:0"

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
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {
                "maxTokens": 800,
                "temperature": 0.7
            }
        })
    )
    
    body = json.loads(response["body"].read())
    raw_text = body["output"]["message"]["content"][0]["text"]
    
    # Handle potential markdown code blocks in response
    if "```" in raw_text:
        parts = raw_text.split("```")
        for part in parts:
            if part.startswith("json"):
                raw_text = part[4:]
                break
            elif part.strip().startswith("{"):
                raw_text = part
                break
    raw_text = raw_text.strip()
    
    # Try to extract JSON from the response
    try:
        content = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        content = {
            "script": raw_text[:500] if len(raw_text) > 500 else raw_text,
            "scene": "Product showcase with professional lighting"
        }
    
    event["script"] = content.get("script", "")
    event["scene"] = content.get("scene", "Product showcase")
    return event