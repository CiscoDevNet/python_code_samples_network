# NETCONF get-config with XPATH

This is an example Python script utilizes get-config. It also take advantage of XPATH filtering for NETCONF available in IOS-XE.

The script calls the get-config verb in NETCONF, and then filters the request to the native model, and also asks for just the data in the hostname container. The data you get back should be the hostname (or more specically the configured hostname).

For a human, this is roughly equivalent to 'show running-config | inclue hostname'

# requirements
-- ncclient

-- IOS-XE running >/= 16.3.1 also enabled for NETCONF

# running
-- Can run on-box or off-box.
