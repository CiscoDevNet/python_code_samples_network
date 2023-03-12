# SNMP: Print the results of an snmpwalk of the ENTITY-MIB from a device

This is an off-box Python script that uses net-snmp's Python bindings
to print the results of an snmpwalk of the ENTITY-MIB from a device.

The script uses either SNMPv1 or SNMPv2c.

For example:

   ```
   $ snmp_entity.py -a 10.1.1.1 -c public -v 2
   entPhysicalDescr.1 : CISCO1941/K9 chassis, Hw Serial#: FTX180381QX, Hw Revision: 1.0
   entPhysicalDescr.2 : C1941 Chassis Slot
   entPhysicalDescr.3 : C1941 Mother board 2GE, integrated VPN and 2W
   entPhysicalDescr.4 : C1941 DaughterCard Slot
   entPhysicalDescr.5 : C1941 DaughterCard Slot
   entPhysicalDescr.6 : 8 Port GE POE EHWIC Switch
   entPhysicalDescr.7 : EHWIC-8 Gigabit Ethernet
   ...
   ```

## Setup

This script has been tested with Python 2.7, and requires the following non-default module(s):

* net-snmp's netsnmp module (see http://net-snmp.sourceforge.net/wiki/index.php/Python_Bindings)

  Ubuntu or Debian:

  ```
  $ sudo apt-get install python-netsnmp
  ```

  CentOS:

  ```
  $ yum install net-snmp-python
  ```

  FreeBSD:

  Install `/usr/ports/net-mgmt/net-snmp` and make sure the PYTHON option is enabled.

Additionally, the ENTITY-MIB needs to be loaded into net-snmp.  By default, the MIBs directory
is `/usr/share/snmp/mibs` on Linux and `/usr/local/share/snmp/mibs` on FreeBSD.  Copy
[https://cisco.github.io/cisco-mibs/v2/ENTITY-MIB.my](https://cisco.github.io/cisco-mibs/v2/ENTITY-MIB.my)
to that location before running this script.
