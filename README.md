# Lambda Function for Sentiment Analysis

Welcome to this machine learning project! This project involves creating an AWS Lambda function that uses the `textblob` library to analyze and return the polarity (sentiment) of a given text. To improve functionality and streamline dependency management, Lambda Layers are used.

## Why Use Lambda Layers?

- **Reduce Deployment Package Size:** Instead of packaging function dependencies directly with your Lambda function, you can isolate them into reusable layers. This keeps your deployment packages smaller and more organized.

- **Separate Logic from Dependencies:** Layers allow you to separate the core logic of your function from its dependencies. This enables you to update dependencies without touching the function code, maintaining clean and lightweight deployments.

- **Share Dependencies Across Functions:** By defining reusable layers, multiple functions can share the same dependencies. This eliminates the need to bundle dependencies with every function, simplifying maintenance.

For more details, see the [AWS Lambda Layers documentation](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html).

## Installing Dependencies

To install the required dependencies, use the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Project Structure

- **`data/`**: Contains zipped Lambda function and layer package files.
- **`src/`**: Contains the main source code for deploying and managing the Lambda function, layer, and API Gateway.
- **`tests/`**: Contains unit and integration tests to ensure code stability and functionality.

## Usage

This project employs CI/CD practices, automatically deploying updates to AWS whenever the Lambda function (`polarity.py`) is modified. If you prefer manual deployment, follow the steps below:

### 1. Create ZIP Files

**Create the Lambda function ZIP file:**

```bash
zip data/polarity.zip polarity.py
```

**Create the Lambda layer package:**

On Linux, from the project’s root folder:

```bash
mkdir -p layer/python/lib/python3.12/site-packages
pip3 install textblob -t layer/python/lib/python3.12/site-packages
cd layer
zip -r ../data/polarity_layer_package.zip *
```

### 2. Deployment Pipeline

To manually deploy the project, run the following scripts in order:

1. **Deploy the Lambda function:**
   ```bash
   python src/deploy/create_function.py data/polarity.zip get_polarity [update]
   ```

2. **Deploy the Lambda layer:**
   ```bash
   python src/deploy/create_layer.py data/polarity_layer_package.zip [update]
   ```

3. **Assign the layer to the Lambda function:**
   ```bash
   python src/deploy/assign_layer.py
   ```

4. **Create or update the API Gateway:**
   ```bash
   python src/deploy/create_api_gateway.py [route] [update]
   ```

### 3. Testing

#### Local Testing

To test the function locally, use:

```bash
pytest
```

#### Remote Testing

After deploying the Lambda function and API Gateway, you can verify the setup by running:

```bash
pytest --local
```

The `--local` flag ensures that tests requiring local resources, such as environment variables, are executed.

## References

- [AWS Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS Lambda Layers Documentation](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
