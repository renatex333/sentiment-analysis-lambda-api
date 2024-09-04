import boto3
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Provide layer name
    layer_name = "layer_polarity_renatex"

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Fetch the layer version ARN based on the layer name
    response = lambda_client.list_layer_versions(
        CompatibleRuntime="python3.10",  # Provide the compatible runtime of the layer
        LayerName=layer_name,
    )

    if "LayerVersions" in response:
        layer_versions = response["LayerVersions"]

        # Delete each layer version
        for version in layer_versions:
            lambda_client.delete_layer_version(
                LayerName=layer_name, VersionNumber=version["Version"]
            )

        print(f"Deleted all versions of layer '{layer_name}'.")
    else:
        print(f"No layer with the name '{layer_name}' found.")

if __name__ == "__main__":
    main()
