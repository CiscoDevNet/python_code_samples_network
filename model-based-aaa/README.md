# Model Based AAA

The NETCONF and RESTCONF are industry standard protocols uses YANG data models for managing network devices. These protocols do not provide any mechanism for authorizing a user with different privilege levels. Every NETCONF or RESTCONF user is a super user with privilege level 15.

NETCONF Access Control Model is a form of role-based access control (RBAC) specified in RFC 6536 can provide rules for privilege levels. A user can be authorized with aaa new-model and the privilege level is determined for that user, in the absence of aaa new-model configuration the locally configured privilege level is used.  Using NACM you can set rules to that privilege level to control what to access for that user. It is a group-based authorization scheme for data and operations modeled in YANG. 

These are examples scripts for the Model Based AAA to retrieve, edit and delete the rules for a privilege level by using ietf-netconf-acm.yang data model. There are also examples for configuring and deleting users in a group.

## requirements

-- ncclient
-- IOS-XE running >/= 16.8 also enabled for NETCONF

