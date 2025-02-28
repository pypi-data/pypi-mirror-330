import boto3
import os

def write_file_to_s3(bucket, path, data, mimetype, aws_region = 'ap-southeast-1', public=False):
    aws_access_key_id = os.getenv('NMI_AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('NMI_AWS_SECRET_ACCESS_KEY')
    aws_s3_default_storage_type = 'REDUCED_REDUNDANCY'
    aws_s3_cache_control = 'max-age=300'
    if os.getenv('ENVIRONMENT') == 'production':
        aws_s3_default_storage_type = 'STANDARD'
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=path,
            Body=data,
            ContentType=mimetype,
            StorageClass=aws_s3_default_storage_type,
            CacheControl=aws_s3_cache_control,
            ACL='public-read' if public else 'private'
        )
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise

