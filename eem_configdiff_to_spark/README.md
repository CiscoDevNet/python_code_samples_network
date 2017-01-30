# EEM: Config Diff to Cisco Spark

An EEM+Python policy that pushes config change diffs to Spark.

![](spark_notice1.png)

## Setup

This script requires the IOS-XE _guestshell_ feature.  To enable guestshell, configure:

   ```
   iox
   ```

Then type the following in `EXEC` mode:

   ```
   guestshell enable
   ```

Next, define the following EEM environment. Be sure *NOT* to put quotes around the variable
values:

* `spark_token` : Bearer token for your Spark user/bot
* `spark_room`  : Spark room name to which messages will be sent

    ```
    event manager environment spark_token Bearer 1234abd...
    event manager environment spark_room Network Operators
    ```
Once the environment variables have been defined, copy the script to the EEM user policy
directory.  If you have not defined an EEM user policy directory yet, a good choice is
to create a directory called `flash:/policies` in which to store EEM policies.  Once
the directory has been created, configure:

   ```
   event manager directory user policy flash:policies
   ```

Once your policy has been copied into that directory, register it with the following
command:

   ```
   event manager policy sl_config_diff_to_spark.py
   ```

Once configuration changes start to happen, check your specified Spark room for updates.
