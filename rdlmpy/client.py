#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

import requests
import json
from rdlmpy.exceptions import RDLMLockWaitExceededException, RDLMLockDeletedException, RDLMLockServerException
from rdlmpy.lock import RDLMLock

class RDLMClient(object):
    '''
    Class which defines a client object
    '''

    _base_url = None
    _default_title = None
    _default_lifetime = None
    _default_wait = None

    def __init__(self, server="localhost", port=8888, default_title=None, default_lifetime=300, default_wait=10):
        '''
        @summary: constructor
        @param server: rdlm server hostname
        @param port: rdlm server port
        @param default_title: default title for locks
        @param default_lifetime: default lifetime for locks (in seconds)
        @param default_wait: default wait time for locks (in seconds)
        @result: client object
        '''
        self._base_url = "http://%s:%i" % (server, port)
        self._default_title = default_title
        self._default_lifetime = default_lifetime
        self._default_wait = default_wait

    def lock_acquire(self, resource_name, lifetime=None, wait=None, title=None):
        '''
        @summary: acquires a lock
        @param resource_name: name of the resource to lock
        @param lifetime: lifetime for the lock (in seconds)
        @param wait: wait time for the lock (in seconds)
        @param title: title
        @result: lock object (if the lock is acquired)

        If the lock is not acquired, this function can raise :
        - a RDLMLockWaitExceededException: can't acquire the lock after "wait" seconds
        - a RDLMLockDeletedException: the request has been deleted by an admin request
        - a RDLMLockServerException: unknown error from the RDLM server
        '''
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
        '''
        @summary: releases a lock
        @param lock: the lock object to release
        @result: True (if ok), False (else)

        The lock object is the return value of lock_acquire() method
        '''
        r = requests.delete(lock.url)
        return (r.status_code == 204)
