import json
import pytest
import polarity
from textblob import TextBlob


def test_simple_sentence_polarity():
    """Tests the polarity function with a simple sentence"""
    sentence = "This was the worst movie I watched this year, horrible!"
    event = {"body": json.dumps({
        "sentence": sentence
        })
    }

    blob = TextBlob(sentence)
    sentiment = "positive" if blob.polarity > 0.2 else "negative" if blob.polarity < -0.8 else "neutral"
    
    expected = {
        "message": "Sentiment analysis lambda function",
        "text": sentence,
        "polarity": str(blob.polarity),
        "sentiment": sentiment
    }

    # Test if return is as expected
    assert polarity.get_polarity(event, None) == expected

def test_no_body_in_request():
    """Tests the polarity function with no body in the request"""
    event = {}

    expected = {
        "error": "No body in the request"
    }

    # Test if return is as expected
    assert polarity.get_polarity(event, None) == expected
