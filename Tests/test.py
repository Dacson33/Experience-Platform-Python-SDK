import unittest

from API import API
from ParameterClasses.AuthToken import AuthToken

class TestSDK(unittest.TestCase):

    testUpload128 = False
    testUpload256 = False
    testUpload500 = False
    testUploadError = False

    def setUp(self):
        self.api = API('config.json')

    def testBadAuth(self):
        self.api.accessToken = AuthToken("eyJ4NXUiOiJpbXNfbmExLWtleS0xLmNlciIsImFsZyI6IlJTMjU2In0.eyJpZCI6IjE1ODA3NTU5MzM0OTFfNTM3ZDZiYWQtNmJjOS00YWFjLWEwZTktMDEzM2YyOTFiNzYxX3VlMSIsImNsaWVudF9pZCI6ImQ4YjY1Y2E3NWVlNDRiOGNhOWJmODdiNmZkYzBhMTc0IiwidXNlcl9pZCI6IkQ5Q0I3OEEyNURBRTE0QkMwQTQ5NUMyMUB0ZWNoYWNjdC5hZG9iZS5jb20iLCJzdGF0ZSI6IntcInNlc3Npb25cIjpcImh0dHBzOi8vaW1zLW5hMS5hZG9iZWxvZ2luLmNvbS9pbXMvc2Vzc2lvbi92MS9aakExT1daak1Ea3RabU5tWmkwME1qTTFMV0V5WkRRdFlqUmlNREV3TnpOalpXTTBMUzFFT1VOQ056aEJNalZFUVVVeE5FSkRNRUUwT1RWRE1qRkFkR1ZqYUdGalkzUXVZV1J2WW1VdVkyOXRcIn0iLCJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiYXMiOiJpbXMtbmExIiwiZmciOiJVRkFLWUpFMkhQRTVKUFVQRzZBTFlQUUFEVT09PT09PSIsIm1vaSI6IjU0YmVlZjg3IiwiYyI6IlRrZnhXK3dwRStzZk9TbGc1RlZITlE9PSIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsInNjb3BlIjoib3BlbmlkLHNlc3Npb24sQWRvYmVJRCxyZWFkX29yZ2FuaXphdGlvbnMsYWRkaXRpb25hbF9pbmZvLnByb2plY3RlZFByb2R1Y3RDb250ZXh0IiwiY3JlYXRlZF9hdCI6IjE1ODA3NTU5MzM0OTEifQ.psJCN3iFkzMx9bgkQBB4cDBHzvuHK6eLT146iw1z-89kf0m0iPqshJuX3ddToUWp3hXEbZWkr9Ta1BezbjTvSnpgtYbNFAs4M2mYnVHpzqCgJQxI41JzQKHAqj94_dHNJIWvHJERnME1L9dX0DHSmFSTSZVwOUZWT7HFdZg-2wPTG4wY3VRVmiwVmmW3lQAJ5aL6N7O1rWUqEEb9tXHM9UJSKeFTdlsmyAX_MV9TK9-zB5kDpkhMK41rQiwUVWzCkB1gawJPutweGv5GiUieOOlwLz0GfD5oH5aoA8FYXt9_hFziQPP55yVoxbYWuOPFMiqRBWmL_zbne8D4Kn7Uwg", "07907987979", "0")
        self.assertFalse(self.api.validate(self.api.dID))

    def testBadConfig(self):
        self.assertFalse(self.api.initConfig('badConfig.json'))

    def test_id_validation(self):
        self.assertTrue(self.api.validate(self.api.dID))
        self.assertFalse(self.api.validate("dijf0fhjw0hf0w"))
        self.assertFalse(self.api.validate(""))

    @unittest.skipUnless(testUpload128, "Skip if false")
    def test_upload_128(self):
        self.assertEquals(self.api.upload('test128.json', self.api.dID), "success")

    @unittest.skipUnless(testUpload256, "Skip if false")
    def test_upload_256(self):
        self.assertEquals(self.api.upload('test256.json', self.api.dID), "success")

    @unittest.skipUnless(testUpload500, "Skip if false")
    def test_upload_large(self):
        self.assertEquals(self.api.upload('test500.json', self.api.dID), "success")

if __name__ == '__main__':
    unittest.main()