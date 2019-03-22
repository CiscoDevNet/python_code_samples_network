# Network Automation with Python Code Samples

A collection of Python Code Samples for Network Management.  Includes samples that leverage on-box libraries, as well as samples that use exposed external APIs (NETCONF/RESTCONF, SNMP, SSH, REST, etc).  Some examples make use of available SDKs.  

## On-Box Examples

Many Cisco switches and routers provide an on-box Python Interpreter that can be leveraged to execute scripts and programs directly on end devices.  In addition to the interpreter, Python libraries are included that provide direct access to the underlying devices operations to execute CLI commands, or monitor for events.  

### Sample Code

|  Code Sample  |  Description  |
|  --- |  ---  |
|  [Execute CLI via Python](/Py-sho-ver-onbox)  |  This example is about as simple as it gets. By leveraging the CLI library, we execute the “show version” command on the box. |
|  [TDR Test Every Interface](/tdr-test)  |  This example once again leverages the CLI library, but to do something a bit more interesting.  A TDR test is run on every interface in “up” status.  |
|  [EEM Config Changes to Spark](/eem_configdiff_to_spark)  |  In this example, the EEM library is used to monitor for configuration changes.  When one occurs a message is sent to a Cisco Spark Room.  |
|  [Python with Eventing Example](/EEM-interface-move-routes)  |  Use the EEM and Python together to script based on local events. |
|  [EEM + Python + Spark ChatOps](/spark_checkin)  |  Use the EEM to monitor for config changes and send a Spark Message |  
|  [EEM + Python + Email alert](/PortFlap_email_alert)  |  This example leverages the CLI library and using the EEM feature to monitor for interface flapping and send an email alert |


## Off-Box Examples

Here are few Python scripts that can interact with network elements using one of the many exposed interfaces (NETCONF, RESTCONF, SNMP, SSH, etc).  Many of these scripts could also be run on-box, however they don’t leverage any of the unique libraries available on device.  

|  Code Sample  |  Description  |
|  --- |  ---  |
|  [Netmiko and CLI Example for Interface Management](/netmiko-interface-example)  |  These are a series of python scripts for retrieving, creating, deleting a Loopback Interface with Python.  | 
|  [MIB Walk with Python](/snmp_entity)  |  In this example, we perform a MIB walk against a device leveraging the “netsnmp” library for Python.  |
|  [NETCONF Connection with Python](/netconf_entity)  |  This example shows the basics of connecting to a device with NETCONF using the  “ncclient” library for Python.  |
|  [Configure Interface IP Address with RESTCONF](/restconf_update_ipaddress)  |  In this example the newly ratified RESTCONF standard is used to configure the IP Address on an interface.  |
|  [Get Inventory from APIC-EM](/apic-em_get_inventory_stats)  |  APIC-EM maintains an inventory database of the entire network.  In this example Python is used to retrieve that information using the REST API.  |  
|  [Get Host List from APIC-EM](/apic-em_get_hosts)  |  APIC-EM maintains a list of all clients connected to the network devices discovered by APIC-EM.  This example queries the APIC-EM for the list, and display’s it in a simple table.  |
|  [Retrieve Tenants from ACI APIC](/acitoolkit_show_tenants)  |  This example leverages the ACI Toolkit to connect to an APIC controller and retrieve the list of Tenants configured.  |  
|  [Basic NETCONF Get](/NC-get-config)  |  A basic ncclient example to `<get>` NETCONF Data  |
|  [Basic NETCONF Edit](/NC-edit-config)  |  A basic ncclient example to `<edit-config>` NETCONF Data  |  
|  [NETCONF XPATH Example](/NC-get-config-xpath)  |  Use the XPATH feature when making a NETCONF Requests  |  
|  [Model Based AAA](/model-based-aaa)  |  These example scripts are for Model Based AAA to get, edit and delete the rule-lists for privilege level users and Groups by using ietf-netconf-acm.yang data model  |
|  [RESTCONF](/RESTCONF)  |  These example scripts are for RESTCONF to retrieve and configure the switch using different operations such as Get, Delete, Put, Post and Patch.  |
