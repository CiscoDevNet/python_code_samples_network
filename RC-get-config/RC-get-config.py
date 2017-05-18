#!/usr/bin/env python
#
# Copyright (c) 2017  Jason Frazier <jafrazie@cisco.com>
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
# This script retrieves entire configuration from a network element via NETCONF 
# prints it out in a "pretty" XML tree.

from argparse import ArgumentParser
import requests

if __name__ == '__main__':

    parser = ArgumentParser(description='Select options.')

    # Input parameters
    parser.add_argument('-host', '--host', type=str, required=True,
                        help="The device IP or DN")
    parser.add_argument('-user', '--username', type=str, default='cisco',
                        help="User credentials for the request")
    parser.add_argument('-passwd', '--password', type=str, default='cisco',
                        help="It's the password")
    parser.add_argument('-port', '--port', type=int, default=443,
                        help="Specify this if you want a non-default port")

    args = parser.parse_args()

    username = args.username
    password = args.password
    host = args.host
    port = str(args.port)

    url = "https://" + host + ":" + port + "/restconf/api/running/"

    headers = {
       "Content-Type": "application/vnd.yang.datastore+json",
       "Accept": "application/vnd.yang.datastore+json",
       }
    response = requests.request("GET", url, headers=headers, auth=(username,password), verify=False)

    print(response.text)
