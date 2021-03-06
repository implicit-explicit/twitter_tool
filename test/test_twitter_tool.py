import math
import sys
import unittest
from unittest.mock import patch

import twitter_tool
import twitter


class MainTestCase(unittest.TestCase):
    """ Main definition tests """

    def test_target_check(self):
        """ Checks for target as command line argument """
        del sys.argv[1]
        test_command = sys.argv[1]
        function_command = twitter_tool.target_check()
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
        auth_keys = twitter_tool.read_auth_file("test/test_keys")
        self.assertListEqual(auth_keys, test_keys)

    @patch("twitter_tool.get_auth_keys")
    def test_get_auth_keys(self, mock_get_auth_keys):
        """ Checking if auth_keys read are what they are {o,o} """
        mock_get_auth_keys.return_value = ['consumer_key', 'consumer_secret']
        auth_key_value = twitter_tool.get_auth_keys()
        test_key_value = ['consumer_secret', 'consumer_key']
        self.assertEqual(auth_key_value[0], test_key_value[1])

    def test_get_a_bearer_token(self):
        """ Make sure the twitter.oauth2_dance() function gives us a bearer token  """
        import os
        auth_keys = twitter_tool.get_auth_keys()
        bearer_token_file = "test/test_bearer_token"
        twitter.oauth2_dance(consumer_key=auth_keys[0], consumer_secret=auth_keys[1], token_filename=bearer_token_file)
        os.remove(bearer_token_file)


class RateLimitCalculationTestCase(unittest.TestCase):
    """ Tests to calculate the Twitter API Rate Limit.
    Numbers source: https://dev.twitter.com/rest/reference/get/followers/list """

    def setUp(self):
        """ Data needed for calculations  """
        import random
        self.rate_request_limit = 30
        self.rate_time_limit = 900
        self.max_followers_per_request = 200
        self.followers = random.randrange(0, 200000)

    def test_calculate_hits(self):
        """ Calculate the number of request hits (rounded up) """
        hits = math.ceil(self.followers / self.max_followers_per_request)
        print("{0} = {1} / {2}".format(hits, self.followers, self.max_followers_per_request))

    def test_calculate_rate_limit_count(self):
        """ Calculates the number of rate limits (rounded up) """
        hits = math.ceil(self.followers / self.max_followers_per_request)
        rate_limit_count = math.ceil(hits / self.rate_request_limit)
        print("{0} = {1} / {2}".format(rate_limit_count, hits, self.rate_request_limit))

    def test_rate_limit_duration(self):
        """ Calculates the approximate duration in seconds """
        hits = math.ceil(self.followers / self.max_followers_per_request)
        rate_limit_count = math.ceil(hits / self.rate_request_limit)
        rate_limit_duration = rate_limit_count * self.rate_time_limit
        print("{0} sec. = {1} * {2}".format(rate_limit_duration, rate_limit_count, self.rate_time_limit))


if __name__ == '__main__':
    unittest.main()
