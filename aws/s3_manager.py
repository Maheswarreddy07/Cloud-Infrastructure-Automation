import os
import boto3
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self):
        # 1. Fetch values from Render environment variables if live
        aws_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

        # 2. Instantiate the client using explicit parameters or fallback environment discovery
        if aws_id and aws_secret:
            # Authenticate using production credentials on Render
            self.client = boto3.client(
                's3',
                aws_access_key_id=aws_id,
                aws_secret_access_key=aws_secret,
                region_name=self.region
            )
        else:
            # Fallback for your local machine's C:\Users\...\.aws\credentials file
            session = boto3.session.Session()
            self.region = session.region_name or "us-east-1"
            self.client = boto3.client('s3', region_name=self.region)

    def create_bucket(self, bucket_name):
        try:
            # Clean up trailing spaces or accidental capital letters from the front-end input
            clean_bucket_name = bucket_name.strip().lower()

            # AWS Rule: us-east-1 breaks if LocationConstraint is provided
            if self.region == 'us-east-1':
                self.client.create_bucket(Bucket=clean_bucket_name)
            else:
                self.client.create_bucket(
                    Bucket=clean_bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            return {"status": "success", "message": f"Bucket '{clean_bucket_name}' created successfully in {self.region}."}
        except ClientError as e:
            return {"status": "error", "message": str(e)}

    def upload_file(self, bucket_name, file_path):
        try:
            filename = os.path.basename(file_path)
            self.client.upload_file(file_path, bucket_name, filename)
            return {"status": "success", "message": f"Uploaded {filename} to {bucket_name}."}
        except ClientError as e:
            return {"status": "error", "message": str(e)}
