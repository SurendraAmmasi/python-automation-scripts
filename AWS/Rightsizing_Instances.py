import boto3
import datetime

# Initialize clients
cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # List all EC2 instances
    instances = ec2.describe_instances()
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            
            # Get CPU utilization for the past week
            cpu_stats = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=7),
                EndTime=datetime.datetime.utcnow(),
                Period=3600,
                Statistics=['Average']
            )
            
            avg_cpu = sum(data['Average'] for data in cpu_stats['Datapoints']) / len(cpu_stats['Datapoints'])
            
            if avg_cpu < 10:
                print(f"Instance {instance_id} ({instance_type}) has low CPU utilization: {avg_cpu}%")
                # Suggest resizing down
            elif avg_cpu > 70:
                print(f"Instance {instance_id} ({instance_type}) has high CPU utilization: {avg_cpu}%")
                # Suggest resizing up
                
    return 'Cost optimization suggestions completed.'

"""
Explanation:

Imports and Initialization: The script imports necessary libraries (boto3 for AWS SDK) and initializes clients (cloudwatch for CloudWatch metrics and ec2 for EC2 instances).

Describe Instances: describe_instances() retrieves details about all EC2 instances in your AWS account.

CPU Utilization Metrics: Using get_metric_statistics() from CloudWatch, the script fetches CPU utilization metrics (CPUUtilization) for each instance over the past 7 days (StartTime to EndTime).

Average CPU Utilization: It calculates the average CPU utilization over the specified period (Period=3600 seconds, or 1 hour).

Rightsizing Logic: Based on the average CPU utilization (avg_cpu), the script prints messages indicating whether the instance has low or high CPU utilization. It's typical to implement additional logic here to modify the instance type (instance['InstanceType']) using the ec2.modify_instance_attribute() method or by launching new instances with the desired type.

Return Statement: The function concludes by returning a message indicating that cost optimization suggestions have been completed.
"""

