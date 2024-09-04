# Lambda Function for Sentment Analysis

Welcome to this ML project!

This project involves creating an AWS Lambda function that utilizes the `textblob` library to analyze and return the polarity of a given text. To enhance the project's functionality and manage dependencies more efficiently, Lambda Layers will be utilized.

The main advantages of using Lambda layers are:

- **Reduce the size of deployment packages:** Rather than packaging function dependencies directly with your function code, you can isolate dependencies into reusable layers. This keeps deployment packages small and organized.

- **Separate core function logic from dependencies:** Using layers allows function logic and dependencies to evolve separately. Layers facilitate independent management, where dependencies can be revised without touching the function code. This allows deployment packages for your functions to focus solely on application logic without the bloat of bundled dependencies.

- **Share dependencies across multiple functions:** By building dependencies into layers, those components can then be associated with multiple functions simultaneously. Layers are reusable, so once a layer is established, any function configuration can reference and inherit its dependencies, rather than requiring redundant inclusion in each deployment package.

For more information on Lambda layers, refer to the official AWS documentation: [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html). 

## Installing Dependencies

To install the project dependencies, use the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Project Structure

- `data`: Contains the data used by the model.
- `models`: Contains the machine learning models and encoders.
- `notebooks`: Contains the notebooks used for data exploration and visualization.
- `src`: Contains the main source code to collect and process data, train models and make predictions.
- `tests`: Contains unit and integration tests to guarantee code stability.

## Usage

### Configure your AWS CLI

Having [AWS CLI installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), configure your credentials on a profile:
```bash
aws configure --profile mlops
```

To set it as deafult profile:

Linux:
```bash
export AWS_PROFILE=mlops
```

Windows CMD:
```bash
set AWS_PROFILE=mlops
```

Windows PowerShell:
```bash
env:AWS_PROFILE = "mlops"
```

### Scripts pipeline

To set up the project, run the following scripts in order:

```bash
python src/create_function.py
python src/create_layer.py
python src/assign_layer.py
python src/create_api_gateway.py
```

### Test deployed instances

To test the deployed instances, run the following command:

```bash
python tests/test.py
```

# References

[Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)