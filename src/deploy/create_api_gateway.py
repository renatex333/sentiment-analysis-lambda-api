import os
import sys
import boto3
import random
import string
import botocore
from dotenv import load_dotenv, set_key, unset_key

def main(api_route: str = "/polarity", update: bool = False):
    """
    Create a new API Gateway to expose the Lambda function

    Args:
    - api_route (str): Route for the API Gateway. Example: "/route". Default is "/polarity".
    - update (str): Whether to update an existing API Gateway. Default is False.
    """
    load_dotenv()

    # Provide function name and ARN copied previously
    lambda_function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
    lambda_function_arn = os.getenv("FUNCTION_ARN")

    api_gateway_name = os.getenv("AWS_API_GATEWAY_NAME")

    api_gateway_client = boto3.client(
        "apigatewayv2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    if update:
        api_gateway_id = os.getenv("API_GATEWAY_ID")
        try:
            api_gateway_client.delete_api(ApiId=api_gateway_id)
            print("API Gateway Deleted!")
            unset_key(".env", "API_GATEWAY_ID")
        except (api_gateway_client.exceptions.NotFoundException, botocore.exceptions.ParamValidationError):
            print(f"No existing API Gateway found with ID '{api_gateway_id}'.")

    api_gateway_create = api_gateway_client.create_api(
        Name=api_gateway_name,
        ProtocolType="HTTP",
        Version="1.0",
        RouteKey=f"POST {api_route}", # Create a /polarity POST route
        Target=lambda_function_arn,
    )

    print("API Endpoint:", api_gateway_create["ApiEndpoint"])
    set_key(".env", "API_GATEWAY_ID", api_gateway_create["ApiId"])
    set_key(".env", "API_GATEWAY_URL", api_gateway_create["ApiEndpoint"] + api_route)

    try:
        id_num = "".join(random.choices(string.digits, k=7))
        api_gateway_permissions = lambda_client.add_permission(
            FunctionName=lambda_function_name,
            StatementId="api-gateway-permission-statement-" + id_num,
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
        )
        print("API Gateway Permissions Created!")
    except Exception as e:
        print(f"Error creating API Gateway permissions: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [api_route] [update]")
        main()
    if len(sys.argv) == 2:
        if sys.argv[1] == "update":
            main(update=True)
        else:
            API_ROUTE = sys.argv[1]
            main(api_route=API_ROUTE)
    if len(sys.argv) == 3:
        API_ROUTE = sys.argv[1]
        main(api_route=API_ROUTE, update=True)
