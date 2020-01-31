import unittest

from API import API

class TestSDK(unittest.TestCase):

    def setUp(self):
        self.api = API()

    def test_id_validation(self):
        self.assertTrue(self.api.validate(self.api.dID))
        self.assertFalse(self.api.validate("dijf0fhjw0hf0w"))

    def test_upload(self):
        self.assertIsNotNone(self.api.upload('test128.json', self.api.dID))
        self.assertIsNotNone(self.api.upload('test256.json', self.api.dID))
        self.assertIsNotNone(self.api.upload('test500.json', self.api.dID))

if __name__ == '__main__':
    unittest.main()