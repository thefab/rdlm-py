#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

class RDLMLock(object):

    url = None

    def __init__(self, url):
        self.url = url
