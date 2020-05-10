import unittest
import unittest.mock

from lcov_to_gcov_fake import collate, add_execution_data_for_line


class TestLcovToGcov(unittest.TestCase):

    def test_collates_one_execution_for_one_line_with_single_file_in_info(self):
        info_content = [
            "TN:test_addparameter",
            "SF:/home/thoni/Utveckling/c-xrefactory/src/this_file.c",
            "FN:1823,exists_valid_parser_action_on",
            "FN:1838,makeCCompletions",
            "FNDA:0,makeCCompletions",
            "FNDA:0,exists_valid_parser_action_on",
            "FNF:2",
            "FNH:0",
            "DA:251,36"
        ]
        expected = {251: 36}
        result = collate(info_content, "this_file.c")
        self.assertEqual(result, expected)

    def test_collates_one_execution_for_one_line_with_multiple_files_in_info(self):
        info_content = [
            "TN:test_add_parameter",
            "SF:/home/thoni/Utveckling/c-xrefactory/src/not_this_file.c",
            "SF:/home/thoni/Utveckling/c-xrefactory/src/this_file.c",
            "FN:1823,exists_valid_parser_action_on",
            "FN:1838,makeCCompletions",
            "FNDA:0,makeCCompletions",
            "FNDA:0,exists_valid_parser_action_on",
            "FNF:2",
            "FNH:0",
            "DA:251,36"
        ]
        expected = {251: 36}
        result = collate(info_content, "this_file.c")
        self.assertEqual(result, expected)

    def test_can_add_executions_to_empty_line_data(self):
        data = {}
        expected = {251: 44}
        add_execution_data_for_line(data, (251, 44))
        self.assertEqual(data, expected)

    def test_can_add_executions_to_existing_line_data(self):
        data = {251: 22}
        expected = {251: 66}
        add_execution_data_for_line(data, (251, 44))
        self.assertEqual(data, expected)
