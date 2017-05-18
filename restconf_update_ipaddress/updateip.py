#!/usr/bin/env python
"""
    This Python script leverages RESTCONF to:
      - retrieve a list of interfaces on a device
      - ask the user for the interface to configure
      - displays the interface IP information
      - asks user for new IP information
      - updates the IP address on the interface
      - displays the final IP information on the interface

    This script has been tested with Python 3.5 and 2.7, however may work with other versions.

    This script targets the RESTCONF DevNet Sandbox that leverages a CSR1000v as
    a target.  To execute this script against a different device, update the variables
    that list the connectivity, management interface, and url_base for RESTCONF.

    Requirements:
      Python
        - requests


"""

import json
import requests
import sys
from argparse import ArgumentParser
from collections import OrderedDict

# These variables target the RESTCONF Always-On Sandbox hosted by Cisco DevNet
HOST = 'ios-xe-mgmt.cisco.com'
PORT = '9443'
USER = 'root'
PASS = 'D_Vay!_10&'

# Identifies the interface on the device used for management access
# Used to ensure the script isn't used to update the IP leveraged to
# manage device
MANAGEMENT_INTERFACE = "GigabitEthernet1"

# Create the base URL for RESTCONF calls
url_base = "{proto}://{h}:{p}/restconf/api"

do_input = None

# Identify yang+json as the data formats
headers = {'Content-Type': 'application/vnd.yang.data+json',
           'Accept': 'application/vnd.yang.data+json'}


# Function to retrieve the list of interfaces on a device
def get_configured_interfaces(args):
    url = url_base.format(proto=args.proto, h=args.host,
                          p=args.port) + "/running/interfaces?deep"

    # this statement performs a GET on the specified url
    response = requests.get(url,
                            auth=(args.username, args.password),
                            headers=headers,
                            verify=False
                            )

    # return the json as text
    return response.json()["ietf-interfaces:interfaces"]["interface"]


# Used to configure the IP address on an interface
def configure_ip_address(args, interface, ip):
    # RESTCONF URL for specific interface
    url = url_base.format(proto=args.proto, h=args.host, p=args.port) + \
        "/running/interfaces/interface/{i}".format(i=interface)

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
    response = requests.put(url,
                            auth=(args.username, args.password),
                            headers=headers,
                            verify=False,
                            json=data
                            )
    print(response.text)


# Retrieve and print the current configuration of an interface
def print_interface_details(args, interface):
    url = url_base.format(proto=args.proto, h=args.host, p=args.port) + \
        "/running/interfaces/interface/{i}?deep".format(i=interface)

    # this statement performs a GET on the specified url
    response = requests.get(url,
                            auth=(args.username, args.password),
                            headers=headers,
                            verify=False
                            )

    intf = response.json()["ietf-interfaces:interface"]
    # return the json as text
    print("Name: {}".format(intf["name"]))
    print("IP Address: {} / {}".format(intf["ietf-ip:ipv4"]["address"][0]["ip"],
                                       intf["ietf-ip:ipv4"]["address"][0]["netmask"]))
    print('')

    return(intf)


# Ask the user to select an interface to configure.  Ensures input is valid and
# NOT the management interface
def interface_selection(args, interfaces):
    # Ask User which interface to configure
    sel = do_input("Which Interface do you want to configure? ")

    # Validate interface input
    # Must be an interface on the device AND NOT be the Management Interface
    while sel == args.interface or not sel in [intf["name"] for intf in interfaces]:
        print("INVALID:  Select an available interface.")
        print("          " + args.interface + " is used for management.")
        print("          Choose another Interface")
        sel = do_input("Which Interface do you want to configure? ")

    return(sel)


# Asks the user to provide an IP address and Mask.  Data is NOT validated.
def get_ip_info():
    # Ask User for IP and Mask
    ip = {}
    ip["address"] = do_input("What IP address do you want to set? ")
    ip["mask"] = do_input("What Subnet Mask do you want to set? ")
    return(ip)


def main():
    global do_input

    """
    Simple main method calling our function.
    """

    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--host', type=str, default=HOST,
                        help='The device IP or hostname')
    parser.add_argument('-u', '--username', type=str,
                        default=USER, help='Username for the device')
    parser.add_argument('-p', '--password', type=str,
                        default=PASS, help='Password for the device')
    parser.add_argument('--port', type=int, default=PORT,
                        help='RESTCONF port for the device')
    parser.add_argument('--use-ssl', dest='proto', action='store_true',
                        default=False, help='Use SSL to connect; default is no encryption')
    parser.add_argument('-i', '--mgmt-interface', dest='interface', type=str,
                        default=MANAGEMENT_INTERFACE, help='Management interface of the device')
    args = parser.parse_args()

    if args.proto:
        args.proto = 'https'
    else:
        args.proto = 'http'

    try:
        do_input = raw_input
    except NameError:
        do_input = input

    # Get a List of Interfaces
    interfaces = get_configured_interfaces(args)

    print("The router has the following interfaces: \n")
    for interface in interfaces:
        print("  * {name:25}".format(name=interface["name"]))

    print("")

    # Ask User which interface to configure
    selected_interface = interface_selection(args, interfaces)
    print(selected_interface)

    # Print Starting Interface Details
    print("Starting Interface Configuration")
    print_interface_details(args, selected_interface)

    # As User for IP Address to set
    ip = get_ip_info()

    # Configure interface
    configure_ip_address(args, selected_interface, ip)

    # Print Ending Interface Details
    print("Ending Interface Configuration")
    print_interface_details(args, selected_interface)


if __name__ == '__main__':
    sys.exit(main())
