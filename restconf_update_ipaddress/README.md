# Calling RESTCONF with Python 

This example script uses the requests Python library to interact with a RESTCONF Agent.  

This Python script leverages RESTCONF to: 
  - retrieve a list of interfaces on a device
  - ask the user for the interface to configure 
  - displays the interface IP information 
  - asks user for new IP information 
  - updates the IP address on the interface 
  - displays the final IP information on the interface 
  
This script has been tested with Python 3.7, however may work with other versions.  
    
## DevNet Sandbox 

This script targets the RESTCONF DevNet Sandbox that leverages a CSR1000v as a target.  

Find details on the Sandbox [here](https://developer.cisco.com/docs/sandbox/#!networking).

To execute this script against a different device, update the variables that list the connectivity, management interface, and url_base for RESTCONF.  
    
## Requirements

Python 

- requests

# Getting Started 

* Clone the Python Examples and change into the directory.  

    ```bash 
    git clone https://github.com/CiscoDevNet/python_code_samples_network
    cd restconf_update_ipaddress
    ```

* Create and activate a virtualenv 

    ```bash 
    virtualenv venv --python=python3.7
    source venv/bin/activate 
    ```
    
* Install the requirements 

    ```bash
    pip install -r requirements.txt
    ```

* Run the script

    ```
    $ python updateip.py

    # Output
    The router has the following interfaces:
    
      * GigabitEthernet1
      * GigabitEthernet2
      * GigabitEthernet3
    
    Which Interface do you want to configure? GigabitEthernet2
    GigabitEthernet2
    Starting Interface Configuration
    Name:  GigabitEthernet2
    IP Address:  101.101.10.10 / 255.255.255.0
    
    What IP address do you want to set? 9.9.9.9
    What Subnet Mask do you want to set? 255.255.255.0
    
    Ending Interface Configuration
    Name:  GigabitEthernet2
    IP Address:  9.9.9.9 / 255.255.255.0    
    ```

