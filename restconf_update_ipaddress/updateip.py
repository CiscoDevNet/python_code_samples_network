#!/usr/bin/env python
"""
    This Python script leverages RESTCONF to:
      - retrieve a list of interfaces on a device
      - ask the user for the interface to configure
      - displays the interface IP information
      - asks user for new IP information
      - updates the IP address on the interface
      - displays the final IP information on the interface

    This script has been tested with Python 3.5, however may work with other versions.

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
from argparse import ArgumentParser
from collections import OrderedDict
from getpass import getpass
import urllib3

# Disable SSL Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Identifies the interface on the device used for management access
# Used to ensure the script isn't used to update the IP leveraged to manage device
MANAGEMENT_INTERFACE = "GigabitEthernet1"

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
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if response.status_code >= 300:
       print('request error:', str(response.status_code), response.reason, file=sys.stderr)
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
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if response.status_code >= 300:
       print('request error:', str(response.status_code), response.reason, file=sys.stderr)
       sys.exit(1)

    print(response.text)


# Retrieve and print the current configuration of an interface
def print_interface_details(url_base, interface, username, password):
    url = url_base + "/interface={i}".format(i=interface)

    # this statement performs a GET on the specified url
    try:
        response = requests.get(url,
                                auth=(username, password),
                                headers=headers,
                                verify=False
                                )
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if response.status_code >= 300:
       print('request error:', str(response.status_code), response.reason, file=sys.stderr)
       sys.exit(1)


    intf = response.json()["ietf-interfaces:interface"]
    # return the json as text
    print("Name: ", intf[0]["name"])
    try:
        print("IP Address: ", intf[0]["ietf-ip:ipv4"]["address"][0]["ip"], "/",
                              intf[0]["ietf-ip:ipv4"]["address"][0]["netmask"])
    except KeyError:
        print("IP Address: UNCONFIGURED")
    print()

    return(intf)


# Ask the user to select an interface to configure.  Ensures input is valid and
# NOT the management interface
def interface_selection(interfaces):
    # Ask User which interface to configure
    sel = input("Which Interface do you want to configure? ")

    # Validate interface input
    # Must be an interface on the device AND NOT be the Management Interface
    while sel == MANAGEMENT_INTERFACE or not sel in [intf["name"] for intf in interfaces]:
        print("INVALID:  Select an available interface.")
        print("          " + MANAGEMENT_INTERFACE + " is used for management.")
        print("          Choose another Interface")
        sel = input("Which Interface do you want to configure? ")

    return(sel)


# Asks the user to provide an IP address and Mask.  Data is NOT validated.
def get_ip_info():
    # Ask User for IP and Mask
    ip = {}
    ip["address"] = input("What IP address do you want to set? ")
    ip["mask"] = input("What Subnet Mask do you want to set? ")
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
    parser.add_argument('--port', '-P', type=int,
                        help='sandbox web port', default=443)
    args = parser.parse_args()

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
    selected_interface = interface_selection(interfaces)
    print(selected_interface)

    # Print Starting Interface Details
    print("Starting Interface Configuration")
    print_interface_details(url_base, selected_interface, args.username,
                            password)

    # As User for IP Address to set
    ip = get_ip_info()

    # Configure interface
    configure_ip_address(url_base, selected_interface, ip, args.username, password)

    # Print Ending Interface Details
    print("Ending Interface Configuration")
    print_interface_details(url_base, selected_interface, args.username,
                            password)

if __name__ == '__main__':
    sys.exit(main())
