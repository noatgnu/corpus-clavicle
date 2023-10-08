import unittest
from rest_framework.test import APIRequestFactory

class RawData(unittest.TestCase):
    def test_upload(self):
        factory = APIRequestFactory()
        request = factory.post(
            '/api/rawdata/', {'name': 'test', 'description': 'test', 'index_col': 'test', 'metadata': 'test', 'file_type': 'test'})


if __name__ == '__main__':
    unittest.main()
