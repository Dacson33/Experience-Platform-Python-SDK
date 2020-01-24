import unittest

from API import API

api = API()


class TestSDK(unittest.TestCase):

    def test_id_validation(self):
        self.assertTrue(api.validate(api.dID))
        self.assertFalse(api.validate("dijf0fhjw0hf0w"))

    def test_upload(self):
        self.assertIsNotNone(api.upload('test128.json', api.dID))
        self.assertIsNotNone(api.upload('test256.json', api.dID))
        self.assertIsNotNone(api.upload('test500.json', api.dID))

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()