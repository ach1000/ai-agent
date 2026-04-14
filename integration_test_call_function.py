"""
Functional tests for call_function dispatch.

These tests exercise the full call_function -> real function -> Content response
pipeline, but do NOT make any network requests. The working directory is
hard-coded to './calculator' inside call_function, so tests that need file
access use paths relative to that directory.
"""
import unittest
from unittest.mock import MagicMock
from google.genai import types
from functions.call_function import call_function


def make_function_call(name, args=None):
    """Build a minimal mock that looks like a types.FunctionCall."""
    fc = MagicMock(spec=types.FunctionCall)
    fc.name = name
    fc.args = args or {}
    return fc


class TestCallFunctionDispatch(unittest.TestCase):
    def test_unknown_function_returns_error(self):
        """An unknown function name should return a Content with an error key."""
        fc = make_function_call("does_not_exist")
        result = call_function(fc)
        self.assertEqual(result.role, "tool")
        self.assertTrue(result.parts)
        response = result.parts[0].function_response.response
        self.assertIn("error", response)
        self.assertIn("does_not_exist", response["error"])

    def test_get_files_info_returns_result(self):
        """call_function should dispatch to get_files_info and return a result."""
        fc = make_function_call("get_files_info", {"directory": "."})
        result = call_function(fc)
        self.assertEqual(result.role, "tool")
        response = result.parts[0].function_response.response
        self.assertIn("result", response)
        self.assertIn("main.py", response["result"])

    def test_get_file_content_returns_result(self):
        """call_function should dispatch to get_file_content and return file text."""
        fc = make_function_call("get_file_content", {"file_path": "main.py"})
        result = call_function(fc)
        response = result.parts[0].function_response.response
        self.assertIn("result", response)
        self.assertIn("Calculator", response["result"])

    def test_get_file_content_missing_file_returns_error_string(self):
        """get_file_content for a nonexistent file returns an error string in result."""
        fc = make_function_call("get_file_content", {"file_path": "no_such_file.py"})
        result = call_function(fc)
        response = result.parts[0].function_response.response
        self.assertIn("result", response)
        self.assertIn("Error", response["result"])

    def test_run_python_file_returns_result(self):
        """call_function should dispatch to run_python_file and capture output."""
        fc = make_function_call("run_python_file", {"file_path": "main.py"})
        result = call_function(fc)
        response = result.parts[0].function_response.response
        self.assertIn("result", response)
        self.assertIn("Calculator", response["result"])

    def test_write_file_and_read_back(self):
        """call_function should write a file and the content should be readable."""
        write_fc = make_function_call(
            "write_file",
            {"file_path": "pkg/morelorem.txt", "content": "functional test content"},
        )
        write_result = call_function(write_fc)
        write_response = write_result.parts[0].function_response.response
        self.assertIn("result", write_response)
        self.assertNotIn("Error", write_response["result"])

        read_fc = make_function_call("get_file_content", {"file_path": "pkg/morelorem.txt"})
        read_result = call_function(read_fc)
        read_response = read_result.parts[0].function_response.response
        self.assertIn("functional test content", read_response["result"])

    def test_result_content_has_correct_role(self):
        """All successful calls should return Content with role='tool'."""
        for name, args in [
            ("get_files_info", {}),
            ("get_file_content", {"file_path": "main.py"}),
            ("run_python_file", {"file_path": "main.py"}),
        ]:
            with self.subTest(name=name):
                fc = make_function_call(name, args)
                result = call_function(fc)
                self.assertEqual(result.role, "tool")

    def test_result_parts_are_non_empty(self):
        """Returned Content always has at least one part."""
        fc = make_function_call("get_files_info", {"directory": "."})
        result = call_function(fc)
        self.assertTrue(result.parts)

    def test_function_response_name_matches_call(self):
        """The function_response.name should match the dispatched function name."""
        fc = make_function_call("get_files_info", {"directory": "."})
        result = call_function(fc)
        fr = result.parts[0].function_response
        self.assertEqual(fr.name, "get_files_info")


if __name__ == "__main__":
    unittest.main()
