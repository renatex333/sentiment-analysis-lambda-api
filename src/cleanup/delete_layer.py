import os
import boto3
from dotenv import load_dotenv, unset_key

def main():
    load_dotenv()

    # Provide layer name
    layer_name = os.getenv("AWS_LAYER_NAME")

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Fetch the layer version ARN based on the layer name
    response = lambda_client.list_layer_versions(
        LayerName=layer_name,
    )

    if "LayerVersions" in response:
        layer_versions = response["LayerVersions"]

        # Delete each layer version
        for version in layer_versions:
            try:
                lambda_client.delete_layer_version(
                    LayerName=layer_name, VersionNumber=version["Version"]
                )
            except lambda_client.exceptions.ResourceNotFoundException:
                print("No existing layer found.")

        print(f"Deleted all versions of layer '{layer_name}'.")
    else:
        print(f"No layer with the name '{layer_name}' found.")

    unset_key(".env", "LAYER_VERSION_ARN")
    unset_key(".env", "LAYER_VERSION")

if __name__ == "__main__":
    main()
