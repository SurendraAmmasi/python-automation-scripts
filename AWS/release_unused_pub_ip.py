import boto3


def remove_unused_public_ips():
    # Initialize boto3 client for EC2
    ec2_client = boto3.client('ec2')

    # Describe all Elastic IP addresses
    response = ec2_client.describe_addresses()

    # Iterate through each Elastic IP address
    for address in response['Addresses']:
        # Check if the Elastic IP is associated with an instance
        if 'InstanceId' not in address:
            # Disassociate and release the Elastic IP
            allocation_id = address['AllocationId']
            ec2_client.release_address(AllocationId=allocation_id)
            print(f"Released Elastic IP: {address['PublicIp']}")


if __name__ == "__main__":
    remove_unused_public_ips()
