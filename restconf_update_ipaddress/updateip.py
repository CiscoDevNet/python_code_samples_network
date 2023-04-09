#!/usr/bin/env python
"""
    This Python script leverages RESTCONF to:
      - retrieve a list of interfaces on a device
      - ask the user for the interface to configure
      - displays the interface IP information
      - asks user for new IP information
      - updates the IP address on the interface
      - displays the final IP information on the interface

    This script has been tested with Python 3.7, however may work with other versions.

    This script targets the RESTCONF DevNet Sandbox that leverages a CSR1000v as
    a target.  To execute this script against a different device, update the
    variables and command-line arguments that list the connectivity, management
    interface, and url_base for RESTCONF.

    Requirements:
      Python
        - requests


"""

import json
import requests
import sys
import os
import ipaddress
from argparse import ArgumentParser
from collections import OrderedDict
from getpass import getpass
import urllib3

# Disable SSL Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Identify yang+json as the data formats
headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}


# Function to retrieve the list of interfaces on a device
def get_configured_interfaces(url_base, username, password):
    # this statement performs a GET on the specified url
    try:
        response = requests.get(url_base,
                                auth=(username, password),
                                headers=headers,
                                verify=False
                                )
        response.raise_for_status()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # return the json as text
    return response.json()["ietf-interfaces:interfaces"]["interface"]


# Used to configure the IP address on an interface
def configure_ip_address(url_base, interface, ip, username, password):
    # RESTCONF URL for specific interface
    url = url_base + "/interface={i}".format(i=interface)

    # Create the data payload to reconfigure IP address
    # Need to use OrderedDicts to maintain the order of elements
    data = OrderedDict([('ietf-interfaces:interface',
              OrderedDict([
                            ('name', interface),
                            ('type', 'iana-if-type:ethernetCsmacd'),
                            ('ietf-ip:ipv4',
                                OrderedDict([
                                  ('address', [OrderedDict([
                                      ('ip', ip["address"]),
                                      ('netmask', ip["mask"])
                                  ])]
                                  )
                                ])
                            ),
                          ])
                        )])

    # Use PUT request to update data
    try:
        response = requests.put(url,
                                auth=(username, password),
                                headers=headers,
                                verify=False,
                                json=data
                                )
        response.raise_for_status()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    print(response.text)


# Retrieve and print the current configuration of an interface
def print_interface_details(url_base, interface, username, password, cidr):
    url = url_base + "/interface={i}".format(i=interface)

    # this statement performs a GET on the specified url
    try:
        response = requests.get(url,
                                auth=(username, password),
                                headers=headers,
                                verify=False
                                )
        response.raise_for_status()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    intf = response.json()["ietf-interfaces:interface"]
    # return the json as text
    print("Name: ", intf[0]["name"])
    try:
        netmask = intf[0]["ietf-ip:ipv4"]["address"][0]["netmask"]
        if cidr:
            nma = ipaddress.ip_address(netmask)
            netmask = str("{0:b}".format(int(nma)).count('1'))
        print("IP Address: ", intf[0]["ietf-ip:ipv4"]["address"][0]["ip"], "/",
              netmask)
    except KeyError:
        print("IP Address: UNCONFIGURED")
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    print()

    return(intf)


# Ask the user to select an interface to configure.  Ensures input is valid and
# NOT the management interface
def interface_selection(interfaces, mgmt_if):
    # Ask User which interface to configure
    sel = input("Which Interface do you want to configure? ")

    # Validate interface input
    # Must be an interface on the device AND NOT be the Management Interface
    while sel == mgmt_if or not sel in [intf["name"] for intf in interfaces]:
        print("INVALID:  Select an available interface.")
        print("          " + mgmt_if + " is used for management.")
        print("          Choose another Interface")
        sel = input("Which Interface do you want to configure? ")

    return(sel)


# Asks the user to provide an IP address and Mask.
def get_ip_info(cidr):
    # Ask User for IP and Mask
    ip = {}
    try:
        if cidr:
            ipa_t = input("What IP address/prefixlen do you want to set? ")
            ipi = ipaddress.ip_interface(ipa_t)
            ip["address"] = ipi.ip.compressed
            ip["mask"] = ipi.netmask.compressed
        else:
            ipa_t = input("What IP address do you want to set? ")
            ipi = ipaddress.ip_interface(ipa_t)
            ip["address"] = ipi.ip.compressed
            ipm_t = input("What Subnet Mask do you want to set? ")
            ipm = ipaddress.ip_address(ipm_t)
            ip["mask"] = ipm.compressed
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    return(ip)


def main():
    """
    Simple main method calling our function.
    """

    parser = ArgumentParser(
        prog=sys.argv[0], description='RESTCONF interface management tool')
    parser.add_argument('--hostname', '-a', type=str,
                        help='sandbox hostname or IP address',
                        default='ios-xe-mgmt.cisco.com')
    parser.add_argument('--username', '-u', type=str,
                        help='sandbox username', default='developer')
    # Identifies the interface on the device used for management access
    # Used to ensure the script isn't used to update the IP leveraged to manage
    # device
    parser.add_argument('--management_if', '-m', type=str,
                        help='management interface', default='GigabitEthernet1')
    parser.add_argument('--port', '-P', type=int,
                        help='sandbox web port', default=443)
    parser.add_argument('--cidr', help='use CIDR format for interface IP',
                        action='store_true')
    args = parser.parse_args()

    password = os.getenv('DEVNET_RESTCONF_PASSWORD')
    if password is None:
        password = getpass()

    # Create the base URL for RESTCONF calls

    url_base = "https://{h}:{p}/restconf/data/ietf-interfaces:interfaces".format(h=args.hostname, p=args.port)

    # Get a List of Interfaces
    interfaces = get_configured_interfaces(url_base, args.username, password)

    print("The router has the following interfaces: \n")
    for interface in interfaces:
        print("  * {name:25}".format(name=interface["name"]))

    print("")

    # Ask User which interface to configure
    selected_interface = interface_selection(interfaces, args.management_if)
    print(selected_interface)

    # Print Starting Interface Details
    print("Starting Interface Configuration")
    print_interface_details(url_base, selected_interface, args.username,
                            password, args.cidr)

    # As User for IP Address to set
    ip = get_ip_info(args.cidr)

    # Configure interface
    configure_ip_address(url_base, selected_interface, ip, args.username, password)

    # Print Ending Interface Details
    print("Ending Interface Configuration")
    print_interface_details(url_base, selected_interface, args.username,
                            password, args.cidr)

if __name__ == '__main__':
    sys.exit(main())
