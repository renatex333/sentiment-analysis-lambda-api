import os
import boto3
from dotenv import load_dotenv, set_key

def main():
    load_dotenv()

    # Lambda function name
    function_name = "get_polarity_renatex"

    # Lambda basic execution role
    lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN")

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Read the contents of the zip file that you want to deploy
    data_dir = os.path.relpath("data", os.getcwd())
    zip_file = "polarity.zip"
    handler = "polarity.get_polarity" # function get_polarity inside polarity.py
    zip_file_path = os.path.join(data_dir, zip_file)
    with open(zip_file_path, "rb") as f:
        zip_to_deploy = f.read()

    lambda_response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime="python3.10", # Change the runtime if you want!
        Role=lambda_role_arn,
        Handler=handler,
        Code={"ZipFile": zip_to_deploy},
    )

    print("Function ARN:", lambda_response["FunctionArn"])
    set_key(".env", "LAMBDA_ARN", lambda_response["FunctionArn"])


if __name__ == "__main__":
    main()
