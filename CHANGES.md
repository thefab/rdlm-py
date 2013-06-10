# CHANGES

## Release 0.2.0 (beta)

- doc update

## Release 0.1.b1 (beta)

- add `resource_get_all()` and `resource_get_all_locks()` methods
- add three new cli tools to interact with the RDLM server
- little bugfixes and typo

## Release 0.1a6 (alpha)

- doc update

## Release 0.1a5 (alpha)

- introduce a `RDLMContextManagerFactory`object
- introduce two cli tools to interact with the RDLM server
- upgrade requirements
- typos and styles fixes

## Release 0.1a4 (alpha)

- `lock_acquire()` can return an RDLMClientException
- `RDLMLockServerException` is renamed to `RDLMServerException`

## Release 0.1a3 (alpha)

- light refactoring
- new methods :
    - `lock_get()`
    - `lock_resource_delete()`
    - `lock_resource_delete_all()`

## Release 0.1a2 (alpha)

- `lock_acquire()` returns an URL as string (and not as an `RDLMLock` object)
- `lock_release()` takes a lock URL as string (and not as an `RDLMLocki` object)

## Release 0.1a1 (alpha)

- first release
