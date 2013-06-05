#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

import json
import datetime
from rdlmpy.exceptions import RDLMClientException


def iso8601_to_datetime(iso8601_string):
    return datetime.datetime.strptime(iso8601_string[0:19], "%Y-%m-%dT%H:%M:%S")


class RDLMLock(object):
    '''
    Class which defines a lock object
    '''

    url = None
    title = None
    uid = None
    lifetime = None
    wait = None
    active_since = None
    active_expires = None
    wait_since = None
    wait_expires = None

    def __init__(self, url):
        self.url = url

    @staticmethod
    def factory(url, get_request_output):
        res = None
        try:
            tmp = json.loads(get_request_output)
            if tmp['active']:
                res = RDLMActiveLock(url)
                res.active_since = iso8601_to_datetime(tmp['active_since'])
                res.active_expires = iso8601_to_datetime(tmp['active_expires'])
            else:
                res = RDLMWaitingLock(url)
                res.wait_since = iso8601_to_datetime(tmp['wait_since'])
                res.wait_expires = iso8601_to_datetime(tmp['wait_expires'])
            res.title = tmp['title']
            res.uid = tmp['uid']
            res.lifetime = tmp['lifetime']
            res.wait = tmp['wait']
        except:
            raise RDLMClientException("impossible to build the lock object")
        return res


class RDLMActiveLock(RDLMLock):

    @property
    def active(self):
        return True


class RDLMWaitingLock(RDLMLock):

    @property
    def active(self):
        return False
