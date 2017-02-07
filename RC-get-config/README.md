# RESTCONF get-config

This is an example Python script that literally just grabs the entiere config of a network element.

It's not just what you would see from the CLI exec command "show running-config". 
You'll get everything. From all known open-models, and the native-model (which is the translation of the running config a human is used to).

# requirements
-- IOS-XE running >/= 16.3.1 also enabled for RESTCONF

# running
-- Can run on-box or off-box.