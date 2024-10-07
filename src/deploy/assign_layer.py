import os
import boto3
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Provide ARN and function name
    layer_version_arn = (
        os.getenv("LAYER_VERSION_ARN")
    )

    function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Get the current configuration of the Lambda function
    response = lambda_client.get_function(FunctionName=function_name)

    # Retrieve the existing layers
    layers = (
        response["Configuration"]["Layers"] if "Layers" in response["Configuration"] else []
    )

    if layers:
        print("Existing layers:")
        for layer in layers:
            print(layer)
    else:
        print("No existing layers found.")

    # Append the layer ARN to the existing layers
    layers.append(layer_version_arn)

    # Update the function configuration with the new layers
    try:
        lambda_response = lambda_client.update_function_configuration(
            FunctionName=function_name, Layers=layers
        )
        print("Updated function configuration successfully.")
    except (lambda_client.exceptions.ResourceNotFoundException, lambda_client.exceptions.InvalidParameterValueException, Exception) as e:
        print(f"Error updating function configuration: {e}")

if __name__ == "__main__":
    main()
