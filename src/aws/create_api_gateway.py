import os
import boto3
import random
import string
from dotenv import load_dotenv, set_key

def main():
    load_dotenv()

    # Provide function name and ARN copied previously
    lambda_function_name = "get_polarity_renatex"
    lambda_arn = os.getenv("LAMBDA_ARN")

    api_gateway_name = "demo_polarity_renatex"

    id_num = "".join(random.choices(string.digits, k=7))

    api_gateway = boto3.client(
        "apigatewayv2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    lambda_function = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    lambda_function_get = lambda_function.get_function(FunctionName=lambda_function_name)

    print(lambda_function_get)

    api_route = "/polarity"
    api_gateway_create = api_gateway.create_api(
        Name=api_gateway_name,
        ProtocolType="HTTP",
        Version="1.0",
        RouteKey=f"POST {api_route}", # Create a /polarity POST route
        Target=lambda_function_get["Configuration"]["FunctionArn"],
    )

    api_gateway_permissions = lambda_function.add_permission(
        FunctionName=lambda_function_name,
        StatementId="api-gateway-permission-statement-" + id_num,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
    )

    print("API Endpoint:", api_gateway_create["ApiEndpoint"])
    set_key(".env", "API_GATEWAY_ID", api_gateway_create["ApiId"])
    set_key(".env", "API_GATEWAY_URL", api_gateway_create["ApiEndpoint"] + api_route)

if __name__ == "__main__":
    main()