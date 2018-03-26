#!/usr/bin/python
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
# This script configures Ip address of a interface using PATCH operation via RESTCONF 

# import the requests library
import requests
import sys

# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()

# use the IP address or hostname of your Cat9300
HOST = '172.26.198.63'

# use your user credentials to access the Cat9300
USER = 'cisco'
PASS = 'cisco'


# create a main() method
def main():
    """Main method that configures the Ip address for a interface via RESTCONF."""

    # url string to issue GET request
    url = "https://{h}/restconf/data/Cisco-IOS-XE-native:native/interface/TenGigabitEthernet=1%2F0%2F10/ip/address/primary".format(h=HOST)
    payload = "{\"primary\": {\"address\": \"100.100.100.1\", \"mask\": \"255.255.255.0\"}}"

    # RESTCONF media types for REST API headers
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}
    # this statement performs a PATCH on the specified url
    response = requests.request("PATCH",url, auth=(USER, PASS),
                            data=payload, headers=headers, verify=False)
                            
    # print the json that is returned
    print(response.text)

if __name__ == '__main__':
    sys.exit(main())
