# Get Hosts List from APIC-EM 

This example script uses the requests Python library to interact with the APIC-EM and retrieve the list of clients connected.  
  
This script has been tested with Python 3.5, however may work with other versions.  
    
## DevNet Sandbox 

This script targets the Always On APIC-EM DevNet Sandbox. 

Find details on the Sandbox [here](https://developer.cisco.com/docs/sandbox/#!networking).

To execute this script against a different device, update the variables that list the APIC-EM IP, User and Password.  
    
## Requirements

Python 

- requests

# Getting Started 

* Clone the Python Examples and change into the directory.  

    ```bash 
    git clone https://github.com/CiscoDevNet/python_code_samples_network
    cd apic-em_get_hosts
    ```

* Create and activate a virtualenv 

    ```bash 
    virtualenv venv --python=python3.5
    source venv/bin/activate 
    ```
    
* Install the requirements 

    ```bash
    pip install -r requirements.txt
    ```

* Run the script

    ```
    $ python gethosts.py
    Client List from APIC-EM
    IP Address           MAC Address          Type
    10.1.15.117          00:24:d7:43:59:d8    wireless
    10.2.1.22            5c:f9:dd:52:07:78    wired
    10.1.12.20           e8:9a:8f:7a:22:99    wired   
    ```

