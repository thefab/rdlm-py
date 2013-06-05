#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

import argparse
from rdlmpy import RDLMClient

parser = argparse.ArgumentParser(description='List all resources (with locks)')
parser.add_argument("-H", "--hostname", type=str, help="rdlm server hostname", default="localhost")
parser.add_argument("-p", "--port", type=int, help="rdlm server port", default=8888)
parser.add_argument("-u", "--username", type=str, help="Administrative username", default=None)
parser.add_argument("-P", "--password", type=str, help="Administrative password", default=None)
parser.add_argument("resource_name", type=str, help="Resource Name")
args = parser.parse_args()

client = RDLMClient(server=args.hostname, port=args.port)

locks = client.resource_get_all_locks(args.resource_name, username=args.username,
                                      password=args.password)
for lock in locks:
    if lock.active:
        print "active: %s since %s [%s]" % (lock.url, lock.active_since, lock.title)
    else:
        print "waiting: %s since %s [%s]" % (lock.url, lock.wait_since, lock.title)
