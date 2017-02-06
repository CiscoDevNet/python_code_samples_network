# APIC-EM: Print some inventory statistics from APIC-EM

This script uses the APIC-EM REST API to grab the list of devices, and then prints
out the list of device families, total counts of devices per family, model names
per family, and software versions per model.

For example:

    ```
    $ ./apic-em_get_inventory_stats.py --hostname 10.1.1.2 --username admin --password Cisco123
    Routers (total: 3)
     CISCO891W-AGN-A-K9 (total: 1)
      15.4(2)T1 (total: 1)
     CSR1000V (total: 1)
      16.4.1 (total: 1)
     CISCO1941/K9 (total: 1)
      15.6(2)T2 (total: 1)

    Switches and Hubs (total: 1)
     WS-C3560V2-24TS-E (total: 1)
      15.0(2)SE10 (total: 1)
    ...
    ```

## Setup

This script has been tested with Python 2.7, and requires the following non-default module(s):

* ncclient (pip install ncclient)
