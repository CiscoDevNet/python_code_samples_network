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

import netsnmp
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=sys.argv[0], description='Print the snmpwalk of the ENTITY-MIB from a device')

    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-c', '--community', type=str, required=True,
                        help="SNMP community string")
    parser.add_argument('-v', '--version', type=int, required=True,
                        help="SNMP version (1 or 2 [for v2c])")

    args = parser.parse_args()

    if args.version != 1 and args.version != 2:
        parser.error('SNMP version must be either 1 or 2')

    vars = netsnmp.VarList(netsnmp.Varbind('entityMIB'))
    netsnmp.snmpwalk(vars,
        Version = args.version,
        DestHost = args.host,
        Community = args.community)

for var in vars:
    print('{}.{} : {}'.format(var.tag, var.iid, var.val))
