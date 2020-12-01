# Using Netmiko to work with Interfaces

These example scripts use the Netmiko Python library to interact with a device through CLI

These Python scripts leverages Netmiko to:
  - Create Loopback 103
  - Retrieve details about Loopback 103
  - Delete Loopback 103

This script has been tested with Python 3.6, however may work with other versions.  

## DevNet Sandbox

This script targets the [IOS XE DevNet Always On Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/27d9747a-db48-4565-8d44-df318fce37ad?diagramType=Topology) that leverages a CSR1000v as a target.  

To execute this script against a different device, create a new device dictionary in `device_info.py` for your device.  Then import this new dictionary instead of `ios_xe1` in the scripts.

## Requirements

Python

- netmiko

# Getting Started

* Clone the Python Examples and change into the directory.  

    ```bash
    git clone https://github.com/CiscoDevNet/python_code_samples_network.git
    cd python_code_samples_network
    cd netmiko-interface-example
    ```

* Create and activate a virtualenv

    ```bash
    Windows - recommendation to use git-bash terminal
    py -3 -m venv venv
    source venv/Scripts/activate

    MacOS or Linux
    python3.6 -m venv venv
    source venv/bin/activate

    ```

* Install the requirements

    ```bash
    pip install -r requirements.txt
    ```

* Run the scripts

    ```
    # Run the get script to retrieve interface
    $ python netmiko-get-interface.py

    # Output - Interface not there yet...                                                ^
    % Invalid input detected at '^' marker.

    There was an error, Loopback103 might not exist.

    # Run the create script to create interface
    $ python netmiko-create-interface.py

    # Output - what was configured
    The following configuration was sent:
    config term
    Enter configuration commands, one per line.  End with CNTL/Z.
    csr1000v(config)#interface Loopback103
    csr1000v(config-if)#description Demo interface by CLI and netmiko
    csr1000v(config-if)#ip address 192.168.103.1 255.255.255.0
    csr1000v(config-if)#no shut
    csr1000v(config-if)#end
    csr1000v#

    # Run the get script again
    $ python netmiko-get-interface.py

    # Output - there it is!
    Building configuration...

    Current configuration : 116 bytes
    !
    interface Loopback103
     description Demo interface by CLI and netmiko
     ip address 192.168.103.1 255.255.255.0
    end

    The interface Loopback103 has ip address 192.168.103.1/255.255.255.0

    # Run the delete script to remove the interface
    $ python netmiko-delete-interface.py

    # Output - what was sent to remove the interface
    The following configuration was sent:
    config term
    Enter configuration commands, one per line.  End with CNTL/Z.
    csr1000v(config)#no interface Loopback103
    csr1000v(config)#end
    csr1000v#
    ```
