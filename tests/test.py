import app
import os
import unittest

from query import *

class TestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_home(self):
        # Checks content of application root page
        res = self.app.get('/')
        self.assertEqual(200, res.status_code)
        types = res.headers['content-type']
        #  data = res.data.decode('utf-8')
        self.assertIn('text/html', types)

    def test_quote(self):
        # Checks the /quote/ endpoint
        res = self.app.get('/quote/')
        self.assertEqual(200, res.status_code)
        types = res.headers['content-type']
        self.assertIn('application/json', types)
        data = res.json
        self.assertTrue(len(data['quotes']) != 0)
        self.assertTrue(len(data['quotes'][0]['author']) != 0)

    def test_quote_args(self):
        # Checks the args for the /quote/endpoint arguments
        res = self.app.get(f'/quote/?num={0}')
        data = res.json
        self.assertEqual(200, res.status_code)
        self.assertTrue(len(data['quotes']) == 0)
        num = random.randint(1, quote_amount())
        res = self.app.get(f'/quote/?num={num}')
        data = res.json
        self.assertEqual(200, res.status_code)
        self.assertTrue(len(data['quotes']) == num)

    def test_quote_id(self):
        res = self.app.get('/quote/0')
        self.assertEqual(200, res.status_code)
    def test_author_id(self):
        res = self.app.get('/quote/author/0')
        self.assertEqual(200, res.status_code)


if __name__ == '__main__':
    unittest.main()
