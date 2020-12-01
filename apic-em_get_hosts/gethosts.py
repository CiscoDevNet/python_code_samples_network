
"""
Simple application that logs on to the APIC-EM and displays all
of the clients connected.  

Leverages the DevNet Sandbox - APIC-EM Always On 
    Information at https://developer.cisco.com/docs/sandbox/#!networking
    
"""


# Import necessary modules
import requests

# Disable warnings
requests.packages.urllib3.disable_warnings()

# Variables
apic_em_ip = "https://sandboxapic.cisco.com/api/v1"
apic_em_user = "devnetuser"
apic_em_password = "Cisco123!"

def get_token(url):

    # Define API Call
    api_call = "/ticket"

    # Payload contains authentication information
    payload = {"username": apic_em_user, "password": apic_em_password}

    # Header information
    headers = {"content-type": "application/json"}

    # Combine URL, API call and parameters variables
    url += api_call

    response = requests.post(url, json=payload, headers=headers, verify=False).json()

    # Return authentication token from respond body
    return response["response"]["serviceTicket"]

def get_hosts(token, url): 
    # Define API Call
    api_call = "/host"

    # Header information
    headers = {"X-AUTH-TOKEN": token}

    # Combine URL, API call and parameters variables
    url += api_call
	
    response = requests.get(url, headers=headers, verify=False).json()
    
    # Get hosts list from response and return
    hosts = response["response"]
    return hosts
    
	
# Assign obtained authentication token to a variable. Provide APIC-EM's
# URL address
auth_token = get_token(apic_em_ip)

# Get list of hosts
hosts = get_hosts(auth_token, apic_em_ip)

# Display in table
print("Client List from APIC-EM")
print("{ip:20} {mac:20} {type:10}".format(ip="IP Address", 
                                          mac="MAC Address", 
                                          type="Type"))

for host in hosts: 
    print("{ip:20} {mac:20} {type:10}".format(ip=host["hostIp"], 
                                              mac=host["hostMac"], 
                                              type=host["hostType"]))
