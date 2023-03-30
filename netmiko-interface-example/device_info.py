#! /usr/bin/env python
"""Device Details for DevNet Sandboxes

This script is imported into other code.

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

__author__ = "Hank Preston"
__author_email__ = "hapresto@cisco.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"

# DevNet Always-On NETCONF/YANG & RESTCONF Sandbox Device
# https://devnetsandbox.cisco.com/RM/Diagram/Index/27d9747a-db48-4565-8d44-df318fce37ad?diagramType=Topology
ios_xe1 = {
             "address": "ios-xe-mgmt.cisco.com",
             "netconf_port": 10000,
             "restconf_port": 9443,
             "ssh_port": 8181,
             "username": "root",
             "password": "D_Vay!_10&",
             "device_type": "cisco_ios"
          }
# DevNet Always-On NETCONF/YANG & RESTCONF Sandbox Device
# https://devnetsandbox.cisco.com/RM/Diagram/Index/7b4d4209-a17c-4bc3-9b38-f15184e53a94?diagramType=Topology
# try this one if you can't access the previous one
ios_xe_latest = {
             "address": "sandbox-iosxe-latest-1.cisco.com",
             "netconf_port": 830,
             "restconf_port": 443,
             "ssh_port": 22,
             "username": "admin",
             "password": "C1sco12345",
             "device_type": "cisco_ios"
          }
# DevNet Always-On Sandbox NX-OS
#
nxos1 = {
             "address": "sbx-nxos-mgmt.cisco.com",
             "netconf_port": 10000,
             "restconf_port": 443,
             "ssh_port": 818122,
             "username": "admin",
             "password": "Admin_1234!",
             "device_type": "cisco_nxos"
          }

# Sample GitHub Editor Comment.  
