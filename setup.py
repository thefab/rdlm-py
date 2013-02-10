#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of rdlm-py released under the MIT license.
# See the LICENSE file for more information.

from setuptools import setup, find_packages
import rdlmpy

DESCRIPTION = "rdlm-py is a python client for RDLM (Restful Distributed Lock Manager)"
try:
    with open('README.rst') as f:
        LONG_DESCRIPTION = f.read()
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name='rdlm-py',
    version=rdlmpy.__version__,
    author="Fabien MARTY",
    author_email="fabien.marty@gmail.com",
    url="https://github.com/thefab/rdlm-py",
    packages=find_packages(),
    license='MIT',
    download_url='https://github.com/thefab/rdlm-py',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=[
        'requests >= 1.0.0'
    ],
    classifiers=[
        'Development Status :: 5 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',  
        'Programming Language :: Python :: 3',  
        'Topic :: Utilities',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development',
      ]
)
