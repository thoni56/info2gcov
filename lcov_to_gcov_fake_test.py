import unittest

from lcov_to_gcov_fake import open_info_file

import os


class TestLcovToGcov(unittest.TestCase):

    def test_open_info_file(self):
        with open("test.info", "w") as f:
            f.write("TN:test_add_parameter")
            f.write("SF:/home/thoni/Utveckling/c-xrefactory/src/c_parser.y")
            f.write("FN:1823,exists_valid_parser_action_on")
            f.write("FN:1838,makeCCompletions")
            f.write("FNDA:0,makeCCompletions")
            f.write("FNDA:0,exists_valid_parser_action_on")
            f.write("FNF:2")
            f.write("FNH:0")
            f.write("DA:251,36")
        try:
            f = open_info_file("test.info")
        except IOError as e:
            self.fail()
        os.remove("test.info")
