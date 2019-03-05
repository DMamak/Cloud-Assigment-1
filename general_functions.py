import subprocess
import webbrowser
from subprocess import *


def find_key_location(key_name):
    full_key_name = key_name + '.pem'
    print("Finding key location")
    commands = '''
    cd ~
    ''' + '''find ~ -iname ''' + full_key_name
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands.encode('utf-8'))
    key_location = out.decode('utf-8')
    return key_location


def is_Blank(myString):
    if myString and myString.strip():
        # myString is not None AND myString is not empty or blank
        return False
        # myString is None OR myString is empty or blank
    return True


def change_key_permissions(key_location):
    changepermissions ='chmod 400 ' + key_location
    subprocess.run(changepermissions, shell=True)


def ssh_commands(key_location, instance_dns, command):
    ssh_command = '''ssh -tt -o StrictHostKeyChecking=no -i ''' + key_location[: -1] + ''' ec2-user@'''\
                  +instance_dns+''' '''+command
    subprocess.run(ssh_command, check=True, shell=True)


def scp_commands(key_location, instance_dns):
    scp_command = 'scp -i ' + key_location[: -1] + ' check_webserver.py' \
                  + ' ec2-user@'''+instance_dns+':/tmp'

    subprocess.run(scp_command, check=True, shell=True)


def create_new_home_page(bucket_name_in, key_location, instance_dns):

    bucket_name = bucket_name_in
    object_name = 'image_for_bucket.jpg'

    try:
        image_url = "https://s3-eu-west-1.amazonaws.com/" + bucket_name + "/" + object_name
        html_tag = "<!DOCTYPE html><html><head><title>Assignment One</title></head><body><h1>Assignment One" \
                   "</h1><p>Image displaying from</p><p><a href='" + image_url + "' target='_blank'>" + image_url +\
                   "</a></p><hr><p>This Works Surprisingly!!!!</p><br><img src='" \
                   + image_url + "' height='500px' width='700px'></body></html>"
        index = open("index.html", "w")
        index.write(html_tag)
        index.close()

        touch_index = 'sudo touch /var/www/html/index.html'
        ssh_commands(key_location, instance_dns, touch_index)
        change_permissions = 'sudo chmod 777 /var/www/html/index.html'
        ssh_commands(key_location, instance_dns, change_permissions)
        scp_index = 'scp -i ' + key_location[: -1] +' index.html ec2-user@'+instance_dns+':/var/www/html/'

        subprocess.run(scp_index, check=True, shell=True)
        webbrowser.get('firefox').open_new_tab(instance_dns)

    except CalledProcessError:
        print("error")


def copy_memory_script(key_location, instance_dns):
    ssh_commands(key_location, instance_dns, 'sudo yum groupinstall "Development Tools" -y')
    ssh_commands(key_location, instance_dns, 'sudo yum install python3-devel -y')
    ssh_commands(key_location, instance_dns, 'sudo pip3 install psutil')
    ssh_commands(key_location, instance_dns, 'sudo pip3 install boto3')
    ssh_commands(key_location, instance_dns, 'sudo pip3 install schedule')
    scp_index = 'scp -i ' + key_location[: -1] + ' memory_checker.py ec2-user@'+instance_dns+':/tmp'
    subprocess.run(scp_index, check=True, shell=True)
    newWeb = 'scp -i ' + key_location[: -1] + ' setupweb.py ec2-user@'+instance_dns+':/tmp'
    subprocess.run(newWeb, check=True, shell=True)
    scp_key = 'scp -i ' + key_location[: -1] + ' ' + key_location[: -1] + ' ec2-user@'+instance_dns+':/tmp'
    subprocess.run(scp_key, check=True, shell=True)
    background_script = 'python3 /tmp/memory_checker.py'
    ssh_commands(key_location, instance_dns, background_script)




