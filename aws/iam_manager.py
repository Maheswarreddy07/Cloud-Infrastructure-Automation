import os
import boto3
from botocore.exceptions import ClientError

class IAMManager:
    def __init__(self):
        # 1. Fetch values from Render environment variables if live
        aws_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

        # 2. Instantiate the client using explicit parameters or fallback environment discovery
        if aws_id and aws_secret:
            # Authenticate using production credentials on Render
            self.client = boto3.client(
                'iam',
                aws_access_key_id=aws_id,
                aws_secret_access_key=aws_secret,
                region_name=self.region
            )
        else:
            # Fallback for your local machine's C:\Users\...\.aws\credentials file
            self.client = boto3.client('iam')

    def create_user(self, username):
        try:
            # Clean up trailing spaces or accidental weird formatting from the front-end input
            clean_username = username.strip()
            
            res = self.client.create_user(UserName=clean_username)
            return {"status": "success", "user": res['User']['UserName']}
        except ClientError as e:
            return {"status": "error", "message": str(e)}
