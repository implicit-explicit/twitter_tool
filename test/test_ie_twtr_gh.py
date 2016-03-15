import sys
import unittest
from unittest.mock import patch

import ie_twtr_gh
import twitter


class MainTestCase(unittest.TestCase):
    """ Main definition tests """

    def test_target_check(self):
        """ Checks for target as command line argument """
        del sys.argv[1]
        test_command = sys.argv[1]
        function_command = ie_twtr_gh.target_check()
        if test_command == "-v":
            print("No arguments passed, moving on!")
        elif (len(sys.argv[1]) > 0) & (test_command != "-v"):
            self.assertEqual(function_command, test_command)

    def test_read_auth_file(self):
        """ Test if lines from 'auth_keys' are read correctly by comparison"""
        with open("test/test_keys", "r") as test_file:
            test_keys = []
            for line in test_file:
                test_keys.append(line.strip())
        auth_keys = ie_twtr_gh.read_auth_file("test/test_keys")
        self.assertListEqual(auth_keys, test_keys)

    @patch("ie_twtr_gh.get_auth_keys")
    def test_get_auth_keys(self, mock_get_auth_keys):
        """ Checking if auth_keys read are what they are {o,o} """
        mock_get_auth_keys.return_value = ['consumer_key', 'consumer_secret']
        auth_key_value = ie_twtr_gh.get_auth_keys()
        test_key_value = ['consumer_secret', 'consumer_key']
        self.assertEqual(auth_key_value[0], test_key_value[1])


if __name__ == '__main__':
    unittest.main()
