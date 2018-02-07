# NETCONF edit-config

This is an example Python script utilizes edit-config. 

The script calls the edit-config verb in NETCONF, and sets the data in the hostname container to what is specified. 

For fun, you'll realize the script reconfigures the hostname of your network element to "NETCONF-WAS-HERE"

# requirements
-- ncclient

-- IOS-XE running >/= 16.5(1) also enabled for NETCONF

# running
-- Can run on-box or off-box.
