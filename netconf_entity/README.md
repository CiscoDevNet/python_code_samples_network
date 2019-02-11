# NETCONF: Print the ENTITY-MIB tree from a device

This is an off-box Python script that uses ncclient to get the ENTITY-MIB
tree from a device and print it as "pretty" XML.

For example:

   ```
   $ nc_entity.py -a 10.1.1.1 -u admin -p admin --port 830
   <?xml version="1.0" ?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
	<ENTITY-MIB xmlns="urn:ietf:params:xml:ns:yang:smiv2:ENTITY-MIB">
		<entityGeneral>
			<entLastChangeTime>114619</entLastChangeTime>
		</entityGeneral>
		<entPhysicalTable>
			<entPhysicalEntry>
				<entPhysicalIndex>1</entPhysicalIndex>
				<entPhysicalDescr>Cisco CSR1000V Chassis</entPhysicalDescr>
				<entPhysicalVendorType>1.3.6.1.4.1.9.12.3.1.3.1165</entPhysicalVendorType>
				<entPhysicalContainedIn>0</entPhysicalContainedIn>
        ...
   ```

## Setup

This script has been tested with Python 2.7, and requires the following non-default module(s):

* ncclient (pip install ncclient)

This script also requires SNMP to be enabled on the target device.  Use the configuration command
`netconf-yang cisco-ia snmp-community-string COMMUNITY` to set the NETCONF community string to
be the same as the read-only string you use on your device.  Note: SNMPv3 is not supported.
