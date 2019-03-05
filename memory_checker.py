#!/usr/bin/env python3
import schedule
import time
import psutil
import subprocess
import setupweb


def job():
    if float(psutil.cpu_percent()) > 50.0:
        commands = 'find . -name *.pem'
        print("CPU usage is above threshold: " + str(psutil.cpu_percent()))
        process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = process.communicate(commands.encode('utf-8'))
        key_location = out.decode('utf-8')
        print(setupweb.create_web_server(key_location))


print('Checking memory status')
schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
