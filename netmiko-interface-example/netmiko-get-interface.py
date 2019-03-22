#! /usr/bin/env python
"""Sample use of the netmiko library for CLI interfacing

This script will retrieve information from a device.

Copyright (c) 2018 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import libraries
from netmiko import ConnectHandler
import re

from device_info import ios_xe1 as device # noqa

# Create a CLI command template
show_interface_config_temp = "show running-config interface {}"

# Open CLI connection to device
with ConnectHandler(ip = device["address"],
                    port = device["ssh_port"],
                    username = device["username"],
                    password = device["password"],
                    device_type = device["device_type"]) as ch:

    # Create desired CLI command and send to device
    command = show_interface_config_temp.format("Loopback103")
    interface = ch.send_command(command)

    # Print the raw command output to the screen
    print(interface)

    try:
        # Use regular expressions to parse the output for desired data
        name = re.search(r'interface (.*)', interface).group(1)
        description = re.search(r'description (.*)', interface).group(1)
        ip_info = re.search(r'ip address (.*) (.*)', interface)
        ip = ip_info.group(1)
        netmask = ip_info.group(2)

        # Print the info to the screen
        print("The interface {name} has ip address {ip}/{mask}".format(
                name = name,
                ip = ip,
                mask = netmask,
                )
            )
    except Exception:
        print("There was an error, Loopback103 might not exist.")
