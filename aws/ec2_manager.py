import boto3
from botocore.exceptions import ClientError

class EC2Manager:
    def __init__(self):
        # Automatically inherit the configuration region from your local system profile
        session = boto3.session.Session()
        self.region = session.region_name or "us-east-1"
        self.client = boto3.client('ec2', region_name=self.region)

    def launch_instance(self, ami_id, instance_type="t3.micro"):
        try:
            # 1. Strip standard whitespaces and replace common web non-breaking spaces
            clean_ami = ami_id.replace('\u00a0', '').strip()
            
            # 2. Ultra-clean: Keep ONLY letters, numbers, and hyphens (deletes hidden characters)
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