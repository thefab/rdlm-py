#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

class RDLMException(Exception):
    '''
    Abstract class to represent a generic RDLM exception
    '''
    pass

class RDLMLockWaitExceededException(RDLMException):
    '''
    Exception: the lock is not acquired after wait timeout
    '''
    pass

class RDLMLockDeletedException(RDLMException):
    '''
    Exception: the lock has been deleted by an admin request
    '''
    pass

class RDLMLockServerException(RDLMException):
    '''
    Unknown exception from the RDLM server
    '''
    pass
