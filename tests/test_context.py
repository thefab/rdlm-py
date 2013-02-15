import unittest
from rdlmpy import RDLMContextManager
from httpretty import HTTPretty, httprettified
from rdlmpy import RDLMLockWaitExceededException

class SpecialException(Exception):

    pass

class TestContext(unittest.TestCase):

    context = None
    server = "localhost"
    port = 8888
    baseurl = None
    resource = "foo"

    def setUp(self):
        self.context = RDLMContextManager(self.resource, server=self.server, port=self.port)
        self.baseurl = "http://%s:%i" % (self.server, self.port)
        self.assertFalse(self.context is None)

    def tearDown(self):
        pass

    @httprettified
    def test_enterexit(self):
        url = "%s/locks/%s" % (self.baseurl, self.resource)
        lock_url = "%s/ff14608f6ab342f0bb2a86d551d42a8c" % url
        HTTPretty.register_uri(HTTPretty.POST, url, status=201, location=lock_url)
        HTTPretty.register_uri(HTTPretty.DELETE, lock_url, status=204)
        result = False
        with self.context as c:
            self.assertFalse(c is None)
            result = True
        self.assertTrue(result)

    @httprettified
    def test_enterexit408(self):
        url = "%s/locks/%s" % (self.baseurl, self.resource)
        HTTPretty.register_uri(HTTPretty.POST, url, status=408)
        try:
            with self.context as c:
                raise Exception("no exception raised")
        except RDLMLockWaitExceededException:
            pass

    @httprettified
    def test_enterexit_exception(self):
        def _delete_callback(method, uri, headers):
            self.delete_flag = True
            return "coucou"
        self.delete_flag = False
        url = "%s/locks/%s" % (self.baseurl, self.resource)
        lock_url = "%s/ff14608f6ab342f0bb2a86d551d42a8c" % url
        HTTPretty.register_uri(HTTPretty.POST, url, status=201, location=lock_url)
        HTTPretty.register_uri(HTTPretty.DELETE, lock_url, body=_delete_callback, status=204)
        try:
            with self.context as c:
                raise SpecialException("no exception raised")
        except SpecialException:
            pass
        self.assertTrue(self.delete_flag)

if __name__ == '__main__':
    unittest.main()
