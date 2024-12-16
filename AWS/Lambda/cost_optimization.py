import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    cloudwatch = boto3.client('cloudwatch')
    
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance['InstanceId']}],
                StartTime=datetime.utcnow() - timedelta(days=7),
                EndTime=datetime.utcnow(),
                Period=3600,
                Statistics=['Average']
            )
            avg_cpu = sum([point['Average'] for point in metrics['Datapoints']]) / len(metrics['Datapoints'])
            if avg_cpu < 10:  # Example threshold
                # Notify or take action on underutilized instance
                print(f"Instance {instance['InstanceId']} is underutilized with avg CPU: {avg_cpu}%")
