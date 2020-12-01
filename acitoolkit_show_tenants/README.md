# Using the ACI Toolkit in Python 

This example script shows how you can leverage the [ACI Toolkit](https://github.com/datacenter/acitoolkit) as part of a Python script connecting to an APIC Controller.  

This basic script simply connects to the APIC and displays the list of tenants and is based on the sample [aci-show-tenants.py](https://github.com/datacenter/acitoolkit/blob/master/samples/aci-show-tenants.py) script from the toolkit.  

## ACI Toolkit Installation 

To run this script, you'll need to have installed the ACI Toolkit in your working Python environment.  See [github.com/datacenter/acitoolkit](https://github.com/datacenter/acitoolkit) for installation instructions.  

## DevNet Sandbox 

This script targets the Always On ACI Simulator DevNet Sandbox. 

Find details on the Sandbox [here](https://developer.cisco.com/docs/sandbox/#!data-center).

To execute this script against a different device, update the variables that list the URL, User and Password for the APIC.  

## Requirements

* Python 2.7
* acitoolkit 

# Getting Started 

* Clone the Python Examples and change into the directory.  

    ```bash 
    git clone https://github.com/CiscoDevNet/python_code_samples_network
    cd acitoolkit_show_tenants
    ```
    
* Run the script 

    ```bash
    $ python aci-show-tenants.py
    
    TENANT
    ------
    Tenant_Max
    common
    infra
    SB-T01
    mgmt    
    ```
