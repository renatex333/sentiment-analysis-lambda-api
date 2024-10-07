"""
Module to contain the polarity function for the sentiment analysis lambda function
"""

import json
from textblob import TextBlob

def get_polarity(event, context):
    """
    Handler function for the sentiment analysis lambda function.
    Receives a sentence in the request body and returns the polarity and sentiment of the sentence.
    """
    if "body" not in event:
        return {
            "error": "No body in the request"
        }

    body = json.loads(event["body"])

    if "sentence" not in body:
        return {
            "error": "No sentence in the request body"
        }

    received_text = body["sentence"]

    blob = TextBlob(received_text)

    sentiment = "positive" if blob.polarity > 0.2 else "negative" if blob.polarity < -0.8 else "neutral"

    return {
        "message": "Sentiment analysis lambda function",
        "text": received_text,
        "polarity": str(blob.polarity),
        "sentiment": sentiment
    }
