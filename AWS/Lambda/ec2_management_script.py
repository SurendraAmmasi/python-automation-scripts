import boto3
import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(Filters=[{'Name': 'tag:AutoStartStop', 'Values': ['true']}])
    instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]
    
    current_hour = datetime.datetime.now().hour
    if 9 <= current_hour < 17:  # Example: Start instances between 9 AM to 5 PM
        ec2.start_instances(InstanceIds=instance_ids)
    else:
        ec2.stop_instances(InstanceIds=instance_ids)
