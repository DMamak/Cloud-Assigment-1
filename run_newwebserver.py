#!/usr/bin/env python3
import setupweb
import set_up_bucket
import general_functions
import time
import os

#Asks User for the name of their Private Key to connect to his aws

key_name = input("Please Input the Name of your key.pem file (excluding the pem extension): -> ")
key_location = general_functions.find_key_location(key_name)
while general_functions.is_Blank(key_location):
    new_name = input("Key Not found Please enter correct Name !: -> ")
    key_location = general_functions.find_key_location(new_name)

key_name = os.path.basename(key_location)
general_functions.change_key_permissions(key_location)
instance_id = setupweb.create_web_server(key_name)
setupweb.check_status(instance_id)

#Ask the user for the name of the bucket and create it
bucket_name = input("Please Enter the name of the bucket you want to create in lowercase: -> ")
bucket_name = set_up_bucket.create_bucket(bucket_name)

#Upload a image to the bucket
set_up_bucket.upload_existing_img(bucket_name)
instance_dns = setupweb.get_instance_dns(instance_id)

#wait for ports to be enabled on instance
print("waiting for ports to be enabled on instance")
time.sleep(60)
general_functions.ssh_commands(key_location, instance_dns, " sudo yum install python3 -y")
general_functions.scp_commands(key_location, instance_dns)
general_functions.ssh_commands(key_location, instance_dns, " python3 /tmp/check_webserver.py")
general_functions.create_new_home_page(bucket_name, key_location, instance_dns)
general_functions.copy_memory_script(key_location, instance_dns)






# print(ec2.get_all_instance_status(instance_ids=" + (createwebserver())))

