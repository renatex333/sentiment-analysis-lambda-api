import os
import sys
import boto3
import botocore
from dotenv import load_dotenv, set_key, unset_key

def main(zip_file_path: str, update: bool = False):
    """
    Create a new Lambda Layer using the provided ZIP file

    Args:
    - zip_file_path (str): Path to the ZIP file containing the Lambda Layer code. Example: "data/FILENAME.zip".
    - update (bool): Whether to update an existing Lambda Layer. Default is False.
    """
    load_dotenv()

    layer_name = os.getenv("AWS_LAYER_NAME")

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

    # Create a new Lambda Layer
    if update:
        try:
            lambda_client.delete_layer_version(
                LayerName=layer_name, VersionNumber=os.getenv("LAYER_VERSION")
            )
            print("Existing Layer was Deleted!")
            unset_key(".env", "LAYER_VERSION_ARN")
            unset_key(".env", "LAYER_VERSION")
        except (lambda_client.exceptions.ResourceNotFoundException, botocore.exceptions.ParamValidationError):
            print("No existing layer found.")

    lambda_response = lambda_client.publish_layer_version(
        LayerName=layer_name,
        Description="Layer with textblob for polarity",
        Content={"ZipFile": zip_to_deploy},
    )

    print("Layer ARN:\n", lambda_response["LayerArn"])
    print("Layer LayerVersionArn:\n", lambda_response["LayerVersionArn"])
    print("Layer Version:\n", lambda_response["Version"])
    set_key(".env", "LAYER_VERSION_ARN", lambda_response["LayerVersionArn"])
    set_key(".env", "LAYER_VERSION", str(lambda_response["Version"]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path to zip package file> [update]")
        sys.exit(1)
    ZIP_FILE = sys.argv[1]
    if len(sys.argv) == 3 and sys.argv[-1] == "update":
        print("Updating existing resources...")
        main(zip_file_path=ZIP_FILE, update=True)
    else:
        main(zip_file_path=ZIP_FILE)
