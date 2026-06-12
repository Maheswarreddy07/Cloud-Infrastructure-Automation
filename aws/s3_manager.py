import boto3
import os
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self):
        # Automatically read the region you typed during 'aws configure'
        session = boto3.session.Session()
        self.region = session.region_name or "us-east-1"
        self.client = boto3.client('s3', region_name=self.region)

    def create_bucket(self, bucket_name):
        try:
            # AWS Rule: us-east-1 breaks if LocationConstraint is provided
            if self.region == 'us-east-1':
                self.client.create_bucket(Bucket=bucket_name)
            else:
                self.client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            return {"status": "success", "message": f"Bucket '{bucket_name}' created successfully in {self.region}."}
        except ClientError as e:
            return {"status": "error", "message": str(e)}

    def upload_file(self, bucket_name, file_path):
        try:
            filename = os.path.basename(file_path)
            self.client.upload_file(file_path, bucket_name, filename)
            return {"status": "success", "message": f"Uploaded {filename} to {bucket_name}."}
        except ClientError as e:
            return {"status": "error", "message": str(e)}