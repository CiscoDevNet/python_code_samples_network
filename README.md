# Network Automation with Python Code Samples 

A collection of Python Code Samples for Network Management.  Includes samples that leverage on-box libraries, as well as samples that use exposed external APIs (NETCONF/RESTCONF, SNMP, SSH, REST, etc).  Some examples make use of available SDKs.  

## On-Box Examples 

Many Cisco switches and routers provide an on-box Python Interpreter that can be leveraged to execute scripts and programs directly on end devices.  In addition to the interpreter, Python libraries are included that provide direct access to the underlying devices operations to execute CLI commands, or monitor for events.  

### Sample Code 

|  Code Sample  |  Description  | 
|  --- |  ---  | 
|  [Execute CLI via Python](/eem_configdiff_to_spark)  |  This example is about as simple as it gets. By leveraging the CLI library, we execute the “show version” command on the box. | 
|  [TDR Test Every Interface](/Py-sho-ver-onbox)  |  This example once again leverages the CLI library, but to do something a bit more interesting.  A TDR test is run on every interface in “up” status.  | 
|  EEM Config Changes to Spark  |  In this example, the EEM library is used to monitor for configuration changes.  When one occurs a message is sent to a Cisco Spark Room.  | 


## Off-Box Examples 

Here are few Python scripts that can interact with network elements using one of the many exposed interfaces (NETCONF, RESTCONF, SNMP, SSH, etc).  Many of these scripts could also be run on-box, however they don’t leverage any of the unique libraries available on device.  

|  Code Sample  |  Description  | 
|  --- |  ---  | 
|  MIB Walk with Python  |  In this example, we perform a MIB walk against a device leveraging the “netsnmp” library for Python.  | 
|  NETCONF Connection with Python  |  This example shows the basics of connecting to a device with NETCONF using the  “ncclient” library for Python.  | 
|  Configure Interface IP Address with RESTCONF  |  In this example the newly ratified RESTCONF standard is used to configure the IP Address on an interface.  | 
|  Get Inventory from APIC-EM  |  APIC-EM maintains an inventory database of the entire network.  In this example Python is used to retrieve that information using the REST API.  |  
|  Get Host List from APIC-EM  |  APIC-EM maintains a list of all clients connected to the network devices discovered by APIC-EM.  This example queries the APIC-EM for the list, and display’s it in a simple table.  | 
|  Retrieve Tenants from ACI APIC  |  This example leverages the ACI Toolkit to connect to an APIC controller and retrieve the list of Tenants configured.  |  
