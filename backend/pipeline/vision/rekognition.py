def handler(event, context):
    event["labels"] = ["stub-label"]
    return event