#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

class RDLMLock(object):
    '''
    Class which defines a lock object
    '''

    url = None

    def __init__(self, url):
        '''
        @summary: constructor
        @param url: url of the lock
        @result: lock object
        '''
        self.url = url
