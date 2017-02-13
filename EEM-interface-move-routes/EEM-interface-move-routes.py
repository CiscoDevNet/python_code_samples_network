#!/usr/bin/env python
#
# Copyright (c) 2017  Jason Frazier <jafrazie@cisco.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# This script retrieves entire configuration from a network element via NETCONF 
# prints it out in a "pretty" XML tree.

# importing the cli module is necessary to run
# config or exec commands on the host.
import cli
# importing the time module works well in 
# this script, as we are pacing some of the execution.

import time
# importing the time module works well in this script, as we are pacing 
# some of the execution.

cli.configure('no ip route 10.10.1.2 255.255.255.255 10.90.1.1');
# CLI route to negate when original event occurs. Idea being, this is the next hop
# on the other end of the interface that went down.
time.sleep(2)
# Sleep, just because. We are doing CLI after all.
cli.configure('ip route 10.10.1.2 255.255.255.255 10.90.1.65');
# CLI route to add when the original event occurs. Next hop of a backup interface.
