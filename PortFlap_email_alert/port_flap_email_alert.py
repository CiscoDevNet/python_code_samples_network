#
# Copyright (c) 2018  Krishna Kotha <krkotha@cisco.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# PURPOSE of this SCRIPT
# The purpose of this script is if a interface flapped 5 times in last 5 minutes it will shutdown that interface. You can change that flapping count to what ever you want.
# Then it will wait for 5 mins and enable that interface.
# If still flapping atleast once it will shutdown that interface and will send an email alert.
#
#
# This script monitors the interface GigabitEthernet1/0/5, change the interface ID based on your requirement.
#
#
# This script requires the following variables to be defined:
# FROM_ADDR
# TO_ADDR
# name-server ip address
# http_proxy and https_proxy commands
#

# importing necessary modules
import os
import sys
import cli
import time
import difflib
from datetime import datetime
from time import strptime
from time import mktime
import smtplib
import shutil
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import subprocess


def checkPortFlap(port_flaps_cnt,interface):

    # calculate current time using time module
    currTime = time.time()
    print("curr time is: %s" % (currTime))

    # retrieve the show log output
    arr_output = cli.cli("show log").split("\n")

    for line in arr_output:

        # In this example I am monitoring the Gi 1/0/5 interface, based on your requirement change the interface ID.
        if(line.find("GigabitEthernet1/0/5, changed state to down") != -1):
            print("The line %s indicates a port flap action" % (line))
            line_arr = line.split("%")

            # seperate the date from the log lines and convert the matching line to list objects and strings
            date_in_log = line_arr[0]
            print("the entry date is: %s" % (date_in_log))
            line_arr = line.split(",")
            line_arr_1 = line_arr[0].split(" ")
            str_line_arr_0=''.join(line_arr_1[0])

            # remove * and : from the strings
            str_line_arr_0= str_line_arr_0[1:]
            str_line_arr_1=''.join(line_arr_1[3])  
            str_line_arr_1=str_line_arr_1[:-1]

            # parse a string to represent a time according to a format
            log_time = time.strptime(str_line_arr_0+" "+line_arr_1[1]+" "+line_arr_1[2]+" "+str_line_arr_1, "%b %d %Y %H:%M:%S") 
            
            # calculate the log time in seconds
            log_time_secs = mktime(log_time)

            # calculate the difference from current time to log time
            delta=currTime-log_time_secs
            interface = line_arr_1[len(line_arr_1) - 1]
            print("the interface is: %s" % (interface))
            
            # if delta is less than 5 minutes that log will be counted.
            if delta <= 300:
                port_flaps_cnt = port_flaps_cnt + 1  
    return port_flaps_cnt, interface
           
       

def send_e_mail(subject):
    """
    send an e mail from the Cisco network to anyone -
    Note: This example uses from address as a Cisco server, Change the domain to your SMTP server to send email from your domain.
    """
    
    # retrieve the hostname using in-built cli module
    host_name = cli.cli("show running-config | include hostname")
    FROM_ADDR = 'xxxx@cisco.com'
    TO_ADDR = 'xxxx@gmail.com'
    
    # create the message
    msg = MIMEMultipart()
    msg['From'] = FROM_ADDR
    msg['To'] = TO_ADDR
    msg['Subject'] = "%s - %s" % (subject, host_name)
    text = "This is an automated e mail message:\n===========================\nAn on-Box Python script running on a Cisco Polaris guestshell device and detected that the %s %s \n===========================\n\n\n===========================\n\n" % (subject, host_name)
    msg.attach(MIMEText(text, 'plain'))
    
    # connect to server and send
    server = smtplib.SMTP('outbound.your_company_name.com', 25)
    server.sendmail(FROM_ADDR, TO_ADDR, msg.as_string())
    server.quit()


def set_device_to_role_as_cisco_mail_server():
    """
    Manipulates the /etc/resolv.conf and set it to a Cisco mail server. The commands are known to the average network Linux admin...
    """
    commands_to_run_on_gs = [
                            "sudo rm /etc/resolv.conf",
                            "sudo touch /etc/resolv.conf",
                            "echo \"nameserver x.x.x.x\" | sudo tee -a /etc/resolv.conf",
                            "echo \"domain x.x.x.x.com\" | sudo tee -a /etc/resolv.conf",                     
                            "echo \"export http_proxy=http://x.x.x.x:80/\" | sudo tee -a /etc/bashrc",
                            "echo \"export https_proxy=http://x.x.x.x:80/\" | sudo tee -a /etc/bashrc",
                            "echo \"export ftp_proxy=http://x.x.x.x:80/\" | sudo tee -a /etc/bashrc",
                            "echo \"export no_proxy=.x.x.x.x.com\" | sudo tee -a /etc/bashrc",
                            "echo \"export HTTP_PROXY=http://x.x.x.x:80/\" | sudo tee -a /etc/bashrc",
                            "echo \"export HTTPS_PROXY=http://x.x.x.x:80/\" | sudo tee -a /etc/bashrc",
                            "echo \"export FTP_PROXY=http://x.x.x.x:80/\" | sudo tee -a /etc/bashrc"
                             ]
    for command in commands_to_run_on_gs:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        print "Linux command output is", output        


# main code:
if __name__ == '__main__':

    # these commands are need to remove msec and add year in the show log command
    cli.configurep("service timestamps log datetime")
    cli.configurep("service timestamps log datetime year")


    port_flaps_cnt = 0
    interface = None  
    port_flaps = checkPortFlap(port_flaps_cnt,interface)

    if(port_flaps[0] == 10):
        if(port_flaps[1] is not None):
            print("shutting down interface %s" % (port_flaps[1]))

            # shut down the interface using cli module
            #cli(["interface %s" % (port_flaps[1]), "shut", "end"])
            cli.configurep(["interface %s" % (port_flaps[1]), "shut", "end"])

            # wait for 5 mins to monitor the interface flap again
            time.sleep(300) 
            print("Waited for 5 mins Enabling the interface %s" % (port_flaps[1]))

            # enable the interface
            #cli("cont f", "interfact %s" % (port_flaps[1]), "no shut", "end")
            cli.configurep(["interface %s" % (port_flaps[1]), "no shut", "end"])
            port_flaps_cnt = 0
            interface = None 

            # re check the interface is flapping or not
            port_flaps = checkPortFlap(port_flaps_cnt,interface)

            # if still flapping shut down the interface and send email
            if(port_flaps[0] >= 2):
                if(port_flaps[1] is not None):
                    print("shutting down interface %s" % (port_flaps[1]))
                    #cli("cont f", "interfact %s" % (port_flaps[1]), "shut", "end")
                    cli.configurep(["interface %s" % (port_flaps[1]), "shut", "end"])
                    set_device_to_role_as_cisco_mail_server()   
                    send_e_mail("interface %s is flapping and did admin shutdown" % (port_flaps[1]))
