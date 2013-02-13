#!/usr/bin/env python
# -*- coding: utf-8 -*-

version_info = (0, 1, 'a1')
__version__ = ".".join([str(x) for x in version_info])

from rdlmpy.client import RDLMClient
from rdlmpy.context import RDLMContextManager

__all__ = ['RDLMClient', 'RDLMContextManager']
