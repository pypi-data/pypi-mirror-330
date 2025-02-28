import boto3
import os

def get_s3_file(bucket_name, file_path, region_name):
    aws_access_key_id = os.getenv('AWS_S3_ACCOUNT_ID')
    aws_secret_access_key = os.getenv('AWS_S3_ACCOUNT_SECRET')

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_path)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching file from S3: {e}")
        return None
