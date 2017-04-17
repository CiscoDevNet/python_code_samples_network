# EEM Spark-CheckIn

This example script sends a notification message to a Cisco Spark user of a Configuration Change.  It was created to be used along with an EEM Applet that monitors for configuration changes, and then executes the script leveraging Python withing Guest Shell.  

This example was tested using IOS-XE 16.5.1b on an ISR 4K router, but should work on other platforms supporting Guest Shell.  

This example script uses the CiscoSparkApi Python library to send the Spark Message.  

You will need to provide the Spark Authorization Token and recipient email address within the EEM Configuration.  It is recommended that you create a [Bot Account](https://developer.ciscospark.com/bots.html) for this use case.  
  
This script has been tested with Python 2.7, however may work with other versions.  
    
    
# Requirements and Setup 

## Host Device and Guest Shell

IOS-XE or NX-OS device supporting Guest Shell and EEM.  

Example Steps to configure Guest Shell on IOS-XE are: 

```
conf t
iox
exit
guestshell enable 

! Enter Guest Shell with 
guestshell run bash 
```

### Python Library

- ciscosparkapi Python Library 

```
# From within Guest Shell 
sudo -E pip install ciscosparkapi 
```

## Create folder for Scripts and Add Script 

```
# From within Guest Shell 
mkdir /bootflash/scripts 
cd /bootflash/scripts
wget https://raw.githubusercontent.com/CiscoDevNet/python_code_samples_network/master/spark_checkin/spark_checkin.py

```

## Test Script 

Test the script by running in manually from within guestshell.  

```
python spark_checkin.py -t SPARK_AUTH_TOKEN -e DESTINATION_EMAIL
```

You should recieve a message similar to this in Spark.  

![](Spark_Message.png)

## Setup EEM Applet

Back within IOS, configure the EEM Applet to monitor for Configuration Changes.  

```
event manager applet GUESTSHELL-CONFIG-CHANGE-TO-SPARK
 event syslog pattern "%SYS-5-CONFIG_I: Configured from"
 action 0.0 cli command "en"
 action 1.0 cli command "python spark_checkin.py -t SPARK_AUTH_TOKEN -e DESTINATION_EMAIL"
```
