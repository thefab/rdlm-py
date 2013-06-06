#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

import requests
import socket
import getpass
import os
import sys
from requests.auth import HTTPBasicAuth
import json
from rdlmpy.lock import RDLMLock
from rdlmpy.exceptions import RDLMLockWaitExceededException
from rdlmpy.exceptions import RDLMLockDeletedException
from rdlmpy.exceptions import RDLMServerException
from rdlmpy.exceptions import RDLMClientException
from rdlmpy import __version__ as VERSION


class RDLMClient(object):
    '''
    Class which defines a client object
    '''

    _base_url = None
    _default_title = None
    _default_lifetime = None
    _default_wait = None

    def __init__(self, server="localhost", port=8888, default_title=None,
                 default_lifetime=300, default_wait=10):
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
        if default_title:
            self._default_title = default_title
        else:
            self._default_title = "%s#%i(%s) with RDLMClient(%s) @%s" % (
                                  getpass.getuser(), os.getpid(), sys.argv[0],
                                  VERSION, socket.gethostname())
        self._default_lifetime = default_lifetime
        self._default_wait = default_wait

    def lock_acquire(self, resource_name, lifetime=None, wait=None,
                     title=None):
        '''
        @summary: acquires a lock
        @param resource_name: name of the resource to lock
        @param lifetime: lifetime for the lock (in seconds)
        @param wait: wait time for the lock (in seconds)
        @param title: title
        @result: lock url (if the lock is acquired)

        If the lock is not acquired, this function can raise :
        - a RDLMLockWaitExceededException: can't acquire the lock after
          "wait" seconds
        - a RDLMLockDeletedException: the request has been deleted by
          an delete request
        - a RDLMServerException: unknown error from the RDLM server
        - a RDLMClientException: unknown error from the RDLM client
        '''
        lock_dict = {}
        lock_dict['lifetime'] = self._default_lifetime \
            if lifetime is None else lifetime
        lock_dict['wait'] = self._default_wait if wait is None else wait
        lock_dict['title'] = self._default_title if title is None else title
        lock_raw = json.dumps(lock_dict)
        try:
            r = requests.post("%s/locks/%s" % (self._base_url, resource_name), data=lock_raw)
        except:
            raise RDLMServerException()
        if r.status_code == 408:
            raise RDLMLockWaitExceededException()
        elif r.status_code == 409:
            raise RDLMLockDeletedException()
        elif r.status_code >= 400 and r.status_code < 500:
            raise RDLMClientException()
        elif r.status_code != 201 or not(r.headers['Location'].startswith('http://')):
            raise RDLMServerException()
        return r.headers['Location']

    def lock_release(self, lock_url):
        '''
        @summary: releases a lock
        @param lock_url: the lock url to release
        @result: True (if ok), False (else)

        The lock url is the return value of lock_acquire() method
        '''
        try:
            r = requests.delete(lock_url)
        except:
            raise RDLMServerException()
        return (r.status_code == 204)

    def lock_get(self, lock_url):
        '''
        @summary: gets informations about a lock
        @param lock_url: the lock url
        @result: informations dict (or None)
        '''
        try:
            r = requests.get(lock_url)
        except:
            raise RDLMServerException()
        if r.status_code == 200:
            return RDLMLock.factory(lock_url, r.content.decode('utf-8'))
        return None

    def resource_delete(self, resource_name, username=None, password=None):
        '''
        @summary: delete all locks on a resource
        @param resource_name: name of the resource
        @param username: admin http username
        @param password: admin http password
        @result: True if there were some locks on the resource, False else
        '''
        if username and password:
            auth = HTTPBasicAuth(username, password)
            r = requests.delete("%s/resources/%s" % (self._base_url, resource_name), auth=auth)
        else:
            r = requests.delete("%s/resources/%s" % (self._base_url, resource_name))
        return (r.status_code == 204)

    def resource_delete_all(self, username=None, password=None):
        '''
        @summary: delete all locks on all resources
        @param username: admin http username
        @param password: admin http password
        @result: True if ok, False else
        '''
        if username and password:
            auth = HTTPBasicAuth(username, password)
            r = requests.delete("%s/resources" % self._base_url, auth=auth)
        else:
            r = requests.delete("%s/resources" % self._base_url)
        return (r.status_code == 204)

    def resource_get_all(self, username=None, password=None):
        '''
        @summary: get resources list (with locks)
        @param username: admin http username
        @param password: admin http password
        @result: list of resource names
        '''
        if username and password:
            auth = HTTPBasicAuth(username, password)
            r = requests.get("%s/resources" % self._base_url, auth=auth)
        else:
            r = requests.get("%s/resources" % self._base_url)
        if r.status_code != 200:
            raise RDLMServerException("Impossible to get all resources\
                                      (unknown error")
        try:
            json_hal = json.loads(r.content)
        except:
            raise RDLMServerException("Impossible to get all resources\
                                      (can't unserialize result")
        if '_embedded' not in json_hal or \
           'resources' not in json_hal['_embedded']:
            return []
        return [x['name'] for x in json_hal['_embedded']['resources']]

    def resource_get_all_locks(self, resource_name, username=None, password=None):
        '''
        @summary: get locks list for a given resource
        @param resource_name: name of the resource
        @param username: admin http username
        @param password: admin http password
        @result: list of lock objects
        '''
        if username and password:
            auth = HTTPBasicAuth(username, password)
            r = requests.get("%s/resources/%s" % (self._base_url, resource_name), auth=auth)
        else:
            r = requests.get("%s/resources/%s" % (self._base_url, resource_name))
        if r.status_code != 200:
            raise RDLMServerException("Impossible to get all locks\
                                      (unknown error")
        try:
            json_hal = json.loads(r.content.decode('utf-8'))
        except:
            raise RDLMServerException("Impossible to get all locks\
                                      (can't unserialize result")
        if '_embedded' not in json_hal or \
           'locks' not in json_hal['_embedded']:
            return []
        out = []
        for x in json_hal['_embedded']['locks']:
            lock_url = "%s%s" % (self._base_url, x['_links']['self']['href'])
            out.append(RDLMLock.factory(lock_url, json.dumps(x)))
        return out
