#!/usr/bin/env python
"""
Simple application that logs on to the APIC and displays all
of the Tenants.  

Leverages the DevNet Sandbox - APIC Simulator Always On 
    Information at https://developer.cisco.com/docs/sandbox/#!data-center
    
Code sample based off the ACI-Toolkit Code sample

https://github.com/datacenter/acitoolkit/blob/master/samples/aci-show-tenants.py     
"""


import sys
import acitoolkit.acitoolkit as ACI

# Credentials and information for the DevNet ACI Simulator Always-On Sandbox
APIC_URL = "https://sandboxapicdc.cisco.com/"
APIC_USER = "admin"
APIC_PASSWORD = "C1sco12345"

def main():
    """
    Main execution routine
    :return: None
    """

    # Login to APIC
    session = ACI.Session(APIC_URL, APIC_USER, APIC_PASSWORD)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        sys.exit(0)

    # Download all of the tenants
    print("TENANT")
    print("------")
    tenants = ACI.Tenant.get(session)
    for tenant in tenants:
        print(tenant.name)

if __name__ == '__main__':
    main()
