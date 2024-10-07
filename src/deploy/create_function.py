import os
import sys
import boto3
import botocore
from dotenv import load_dotenv, set_key, unset_key

def main(zip_file_path: str, handler: str, update: bool = False):
    """
    Create a new Lambda function using the provided ZIP file

    Args:
    - zip_file_path (str): Path to the ZIP file containing the Lambda function code. Example: "data/FILENAME.zip".
    - handler (str): Handler function for the Lambda function. Example: "FILENAME.FUNCTION_NAME".
    - update (bool): Whether to update an existing Lambda function. Default is False.
    """
    load_dotenv()

    # Lambda function name
    function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")

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
    with open(zip_file_path, "rb") as f:
        zip_to_deploy = f.read()

    # Create a new Lambda function
    if update:
        try:
            lambda_client.delete_function(FunctionName=function_name)
            print("Existing Function was Deleted!")
            unset_key(".env", "FUNCTION_ARN")
        except (lambda_client.exceptions.ResourceNotFoundException, botocore.exceptions.ParamValidationError):
            print("No existing function found.")

    lambda_response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime="python3.10",
        Role=lambda_role_arn,
        Handler=handler,
        Code={"ZipFile": zip_to_deploy},
    )

    print("Function ARN:", lambda_response["FunctionArn"])
    set_key(".env", "FUNCTION_ARN", lambda_response["FunctionArn"])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <path to zip file> <handler> [update]")
        sys.exit(1)
    ZIP_FILE = sys.argv[1]
    HANDLER = ZIP_FILE.split("/")[-1].replace(".zip", f".{sys.argv[2]}")
    if len(sys.argv) == 4 and sys.argv[-1] == "update":
        print("Updating existing resources...")
        main(zip_file_path=ZIP_FILE, handler=HANDLER, update=True)
    else:
        main(zip_file_path=ZIP_FILE, handler=HANDLER)
