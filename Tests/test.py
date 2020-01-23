import unittest

from API import API


class TestSDK(unittest.TestCase):

    def test_id_validation(self):
        api = API()
        self.assertFalse(api.validate(api.datasetIds, "dijf0fhjw0hf0w"))

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