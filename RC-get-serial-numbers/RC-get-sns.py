#!/usr/bin/env python
#
# Copyright (c) 2019  Joe Clarke <jclarke@cisco.com>
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
# This script retrieves inventory from devices with RESTCONF and prints all serial
# numbers per device.
#

import requests
from argparse import ArgumentParser


def main():

    parser = ArgumentParser(description='Select options.')

    # Input parameters
    parser.add_argument('-hosts', '--hosts', type=str, required=True,
                        help="Comma-separated list of devices")
    parser.add_argument('-user', '--username', type=str, default='cisco',
                        help="User credentials for the request")
    parser.add_argument('-passwd', '--password', type=str, default='cisco',
                        help="It's the password")

    args = parser.parse_args()
    url = 'https://{}/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/device-hardware'
    inv_cache = {}

    hosts = args.hosts.split(',')

    for host in hosts:

        u = url.format(host)

        headers = {
            'Accept': "application/yang-data+json",
        }

        response = None

        try:
            response = requests.request('GET', u, auth=(
                args.username, args.password), headers=headers, verify=False)
            response.raise_for_status()
        except Exception as e:
            print('Failed to get inventory from device: {}'.format(e))
            continue

        inv = response.json()

        for asset in inv['Cisco-IOS-XE-device-hardware-oper:device-hardware']['device-inventory']:
            if host not in inv_cache:
                inv_cache[host] = []

            if asset['serial-number'] == '':
                continue

            inv_cache[host].append(
                {'sn': asset['serial-number'], 'pn': asset['part-number']})

    for host, comps in inv_cache.items():
        print('Host {} serial numbers:'.format(host))
        for comp in comps:
            print('\t{}'.format(comp['sn']))


if __name__ == '__main__':
    main()
