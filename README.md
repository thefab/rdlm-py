# rdlm-py

## What is it ?

`rdlm-py` is a python client for the [restful-distributed-lock-manager (RDLM)](https://github.com/thefab/restful-distributed-lock-manager).

## Warning

`rdlm-py` is at an early stage of development (API can change).

## Two ways to use it 

### Classic API

    # Import the Classic client class
    from rdlmpy import RDLMClient
    from rdlmpy import RDLMException

    # Make a client object with some default parameters
    client = RDLMClient(server="localhost", port=8888, default_title="classic example", default_lifetime=300, default_wait=10)

    # Acquire a lock on resource : foo
    lock = client.lock_acquire("foo")

    # We have the lock on resource : foo
    # [...]

    # Try to acquire the same lock another time with a overrided wait timeout of 3 seconds
    # => RDLMException 
    try:
        lock2 = client.lock_acquire("foo", wait=3)
    except RDLMException:
        print "Can't acquire the lock"

    # Release the lock
    result = client.lock_release(lock)
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

