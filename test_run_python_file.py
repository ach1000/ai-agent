import unittest
from functions.run_python_file import run_python_file


class TestRunPythonFile(unittest.TestCase):
    def test_run_main_without_args(self):
        """Test running main.py without arguments"""
        result = run_python_file("calculator", "main.py")
        
        print(f"\nrun_python_file('calculator', 'main.py'):")
        print(f"Result:\n{result}\n")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        
        # Should contain usage instructions
        self.assertIn("Calculator App", result)
        self.assertIn("Usage:", result)
    
    def test_run_main_with_args(self):
        """Test running main.py with calculator expression"""
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        
        print(f"\nrun_python_file('calculator', 'main.py', ['3 + 5']):")
        print(f"Result:\n{result}\n")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        
        # Should contain the result
        self.assertIn("STDOUT:", result)
        self.assertIn("8", result)
    
    def test_run_tests(self):
        """Test running the calculator tests"""
        result = run_python_file("calculator", "tests.py")
        
        print(f"\nrun_python_file('calculator', 'tests.py'):")
        print(f"Result (first 500 chars):\n{result[:500]}\n")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        
        # Should contain test output (unittest writes to stderr)
        self.assertTrue("STDOUT:" in result or "STDERR:" in result)
        self.assertIn("OK", result)
    
    def test_execute_outside_working_directory(self):
        """Test that executing files outside working_directory is blocked"""
        result = run_python_file("calculator", "../main.py")
        
        print(f"\nrun_python_file('calculator', '../main.py'):")
        print(f"Result:\n{result}\n")
        
        # Should return an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("outside the permitted working directory", result)
    
    def test_execute_nonexistent_file(self):
        """Test that executing nonexistent files returns an error"""
        result = run_python_file("calculator", "nonexistent.py")
        
        print(f"\nrun_python_file('calculator', 'nonexistent.py'):")
        print(f"Result:\n{result}\n")
        
        # Should return an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("does not exist", result)
    
    def test_execute_non_python_file(self):
        """Test that executing non-Python files returns an error"""
        result = run_python_file("calculator", "lorem.txt")
        
        print(f"\nrun_python_file('calculator', 'lorem.txt'):")
        print(f"Result:\n{result}\n")
        
        # Should return an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("not a Python file", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
