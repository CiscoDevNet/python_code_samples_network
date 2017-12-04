::cisco::eem::event_register_syslog pattern "CONFIG_I" maxrun 60
#
# Copyright (c) 2017  Joe Clarke <jclarke@cisco.com>
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
# This script requires the following EEM environment variables to be defined:
#
# spark_token : Bearer token for your Spark user/bot
# spark_room  : Spark room name to which messages will be sent
# device_name : Device name from which the messages will be sent
#
# E.g.:
#
# event manager environment spark_token Bearer 1234abd...
# event manager environment spark_room Network Operators
# event manager environment device_name C3850
#

import eem
import sys
import os
import requests
import re

CFG_BAK_PY = '/flash/running-config.bak'
CFG_BAK_IOS = 'flash:/running-config.bak'
SPARK_API = 'https://api.ciscospark.com/v1/'

# Get the CLI event variables for this specific event.
arr_einfo = eem.event_reqinfo()
# Get the environment variables
arr_envinfo = eem.env_reqinfo()

if 'spark_token' not in arr_envinfo:
    eem.action_syslog(
        'Environment variable "spark_token" must be set', priority='3')
    sys.exit(1)
if 'spark_room' not in arr_envinfo:
    eem.action_syslog(
        'Environment variable "spark_room" must be set', priority='3')
    sys.exit(1)
if 'device_name' not in arr_envinfo:
    eem.action_syslog(
        'Environment variable "device_name" must be set', priority='3')
    sys.exit(1)

# Get a CLI handle
cli = eem.cli_open()
eem.cli_exec(cli, 'enable')

if not os.path.isfile(CFG_BAK_PY):
    try:
        eem.cli_write(cli, 'copy runn {}'.format(CFG_BAK_IOS))
        prom = eem.cli_read_pattern(cli, '(filename|#)')
        if re.search(r'filename', prom):
            eem.cli_exec(cli, '\r')
    except Exception as e:
        eem.action_syslog('Failed to backup configuration to {}: {}'.format(
            CFG_BAK_IOS, e), priority='3')
        sys.exit(1)
    # First time through, only save the current config
    eem.cli_close(cli)
    sys.exit(0)

res = None
try:
    res = eem.cli_exec(
        cli, 'show archive config diff {} system:running-config'.format(CFG_BAK_IOS))
    os.remove(CFG_BAK_PY)
    eem.cli_write(cli, 'copy runn {}'.format(CFG_BAK_IOS))
    prom = eem.cli_read_pattern(cli, 'filename')
    if re.search(r'filename', prom):
        eem.cli_exec(cli, '\r')
except Exception as e:
    eem.action_syslog(
        'Failed to get config differences: {}'.format(e), priority='3')
    sys.exit(1)

eem.cli_close(cli)

diff_lines = re.split(r'\r?\n', res)
if re.search('No changes were found', res):
    # No differences found
    sys.exit(0)

device_name = arr_envinfo['device_name']
msg = '### Alert: Config changed on ' + device_name + '\n'
msg += 'Configuration differences between the running config and last backup:\n'
msg += '```{}```'.format('\n'.join(diff_lines[:-1]))

headers = {
    'authorization': arr_envinfo['spark_token'],
    'content-type': 'application/json'
}

# Get the Spark room ID
url = SPARK_API + 'rooms'

r = None
try:
    r = requests.request('GET', url, headers=headers)
    r.raise_for_status()
except Exception as e:
    eem.action_syslog(
        'Failed to get list of Spark rooms: {}'.format(e), priority='3')
    sys.exit(1)

room_id = None
for room in r.json()['items']:
    if room['title'] == arr_envinfo['spark_room']:
        room_id = room['id']
        break

if room_id is None:
    eem.action_syslog('Failed to find room ID for {}'.format(
        arr_envinfo['spark_room']))
    sys.exit(1)

# Post the message to Spark
url = SPARK_API + 'messages'

payload = {'roomId': room_id, 'markdown': msg}

try:
    r = requests.request(
        'POST', url, json=payload, headers=headers)
    r.raise_for_status()
except Exception as e:
    eem.action_syslog(
        'Error posting message to Spark: {}'.format(e), priority='3')
    sys.exit(1)
