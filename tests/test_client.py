import unittest
from rdlmpy import RDLMClient
from httpretty import HTTPretty, httprettified

class TestClient(unittest.TestCase):

    client = None
    server = "localhost"
    port = 8888
    baseurl = None
    resource = "foo"

    def setUp(self):
        self.baseurl = "http://%s:%i" % (self.server, self.port)
        self.client = RDLMClient(server=self.server, port=self.port)
        self.assertFalse(self.client is None)

    def tearDown(self):
        pass

    def _make_lock_object(self):
        url = "%s/locks/%s" % (self.baseurl, self.resource)
        lock_url = "%s/ff14608f6ab342f0bb2a86d551d42a8c" % url
        HTTPretty.register_uri(HTTPretty.POST, url, status=201, location=lock_url)
        r = self.client.lock_acquire(self.resource)
        self.assertFalse(r is None)
        return (r, lock_url)

    @httprettified
    def test_acquire(self):
        (lock, lock_url) = self._make_lock_object()
        self.assertEqual(lock.url, lock_url)

    @httprettified
    def test_release(self):
        (lock, lock_url) = self._make_lock_object()
        self.assertEqual(lock.url, lock_url)
        HTTPretty.register_uri(HTTPretty.DELETE, lock_url, status=204)
        f = self.client.lock_release(lock)
        self.assertTrue(f)

if __name__ == '__main__':
    unittest.main()
