# EEM: Config Diff to Cisco Spark

An EEM+Python policy that pushes config change diffs to Spark

![](spark_notice1.png)

## Setup

This script requires the following EEM environment variables to be defined:

* `spark_token` : Bearer token for your Spark user/bot
* `spark_room`  : Spark room name to which messages will be sent

    ```
    event manager environment spark_token Bearer 1234abd...
    event manager environment spark_room Network Operators
    ```
    

    
