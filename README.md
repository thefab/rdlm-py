# rdlm-py

## Status (master branch)

[![Build Status](https://travis-ci.org/thefab/rdlm-py.png)](https://travis-ci.org/thefab/rdlm-py)

## What is it ?

`rdlm-py` is a python client for the [restful-distributed-lock-manager (RDLM)](https://github.com/thefab/restful-distributed-lock-manager).

## Special features

- Classic and administrative (password protected) requests
- Two ways to use it (a classical API and a (more pythonic) ContextManager API)

## Warning

`rdlm-py` is at an early stage of development (API can change).

## Quickstart

### Installation

    pip install rdlm-py

    Requirements: 
    - Python 2.6, 2.7, 3.2 or 3.3
    - Requests >= 1.2.3

## Three ways to use it 

### Classic API

    # Import the Classic client class
    from rdlmpy import RDLMClient
    from rdlmpy import RDLMException

    # Make a client object with some default parameters
    client = RDLMClient(server="localhost", port=8888, default_title="classic example", default_lifetime=300, default_wait=10)

    # Acquire a lock on resource : foo
    lock_url = client.lock_acquire("foo")

    # We have the lock on resource : foo
    # [...]

    # Try to acquire the same lock another time with a overrided wait timeout of 3 seconds
    # => RDLMException 
    try:
        lock_url2 = client.lock_acquire("foo", wait=3)
    except RDLMException:
        print "Can't acquire the lock"

    # Release the lock
    result = client.lock_release(lock_url)
    if not(result):
        print "Can't release the lock"

### Context Manager API

    # Import the Context Manager class class
    from rdlmpy import RDLMContextManager

    with RDLMContextManager("foo") as c:
        # We have the lock on resource: foo
        # [...]
        # No need to release the lock, even if an exception is raised

    # Here, we don't have the lock anymore
    # [...]

### CLI tools

Two CLI tools are available :

- `lock-acquire.py`: acquire a lock 
- `lock-release.py`: release a lock

Example in a shell script :

    #!/bin/bash

    LOCK_URL=`lock-acquire.py foo`
    if test $? -ne 0; then
        exit 1
    fi

    [...] 

    lock-release.py ${LOCK_URL}

Full manual (`lock-acquire.py`) :

    usage: lock-acquire.py [-h] [-H HOSTNAME] [-p PORT] [-t TIMEOUT] [-w WAIT]
                        resource_name

    Acquire a lock

    positional arguments:
    resource_name         Resource Name

    optional arguments:
    -h, --help            show this help message and exit
    -H HOSTNAME, --hostname HOSTNAME
                        rdlm server hostname
    -p PORT, --port PORT  rdlm server port
    -t TIMEOUT, --timeout TIMEOUT
                        timeout of the lock if acquired and not released
                        (seconds)
    -w WAIT, --wait WAIT  max number of seconds to wait for the lock

Full manual (`lock-release.py`) :

    usage: lock-release.py [-h] lock_url

    Release a lock

    positional arguments:
    lock_url    Lock Url (returned by lock-acquire.py)

    optional arguments:
    -h, --help  show this help message and exit
