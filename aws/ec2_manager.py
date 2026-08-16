import os
import boto3
from botocore.exceptions import ClientError

class EC2Manager:
    def __init__(self):
        # 1. Fetch values from Render environment variables if live, or default back to local setup
        aws_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

        # 2. Instantiate the client using explicit parameters or fallback environment discovery
        if aws_id and aws_secret:
            self.client = boto3.client(
                'ec2',
                aws_access_key_id=aws_id,
                aws_secret_access_key=aws_secret,
                region_name=self.region
            )
        else:
            # Fallback for your local machine's C:\Users\...\.aws\credentials file
            session = boto3.session.Session()
            self.region = session.region_name or "us-east-1"
            self.client = boto3.client('ec2', region_name=self.region)

    def launch_instance(self, ami_id, instance_type="t3.micro"):
        try:
            # Strip standard whitespaces and replace common web non-breaking spaces
            clean_ami = ami_id.replace('\u00a0', '').strip()
            
            # Ultra-clean: Keep ONLY letters, numbers, and hyphens (deletes hidden characters)
            clean_ami = "".join(ch for ch in clean_ami if ch.isalnum() or ch == '-')
            
            response = self.client.run_instances(
                ImageId=clean_ami,
                InstanceType=instance_type,
                MinCount=1,
                MaxCount=1
            )
            instance_id = response['Instances'][0]['InstanceId']
            return {"status": "success", "instance_id": instance_id}
        except ClientError as e:
            return {"status": "error", "message": str(e)}

    def stop_instance(self, instance_id):
        try:
            # Clean the user string input
            clean_id = instance_id.strip()
            self.client.stop_instances(InstanceIds=[clean_id])
            return {"status": "success", "message": f"Stopping instance {clean_id}."}
        except ClientError as e:
            return {"status": "error", "message": str(e)}
