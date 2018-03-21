# RESTCONF

The RESTCONF is a standard protocol uses YANG data models for managing network devices. It is a protocol based on HTTP to access the configuration data or state data of a networking device. RESTCONF supports operations such as Get, Put, Post, Patch, and Delete. One of the major advantages RESTCONF has over NETCONF is its ability to leverage JSON as a data format. To make the RESTCONF calls, you can use any client application that supports any REST call.

These are examples scripts for RESTCONF to retrieve and configure the switch using different operations such as Get, Delete, Post, Put and Patch.

## requirements

-- IOS-XE running >/= 16.8 also enabled for RESTCONF

