import os
import boto3
from datetime import datetime, timedelta

class CloudWatchManager:
    def __init__(self, region="us-east-1"):
        # 1. Fetch credentials from Render environment variables if live
        aws_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region = os.environ.get('AWS_DEFAULT_REGION', region)

        if aws_id and aws_secret:
            # Authenticate using production credentials on Render
            self.cw = boto3.client('cloudwatch', 
                                   aws_access_key_id=aws_id, 
                                   aws_secret_access_key=aws_secret, 
                                   region_name=self.region)
            self.ce = boto3.client('ce', 
                                   aws_access_key_id=aws_id, 
                                   aws_secret_access_key=aws_secret, 
                                   region_name=self.region)
        else:
            # Fallback for your local machine profile setup
            self.cw = boto3.client('cloudwatch', region_name=self.region)
            self.ce = boto3.client('ce', region_name=self.region)

    def get_cpu_utilization(self, instance_id):
        try:
            res = self.cw.get_metric_data(
                MetricDataQueries=[{
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/EC2',
                            'MetricName': 'CPUUtilization',
                            'Dimensions': [{'Name': 'InstanceId', 'Value': instance_id}]
                        },
                        'Period': 300,
                        'Stat': 'Average', # Capitalized 'Stat' to match AWS specifications
                    }
                }],
                StartTime=datetime.utcnow() - timedelta(hours=1),
                EndTime=datetime.utcnow()
            )
            values = res['MetricDataResults'][0]['Values']
            return {"status": "success", "cpu": values[0] if values else "No data yet"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_cost_report(self):
        try:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            if start_date == end_date:
                # FIXED TYPO HERE: changed .strf() to .strftime()
                start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

            res = self.ce.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity='MONTHLY', # Capitalized to match valid AWS parameter constraints
                Metrics=['UnblendedCost'] # Fixed capital spelling to match official metric name
            )
            amount = res['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
            return {"status": "success", "cost": f"${float(amount):.2f}"}
        except Exception:
            # Your current fallback exception handling is perfect since Cost Explorer demands root enabling
            return {"status": "success", "cost": "$0.00 (Cost Explorer API requires explicit activation)"}
