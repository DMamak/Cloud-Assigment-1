
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


def create_web_server(name):
    # This Method Takes in users .pem key and creates a new instance of server on the aws.
    print("Creating new web server")
    user_data_script = """#!/bin/bash
    echo "Updating yum" >> /tmp/server_log.txt
    sudo yum update -y
    echo "Installing Apache" >> /tmp/server_log.txt
    sudo yum install httpd -y
    sudo systemctl enable httpd
    """

    instance = ec2.create_instances(
        ImageId='ami-0bdb1d6c15a40392c',
        InstanceType='t2.micro',
        KeyName=name[:-5],
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[check_security_group()],
        UserData=user_data_script
    )
    instance_id = instance[0].instance_id
    print("Created a new Web Server with ID : " + instance_id)
    return instance_id


def check_security_group():
    #This Method checks if SSH Security Group Exists otherwise it Creates a new Security Group
    print("Checking if Security Group Exists")
    try:
        response = client.describe_security_groups(
            GroupNames=[
                'sshSecurity',
            ],
        )
        print("Security Group Already Exists")
        print("Check SSH Inbound Rule")
        check_rule(response['SecurityGroups'][0]['GroupId'])
        return response['SecurityGroups'][0]['GroupId']
    except ClientError as e:
        print("Security Group Doesn't Exists")
        print("Creating a security group")
        response = ec2.create_security_group(
            Description='custom security group to ssh into webserver',
            GroupName='sshSecurity',
        )
        print("Created security group with id " + response.id)
        check_rule(response.id)
        return response.id


def check_rule(groupid):
    #This Method checks if a security group has proper inbound rules set if not it creates them.
    try:
        print("SSH Inbound Rule Doesnt Exist")
        data = client.authorize_security_group_ingress(
            GroupId=groupid,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print("Rule Created")
    except ClientError as e:
        print("Inbound Rule Exists")


def check_status(instance_id):
    print("Waiting for Server to be Running!")
    waiter = client.get_waiter('instance_running')
    waiter.wait(
        InstanceIds=[
            instance_id,
        ]
    )
    print("status up")


def get_instance_dns(instance_id):
    print("Getting DNS")
    running_instances = ec2.instances.filter(Filters=[{
        'Name': 'instance-id',
        'Values': [instance_id]}])
    for instance in running_instances:
        instance_dns = instance.public_dns_name
        return instance_dns