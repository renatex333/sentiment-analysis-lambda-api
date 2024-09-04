import os
import boto3
from dotenv import load_dotenv, set_key

def main():
    load_dotenv()

    layer_name = "layer_polarity_renatex"

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Read the contents of the zip file that you want to deploy
    data_dir = os.path.relpath("data", os.getcwd())
    zip_file = "polarity_layer_package.zip"
    zip_file_path = os.path.join(data_dir, zip_file)
    with open(zip_file_path, "rb") as f:
        zip_to_deploy = f.read()

    lambda_response = lambda_client.publish_layer_version(
        LayerName=layer_name,
        Description="Layer with textblob for polarity",
        Content={"ZipFile": zip_to_deploy},
    )

    print("Layer ARN:\n", lambda_response["LayerArn"])
    print("Layer LayerVersionArn:\n", lambda_response["LayerVersionArn"])
    set_key(".env", "LAYER_VERSION_ARN", lambda_response["LayerVersionArn"])

if __name__ == "__main__":
    main()
