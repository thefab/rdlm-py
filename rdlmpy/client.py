#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

import requests
import json
from rdlmpy.exceptions import RDLMLockWaitExceededException, RDLMLockDeletedException
from rdlmpy.lock import RDLMLock

class RDLMClient(object):

    _base_url = None
    _default_title = None
    _default_lifetime = None
    _default_wait = None

    def __init__(self, server="localhost", port=8888, default_title=None, default_lifetime=300, default_wait=10):
        self._base_url = "http://%s:%i" % (server, port)
        self._default_title = default_title
        self._default_lifetime = default_lifetime
        self._default_wait = default_wait

    def lock_acquire(self, resource_name, lifetime=None, wait=None, title=None):
        lock_dict = {}
        lock_dict['lifetime'] = self._default_lifetime if lifetime is None else lifetime
        lock_dict['wait'] = self._default_wait if wait is None else wait
        lock_dict['title'] = self._default_title if title is None else title
        lock_raw = json.dumps(lock_dict)
        r = requests.post("%s/locks/%s" % (self._base_url, resource_name), data=lock_raw)
        if r.status_code == 408:
            raise RDLMLockWaitExceededException()
        elif r.status_code == 409:
            raise RDLMLockDeletedException()
        elif r.status_code != 201 or not(r.headers['Location'].startswith('http://')):
            raise RDLMLockServerException()
        return RDLMLock(url=r.headers['Location'])

    def lock_release(self, lock):
        r = requests.delete(lock.url)
        return (r.status_code == 204)

    def lock_info(self, lock):
        pass
