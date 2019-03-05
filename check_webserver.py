from subprocess import *

try:
    checkhttpd = 'ps -A | grep httpd'
    starthttpd = """#!/bin/bash
		sudo yum install httpd -y
		sudo systemctl enable httpd
		sudo systemctl start httpd"""

    run(checkhttpd, check=True, shell=True)
    print("Web Server IS running")

except CalledProcessError:
    print("Web Server IS NOT running")
    print("Starting Web Server")
    try:
        run(starthttpd, check=True, shell=True)
        print("Web Server IS running")

    except CalledProcessError:
        print("Web Server IS NOT running")
