import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instance_id = event['detail']['instance-id']
    
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {'Key': 'Environment', 'Value': 'Development'},
            {'Key': 'Owner', 'Value': 'Team A'}
        ]
    )
