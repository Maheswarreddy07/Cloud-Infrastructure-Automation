import boto3
from botocore.exceptions import ClientError

class IAMManager:
    def __init__(self):
        self.client=boto3.client('iam')

    def create_user(self,username):
        try:
            res=self.client.create_user(UserName=username)
            return {"status":"success","user":res['User']['UserName']}
        except ClientError as e:
            return {"status":"error","message":str(e)}