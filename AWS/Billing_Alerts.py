import boto3
import json
import os

sns = boto3.client('sns')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    # Define the budget threshold
    budget_threshold = 100  # Example threshold in USD
    
    # Get the current month's estimated charges
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions=[{'Name': 'Currency', 'Value': 'USD'}],
        StartTime=datetime.datetime.utcnow().replace(day=1),
        EndTime=datetime.datetime.utcnow(),
        Period=86400,
        Statistics=['Maximum']
    )
    
    estimated_charges = response['Datapoints'][0]['Maximum']
    
    if estimated_charges > budget_threshold:
        alert_message = f"AWS spending alert: Your estimated charges for this month have exceeded ${budget_threshold}. Current charges: ${estimated_charges:.2f}"
        
        # Send alert via SNS
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Subject='AWS Spending Alert',
            Message=alert_message
        )
        
        return alert_message
    
    return 'No alert. Charges within threshold.'

"""
Explanation:

Imports and Initialization: The script imports necessary libraries (boto3 for AWS SDK) and initializes clients (sns for SNS - Simple Notification Service and cloudwatch for CloudWatch).

Billing Threshold: budget_threshold is set to $100 (adjust as needed) as the maximum allowed monthly AWS spending.

CloudWatch Metrics: Using get_metric_statistics() from CloudWatch, the script retrieves the maximum estimated charges (EstimatedCharges) for the current month (StartTime to EndTime).

Alert Condition: If the estimated_charges exceed budget_threshold, an alert message is generated.

Sending Alerts: The alert message is sent via SNS (sns.publish()), using the specified SNS topic ARN (os.environ['SNS_TOPIC_ARN']).

Return Statement: Depending on whether an alert was triggered or not, the function returns an appropriate message indicating the status of AWS spending relative to the threshold.


"""