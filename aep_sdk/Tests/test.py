import unittest

from aep_sdk.API import API
from aep_sdk.ParameterClasses.AuthToken import AuthToken


class TestSDK(unittest.TestCase):
    testUpload128 = True
    testUpload256 = True
    testUpload500 = True
    testUploadError = True
    testMultipleFilesSuccess = True
    testMultipleFilesFailure = True
    testMultipleFilesSuccessLarge = True
    testMultipleFilesFailureLarge = True
    testUploadAll = True

    def setUp(self):
        self.api = API('config.json')
        self.dataset_id = "5e29e7e984479018a93e70a7"

    def testHelp(self):
        self.assertIsNone(help(API))

    def testBadAuth(self):
        self.api.access_token = AuthToken("eyJ4NXUiOiJpbXNfbmExLWtleS0xLmNlciIsImFsZyI6IlJTMjU2In0.eyJpZCI6IjE1ODA3NTU5"
                                          "MzM0OTFfNTM3ZDZiYWQtNmJjOS00YWFjLWEwZTktMDEzM2YyOTFiNzYxX3VlMSIsImNsaWVudF9p"
                                          "ZCI6ImQ4YjY1Y2E3NWVlNDRiOGNhOWJmODdiNmZkYzBhMTc0IiwidXNlcl9pZCI6IkQ5Q0I3OEEy"
                                          "NURBRTE0QkMwQTQ5NUMyMUB0ZWNoYWNjdC5hZG9iZS5jb20iLCJzdGF0ZSI6IntcInNlc3Npb25c"
                                          "IjpcImh0dHBzOi8vaW1zLW5hMS5hZG9iZWxvZ2luLmNvbS9pbXMvc2Vzc2lvbi92MS9aakExT1da"
                                          "ak1Ea3RabU5tWmkwME1qTTFMV0V5WkRRdFlqUmlNREV3TnpOalpXTTBMUzFFT1VOQ056aEJNalZF"
                                          "UVVVeE5FSkRNRUUwT1RWRE1qRkFkR1ZqYUdGalkzUXVZV1J2WW1VdVkyOXRcIn0iLCJ0eXBlIjoi"
                                          "YWNjZXNzX3Rva2VuIiwiYXMiOiJpbXMtbmExIiwiZmciOiJVRkFLWUpFMkhQRTVKUFVQRzZBTFlQ"
                                          "UUFEVT09PT09PSIsIm1vaSI6IjU0YmVlZjg3IiwiYyI6IlRrZnhXK3dwRStzZk9TbGc1RlZITlE9"
                                          "PSIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsInNjb3BlIjoib3BlbmlkLHNlc3Npb24sQWRvYmVJ"
                                          "RCxyZWFkX29yZ2FuaXphdGlvbnMsYWRkaXRpb25hbF9pbmZvLnByb2plY3RlZFByb2R1Y3RDb250"
                                          "ZXh0IiwiY3JlYXRlZF9hdCI6IjE1ODA3NTU5MzM0OTEifQ.psJCN3iFkzMx9bgkQBB4cDBHzvuHK"
                                          "6eLT146iw1z-89kf0m0iPqshJuX3ddToUWp3hXEbZWkr9Ta1BezbjTvSnpgtYbNFAs4M2mYnVHpz"
                                          "qCgJQxI41JzQKHAqj94_dHNJIWvHJERnME1L9dX0DHSmFSTSZVwOUZWT7HFdZg-2wPTG4wY3VRVm"
                                          "iwVmmW3lQAJ5aL6N7O1rWUqEEb9tXHM9UJSKeFTdlsmyAX_MV9TK9-zB5kDpkhMK41rQiwUVWzCk"
                                          "B1gawJPutweGv5GiUieOOlwLz0GfD5oH5aoA8FYXt9_hFziQPP55yVoxbYWuOPFMiqRBWmL_zbne"
                                          "8D4Kn7Uwg",
                                          7907987979, "0")
        self.assertFalse(self.api.validate(self.dataset_id))

    def testBadConfig(self):
        self.assertFalse(self.api.init_config('badConfig.json'))

    def test_id_validation(self):
        self.assertTrue(self.api.validate(self.dataset_id))
        self.assertFalse(self.api.validate("dijf0fhjw0hf0w"))
        self.assertFalse(self.api.validate(""))

    @unittest.skipUnless(testUpload128, "Not currently testing")
    def test_upload_128(self):
        self.assertEqual(self.api.upload(['test128.json'], self.dataset_id), "success")

    @unittest.skipUnless(testUpload256, "Not currently testing")
    def test_upload_256(self):
        self.assertEqual(self.api.upload(['test256.json'], self.dataset_id), "success")

    @unittest.skipUnless(testUpload500, "Not currently testing")
    def test_upload_large(self):
        self.assertEqual(self.api.upload(['test500.json'], self.dataset_id), "success")

    @unittest.skipUnless(testUploadError, "Not currently testing")
    def test_upload_error(self):
        self.assertEqual(self.api.upload(['testError.json'], self.dataset_id), "failure")

    @unittest.skipUnless(testMultipleFilesSuccess, "Not currently testing")
    def test_upload_multiple_success(self):
        self.assertEqual(self.api.upload(['test1.json', 'test128.json'], self.dataset_id), "success")

    @unittest.skipUnless(testMultipleFilesFailure, "Not currently testing")
    def test_upload_multiple_failure(self):
        self.assertEqual(self.api.upload(['test1.json', 'testError.json'], self.dataset_id), "failure")

    @unittest.skipUnless(testMultipleFilesSuccessLarge, "Not currently testing")
    def test_upload_multiple_success_large(self):
        self.assertEqual(self.api.upload(['test1.json', 'test500.json'], self.dataset_id), "success")

    @unittest.skipUnless(testMultipleFilesFailureLarge, "Not currently testing")
    def test_upload_multiple_failure_large(self):
        self.assertEqual(self.api.upload(['test500.json', 'testError.json'], self.dataset_id), "failure")

    @unittest.skipUnless(testUploadAll, "Not currently testing")
    def test_upload_all(self):
        self.assertEqual(self.api.upload(['test128.json', 'test256.json', 'test500.json'], self.dataset_id), "success")


if __name__ == '__main__':
    unittest.main()
