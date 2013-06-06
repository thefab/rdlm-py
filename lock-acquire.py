#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

import argparse
import sys
from rdlmpy import RDLMClient
from rdlmpy import RDLMLockWaitExceededException, RDLMLockDeletedException

parser = argparse.ArgumentParser(description='Acquire a lock')
parser.add_argument("-H", "--hostname", type=str, help="rdlm server hostname", default="localhost")
parser.add_argument("-p", "--port", type=int, help="rdlm server port", default=8888)
parser.add_argument("-t", "--timeout", type=int,
                    help="timeout of the lock if acquired\
                          and not released (seconds)", default=300)
parser.add_argument("-w", "--wait", type=int,
                    help="max number of seconds\
                    to wait for the lock", default=10)
parser.add_argument("resource_name", type=str, help="Resource Name")
args = parser.parse_args()

client = RDLMClient(server=args.hostname, port=args.port)
return_code = 3
try:
    lock_url = client.lock_acquire(args.resource_name, lifetime=args.timeout,
                                   wait=args.wait)
    print lock_url
    return_code = 0
except RDLMLockWaitExceededException:
    sys.stderr.write("Can't acquire the lock on %s resource in %i second(s)\n" %
                     (args.resource_name, args.wait))
    return_code = 1
except RDLMLockDeletedException:
    sys.stderr.write("The lock request has been deleted by an delete request\n")
    return_code = 2
except:
    sys.stderr.write("Unknown error\n")
sys.exit(return_code)
