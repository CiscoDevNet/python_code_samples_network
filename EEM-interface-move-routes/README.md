# EEM interface-move-routes.py

This is an example Python script utilizing EEM integration. 

The example EEM is below:

```
event manager applet INTERFACE-DOWN
 event syslog pattern "LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0, changed state to down"
 action 0.0 cli command "en"
 action 1.0 cli command "guestshell run python EEM-interface-routes.py"
```

As you can see, this EEM policy named "INTERFACE-DOWN" looks for a syslog pattern. In this example case, it is a syslog pattern for a specifc interface going down. When EEM sees this, it triggers an exec CLI that executes the onbox Python script named "EEM-interface-routes.py"

No verification has been built into this, but the script could be extednded as well.

# requirements
-- IOS-XE running >/= 16.5.1 also enabled for GuestShell

# running
-- onbox
