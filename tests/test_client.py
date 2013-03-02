import unittest
from rdlmpy import RDLMClient
from rdlmpy import RDLMLockWaitExceededException, RDLMLockDeletedException, RDLMServerException
from httpretty import HTTPretty, httprettified
import base64
import os

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
        (lock_u, lock_url) = self._make_lock_object()
        self.assertEqual(lock_u, lock_url)

    @httprettified
    def _test_acquire_exception(self, status_code, exception):
        url = "%s/locks/%s" % (self.baseurl, self.resource)
        if status_code == 201:
            lock_url = "%s/ff14608f6ab342f0bb2a86d551d42a8c" % url
            HTTPretty.register_uri(HTTPretty.POST, url, status=status_code, location=lock_url)
        else:
            HTTPretty.register_uri(HTTPretty.POST, url, status=status_code)
        try:
            self.client.lock_acquire(self.resource)
            raise Exception("no exception raised")
        except exception:
            pass

    @httprettified
    def test_acquire_408(self):
        self._test_acquire_exception(408, RDLMLockWaitExceededException)

    @httprettified
    def test_acquire_500(self):
        self._test_acquire_exception(500, RDLMServerException)

    @httprettified
    def test_acquire_409(self):
        self._test_acquire_exception(409, RDLMLockDeletedException)

    @httprettified
    def test_release(self):
        (lock_u, lock_url) = self._make_lock_object()
        self.assertEqual(lock_u, lock_url)
        HTTPretty.register_uri(HTTPretty.DELETE, lock_url, status=204)
        f = self.client.lock_release(lock_url)
        self.assertTrue(f)

    @httprettified
    def test_delete_all_resources(self):
        HTTPretty.register_uri(HTTPretty.DELETE, "%s/resources" % self.baseurl, status=401)
        f = self.client.resource_delete_all()
        self.assertFalse(f)
        self.assertFalse('Authorization' in HTTPretty.last_request.headers)
        HTTPretty.register_uri(HTTPretty.DELETE, "%s/resources" % self.baseurl, status=204)
        f = self.client.resource_delete_all("foo", "bar")
        self.assertTrue(f)
        self.assertTrue('Authorization' in HTTPretty.last_request.headers)
        b64 = base64.standard_b64encode(b"foo:bar")
        expected = b"Basic " + b64
        self.assertEqual(HTTPretty.last_request.headers['Authorization'].encode('ascii'), expected)

    @httprettified
    def test_delete_resource(self):
        HTTPretty.register_uri(HTTPretty.DELETE, "%s/resources/foo" % self.baseurl, status=401)
        f = self.client.resource_delete("foo")
        self.assertFalse(f)
        self.assertFalse('Authorization' in HTTPretty.last_request.headers)
        HTTPretty.register_uri(HTTPretty.DELETE, "%s/resources/foo" % self.baseurl, status=204)
        f = self.client.resource_delete("foo", username="foo", password="bar")
        self.assertTrue(f)
        self.assertTrue('Authorization' in HTTPretty.last_request.headers)
        b64 = base64.standard_b64encode(b"foo:bar")
        expected = b"Basic " + b64
        self.assertEqual(HTTPretty.last_request.headers['Authorization'].encode('ascii'), expected)

    @httprettified
    def test_get(self):
        lock_url = "%s/locks/foo/94e4458bad8248828213275ae0b17eae" % self.baseurl
        HTTPretty.register_uri(HTTPretty.GET, lock_url, status=404)
        f = self.client.lock_get(lock_url)
        self.assertTrue(f is None)
        json_file = os.path.join(os.path.dirname(__file__), "lock1.json")
        with open(json_file, "r") as f:
            body = f.read()
        HTTPretty.register_uri(HTTPretty.GET, lock_url, status=200, body=body)
        f = self.client.lock_get(lock_url)
        self.assertFalse(f is None)
        self.assertTrue(f.active)
        self.assertEqual(f.title, "test title")
        self.assertEqual(f.uid, "94e4458bad8248828213275ae0b17eae")
        self.assertEqual(f.lifetime, 300)
        self.assertEqual(f.wait, 10)
        self.assertEqual(f.active_since.isoformat(), "2013-03-02T22:00:05")
        self.assertEqual(f.active_expires.isoformat(), "2013-03-02T22:05:05")

if __name__ == '__main__':
    unittest.main()
