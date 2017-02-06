#!/usr/bin/env python
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
# This script prints inventory stats from APIC-EM including device families,
# total devices in each family, device models, and number of different
# software revisions per model.
#

import requests
from requests import Request, Session
import argparse
import re
import sys
import time
import json
import operator

DEBUG = False
REST_TIMEOUT = 300
REST_RETRY_INTERVAL = 1
REST_RETRIES = 3
REST_PAGE_LIMIT = 500


class RestError:
    code = -1
    msg = ""

    def set_code(self, code):
        self.code = code

    def set_msg(self, msg):
        self.msg = msg

    def get_code(self):
        return self.code

    def get_msg(self):
        return self.msg


def fetch_url(url, error, p=False, timeout=REST_TIMEOUT):
    global DEBUG

    s = Session()
    requests.packages.urllib3.disable_warnings()
    req = 'GET'
    data = {}
    headers = {}
    params = {}

    if 'get' in p:
        params = p['get']
    if 'post' in p:
        req = 'POST'
        data = p['post']
    if 'put' in p:
        req = 'PUT'
        if 'header' not in p:
            p['header'] = {}
        p['header']['Content-Length'] = len(p['put'])
        data = p['put']
    if 'header' in p:
        headers = p['header']

    req = Request(req, url, data=data, params=params, headers=headers)
    ph = req.prepare()

    if DEBUG:
        print('DEBUG: Requested URL {}'.format(url))
        print('DEBUG:  Headers = ')
        for h in ph.headers:
            print('  {} : {}'.format(h, ph.headers[h]))
        print('DEBUG:  Parameters = ')
        for par, val in params.items():
            print('  {} : {}'.format(par, val))
        print('DEBUG: Body    = {}'.format(ph.body))

    res = s.send(ph, verify=False, timeout=timeout)

    if res.status_code > 299:
        if DEBUG:
            print('DEBUG: The server returned code: {} response: {}'.format(
                str(res.status_code), res.text))
            print('DEBUG: Response Headers: ')
            for h in res.headers:
                print('  {} : {}'.format(h, res.headers[h]))
        error.set_code(res.status_code)
        j = res.json()
        error.set_msg(j['response']['message'])
        return None
    else:
        return res.text


def get_device_count(host, port, ticket, error):
    global REST_RETRIES, REST_RETRY_INTERVAL

    url = 'https://{}:{}/api/v1/network-device/count'.format(host, port)
    p = {}
    p['header'] = {"X-Auth-Token": ticket}

    i = 0
    res = None
    while i < REST_RETRIES:
        res = fetch_url(url, error, p)
        if res is not None:
            break
        time.sleep(REST_RETRY_INTERVAL)
        i = i + 1
    if res is not None:
        j = json.loads(res)
        return j['response']

    return None


def get_ticket(host, port, user, password, error):
    global REST_RETRIES, REST_RETRY_INTERVAL

    url = 'https://{}:{}/api/v1/ticket'.format(host, port)
    p = {}

    p['post'] = json.dumps({"username": user, "password": password})
    p['header'] = {"Content-Type": "application/json"}

    i = 0
    res = None
    while i < REST_RETRIES:
        res = fetch_url(url, error, p)
        if res is not None:
            break
        time.sleep(REST_RETRY_INTERVAL)
        i = i + 1
    if res is not None:
        j = json.loads(res)
        return j['response']['serviceTicket']

    return None


def get_inventory(host, port, ticket, error):
    global REST_RETRIES, REST_RETRY_INTERVAL, REST_PAGE_LIMIT

    url = 'https://{}:{}/api/v1/network-device'.format(host, port)
    p = {}

    p['header'] = {"X-Auth-Token": ticket}

    count = get_device_count(host, port, ticket, error)
    if count is None:
        return None

    offset = 1
    limit = REST_PAGE_LIMIT
    p['get'] = {}
    devs = []
    while True:
        p['get']['offset'] = offset
        p['get']['limit'] = limit

        i = 0
        res = None
        while i < REST_RETRIES:
            res = fetch_url(url, error, p)
            if res is not None:
                break
            time.sleep(REST_RETRY_INTERVAL)
            i = i + 1
        if res is not None:
            j = json.loads(res)
            devs += j['response']

        offset += limit
        if offset >= count:
            break

    return devs


if __name__ == '__main__':
    error = RestError()
    families = {}
    models = {}

    parser = argparse.ArgumentParser(
        prog=sys.argv[0], description='Print inventory stats from APIC-EM')
    parser.add_argument('--hostname', '-a', type=str,
                        help='APIC-EM hostname or IP address', required=True)
    parser.add_argument('--username', '-u', type=str,
                        help='APIC-EM API username', required=True)
    parser.add_argument('--password', '-p', type=str,
                        help='APIC-EM API password', required=True)
    parser.add_argument('--port', '-P', type=int,
                        help='APIC-EM web port (default: 443)')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Enable debugging (default: False)')
    parser.set_defaults(debug=False, port=443)
    args = parser.parse_args()

    if args.debug:
        DEBUG = args.debug

    ticket = get_ticket(args.hostname, args.port,
                        args.username, args.password, error)
    if ticket is None:
        print('Error obtaining RBAC ticket from APIC-EM: {}'.format(error.get_msg()))
        sys.exit(1)

    inventory = get_inventory(args.hostname, args.port, ticket, error)
    if inventory is None:
        print('Error obtaining inventory from APIC-EM: {}'.format(error.get_msg()))
        sys.exit(1)

    for dev in inventory:
        if dev['family'] not in families:
            families[dev['family']] = {}

        if dev['platformId'] not in families[dev['family']]:
            families[dev['family']][dev['platformId']] = {}

        if dev['softwareVersion'] not in families[dev['family']][dev['platformId']]:
            families[dev['family']][dev['platformId']][
                dev['softwareVersion']] = 1
        else:
            families[dev['family']][dev['platformId']][
                dev['softwareVersion']] += 1

    fam_sort = sorted(families.items(), key=operator.itemgetter(0))
    for fams in fam_sort:
        family = fams[0]
        model = fams[1]
        total = 0
        mod_sort = sorted(model.items(), key=lambda x: sum(x[1].values()))
        for m in model.values():
            total += sum(m.values())
        print('{} (total: {})'.format(family, total))
        for mods in mod_sort:
            m = mods[0]
            c = mods[1]
            print(' {} (total: {})'.format(m, sum(c.values())))

            c_sort = sorted(
                c.items(), key=operator.itemgetter(1), reverse=True)
            for revs in c_sort:
                code = revs[0]
                count = revs[1]
                print('  {} (total: {})'.format(code, count))
        print('')
