import os
import io
import json
import boto3
import requests
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Lambda function name
    function_name = "get_polarity_renatex"

    # Lambda basic execution role
    test_lambda(function_name)
    # Gateway basic response
    test_gateway()

def test_lambda(function_name: str):
    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    try:
        # Invoke the function
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
        )

        payload = response["Payload"]

        response_dict = json.loads(io.BytesIO(payload.read()).read().decode("utf-8"))
        print(f"Response:\n{response_dict}")
        assert "error" in response_dict # The function should return an error, because the event does not have a body

    except Exception as e:
        print(e)

def test_gateway():
    
    url = os.getenv("API_GATEWAY_URL")

    body = {"sentence": "This was the worst movie I watched this year, horrible!"}

    resp = requests.post(url, json=body)

    print(f"status code: {resp.status_code}")
    print(f"text: {resp.text}")


if __name__ == "__main__":
    main()
