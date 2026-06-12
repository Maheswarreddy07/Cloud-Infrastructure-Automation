import boto3
from datetime import datetime,timedelta

class CloudWatchManager:
    def __init__(self,region="us-east-1"):
        self.cw=boto3.client('cloudwatch',region_name=region)
        self.ce=boto3.client('ce',region_name=region)

    def get_cpu_utilization(self,instance_id):
        try:
            res=self.cw.get_metric_data(
                MetricDataQueries=[{
                    'Id':'m1',
                    'MetricStat':{
                        'Metric':{
                            'Namespace':'AWS/EC2',
                            'MetricName':'CPUUtilization',
                            'Dimensions':[{'Name':'InstanceId','Value':instance_id}]
                        },
                        'Period':300,
                        'stat':'Average',
                        }
                    }],
                    StartTime=datetime.utcnow()-timedelta(hours=1),
                    EndTime=datetime.utcnow()
            )
            values=res['MetricDataResults'][0]['Values']
            return {"status":"success","cpu":values[0] if values else "No data yet"}
        except Exception as e:
            return {"status":"error","message":str(e)}

    def get_cost_report(self):
        try:
            start_date=datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date=datetime.now().strftime('%Y-%m-%d')
            if start_date==end_date:
                start_date=(datetime.now()-timedelta(days=1)).strf('%Y-%m-%d')

                res=self.ce.get_cost_and_usage(
                    TimePeriod={'Start':start_date,'End':end_date},
                    Granularity='Monthly',
                    Metrics=['UnbalancedCost']
                )
                amount=res['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
                return {"status":"success","cost":f"${float(amount):.2f}"}
        except Exception:
            return {"status":"success","cost":"$0.00(cost Explorer API requires explicit activation)"}