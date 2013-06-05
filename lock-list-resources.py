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
args = parser.parse_args()

client = RDLMClient(server=args.hostname, port=args.port)

names = client.resource_get_all(args.username, args.password)
for name in names:
    print name
