#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

import argparse
import sys
from rdlmpy import RDLMClient
from urlparse import urlparse

parser = argparse.ArgumentParser(description='Get some informations about a lock')
parser.add_argument("lock_url", type=str, help="Lock Url (returned by lock-acquire.py)")
args = parser.parse_args()

url_parsed = urlparse(args.lock_url)
netloc = url_parsed.netloc
netloc_splitted = netloc.split(":")
hostname = netloc_splitted[0]
if len(netloc_splitted) == 1:
    port = 80
else:
    port = int(netloc_splitted[1])

client = RDLMClient(server=hostname, port=port)
return_code = 3
lock = client.lock_get(args.lock_url)
if lock:
    print "url:            %s" % lock.url
    print "timeout:        %s (seconds)" % lock.lifetime
    print "wait:           %s (seconds)" % lock.wait
    print "title:          %s" % lock.title
    if lock.active:
        print "state:          active"
        print "active_since:   %s" % lock.active_since
        print "active_expires: %s" % lock.active_expires
    else:
        print "state:          waiting"
        print "wait_since:     %s" % lock.wait_since
        print "wait_expires:   %s" % lock.wait_expires
    return_code = 0
else:
    sys.stderr.write("Can't find the lock\n")
    return_code = 1

sys.exit(return_code)
