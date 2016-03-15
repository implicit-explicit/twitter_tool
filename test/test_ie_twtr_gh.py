import sys
import unittest
from unittest.mock import patch

import ie_twtr_gh
from twitter import *


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

    


if __name__ == '__main__':
    unittest.main()
