import boto3
from botocore.exceptions import ClientError

class EC2Manager:
    def __init__(self,region="us-east-1"):
        self.client=boto3.client('ec2',region_name=region)

        def launch_instance(self,ami_id,instance_type="t2.micro"):
            try:
                res=self.client.run_instances(
                    ImageId=ami_id,InstanceType=instance_type,MinCount=1,MaxCount=1
                )
                return {"status":"success","instance_id":res['Instances'][0]['InstanceId']}
            except ClientError as e:
                return {"status":"error","message":str(e)}

        def stop_instance(self,instance_id):
            try:
                self.client.stop_instances(InstanceIds=[instance_id])
                return {"status":"success","message":f"Stopping {instance_id}"}
            except ClientError as e:
                return {"status":"error","message":str(e)}