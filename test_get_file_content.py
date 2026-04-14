import unittest
from functions.get_file_content import get_file_content
from config import MAX_FILE_CHARS

TEST_MAX_FILE_CHARS = 2000


class TestGetFileContent(unittest.TestCase):
    def test_lorem_ipsum_truncation(self):
        """Test that large files are truncated at MAX_FILE_CHARS"""
        result = get_file_content("calculator", "lorem.txt")
        
        print(f"\nget_file_content('calculator', 'lorem.txt'):")
        print(f"Content length: {len(result)} characters")
        print(f"Last 100 characters:\n  {result[-100:]}")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        
        # Should contain truncation message
        self.assertIn("truncated", result)
        self.assertIn(str(MAX_FILE_CHARS), result)
        
        # Should be longer than MAX_FILE_CHARS due to truncation message
        self.assertGreater(len(result), MAX_FILE_CHARS)
    
    def test_main_py(self):
        """Test reading main.py file"""
        result = get_file_content("calculator", "main.py")
        
        print(f"\nget_file_content('calculator', 'main.py'):")
        print(f"Content (first {TEST_MAX_FILE_CHARS} chars):\n  {result[:TEST_MAX_FILE_CHARS]}")
        print(f"Content length: {len(result)} characters")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        
        # Should contain expected imports
        self.assertIn("import sys", result)
        self.assertIn("def main():", result)
        
        # Should not have truncation message (file is small)
        self.assertNotIn("truncated", result)
    
    def test_pkg_calculator_py(self):
        """Test reading a file in a subdirectory"""
        result = get_file_content("calculator", "pkg/calculator.py")
        
        print(f"\nget_file_content('calculator', 'pkg/calculator.py'):")
        print(f"Content (first {TEST_MAX_FILE_CHARS} chars):\n  {result[:TEST_MAX_FILE_CHARS]}")
        print(f"Content length: {len(result)} characters")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        
        # Should contain expected class
        self.assertIn("class Calculator:", result)
        
        # Should not have truncation message (file is small)
        self.assertNotIn("truncated", result)
    
    def test_absolute_path_outside_working_directory(self):
        """Test that absolute paths outside working_directory are blocked"""
        result = get_file_content("calculator", "/bin/cat")
        
        print(f"\nget_file_content('calculator', '/bin/cat'):")
        print(f"Result:\n  {result}")
        
        # Should return an error string
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("outside the permitted working directory", result)
    
    def test_file_not_found(self):
        """Test that nonexistent files return an error"""
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        
        print(f"\nget_file_content('calculator', 'pkg/does_not_exist.py'):")
        print(f"Result:\n  {result}")
        
        # Should return an error string
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("File not found", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
