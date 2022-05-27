from dotenv import load_dotenv
import boto3
import os

load_dotenv()

bucket_name = os.getenv("BUCKET_NAME")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_endpoint = os.getenv("AWS_ENDPOINT")
session = boto3.session.Session()
s3_client = session.client(
    service_name="s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    endpoint_url=aws_endpoint,
)
