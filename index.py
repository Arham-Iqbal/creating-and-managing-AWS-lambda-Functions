import boto3
import zipfile
import os

# Initialize a session using Boto3
lambda_client = boto3.client('lambda', region_name='your-region')

# Create a zip file of the Lambda function code
with zipfile.ZipFile('/tmp/lambda_function.zip', 'w') as lambda_zip:
    lambda_zip.write('lambda_function.py')

# Define the Lambda function code and configuration
with open('/tmp/lambda_function.zip', 'rb') as f:
    zip_content = f.read()

response = lambda_client.create_function(
    FunctionName='MyLambdaFunction',
    Runtime='python3.8',
    Role='arn:aws:iam::your-account-id:role/your-lambda-role',
    Handler='lambda_function.lambda_handler',
    Code=dict(ZipFile=zip_content),
    Timeout=10,
    MemorySize=128,
    Publish=True
)

print(f"Created Lambda Function: {response['FunctionArn']}")

response = lambda_client.invoke(
    FunctionName='MyLambdaFunction',
    InvocationType='RequestResponse',
    LogType='Tail'
)

print("Function output:", response['Payload'].read().decode('utf-8'))

# Publish a new version of the Lambda function
response = lambda_client.publish_version(
    FunctionName='MyLambdaFunction',
    Description='Version 1'
)
print(f"Published Version: {response['Version']}")

# Create an alias for the new version
response = lambda_client.create_alias(
    FunctionName='MyLambdaFunction',
    Name='prod',
    FunctionVersion=response['Version']
)
print(f"Created Alias: {response['AliasArn']}")
