#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

class RDLMException(Exception):
    pass

class RDLMLockWaitExceededException(RDLMException):
    pass

class RDLMLockDeletedException(RDLMException):
    pass

class RDLMLockServerException(RDLMException):
    pass
