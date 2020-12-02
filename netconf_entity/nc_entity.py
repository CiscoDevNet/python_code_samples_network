#!/usr/bin/env python
#
# Copyright (c) 2017  Joe Clarke <jclarke@cisco.com>
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
# This script retrieves the ENTITY-MIB tree from a device via NETCONF and
# prints it out in a "pretty" XML tree.
#

from ncclient import manager
import xml.dom.minidom
import logging
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=sys.argv[0], description='Print ENTITY-MIB data via NETCONF from a device')

    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (NETCONF server username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (NETCONF server password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Enable ncclient debugging")

    parser.set_defaults(debug=False)
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    with manager.connect_ssh(host=args.host, port=args.port, username=args.username, hostkey_verify=False, password=args.password) as m:
        entity_filter = '''
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <ENTITY-MIB xmlns="urn:ietf:params:xml:ns:yang:smiv2:ENTITY-MIB"/>
</filter>
        '''

        try:
            c = m.get(entity_filter).data_xml
            print(xml.dom.minidom.parseString(c).toprettyxml())
        except Exception as e:
            print('Failed to execute <get> RPC: {}'.format(e))
