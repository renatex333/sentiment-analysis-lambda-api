import os
import io
import json
import boto3
import pytest
import requests
from dotenv import load_dotenv

@pytest.mark.local
def test_lambda():
    load_dotenv()
    # Create a Boto3 client for AWS Lambda
    function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
    )

    payload = response["Payload"]

    response_dict = json.loads(io.BytesIO(payload.read()).read().decode("utf-8"))

    assert "error" in response_dict

@pytest.mark.local
def test_gateway():
    load_dotenv()
    url = os.getenv("API_GATEWAY_URL")

    sentence = "This was the worst movie I watched this year, horrible!"
    body = {"sentence": sentence}

    resp = requests.post(url, json=body)

    assert resp.status_code == 200
    assert "message" in resp.json()
    assert "text" in resp.json()
    assert "polarity" in resp.json()
    assert "sentiment" in resp.json()
    assert resp.json()["sentiment"] == "negative"
