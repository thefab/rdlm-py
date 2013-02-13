#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

from rdlmpy.client import RDLMClient

class RDLMContextManager(object):
    '''
    Class which defines a ContextManager to get a convenient way to use RDLMClient with 
    the "with" statement
    '''

    __client = None
    __resource_name = None
    __lock = None

    def __init__(self, resource_name, server="localhost", port=8888, lifetime=300, wait=10, title=None):
        self.__client = RDLMClient(server=server, port=port, default_lifetime=lifetime, default_wait=wait, default_title=title)
        self.__resource_name = resource_name

    def __enter__(self):
        self.__lock = self.__client.lock_acquire(self.__resource_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__lock:
            self.__client.lock_release(self.__lock)
        return False
