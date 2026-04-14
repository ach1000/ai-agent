import unittest
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_root_directory(self):
        """Test listing the calculator root directory"""
        result = get_files_info("calculator", ".")
        
        print(f"\nget_files_info('calculator', '.'):")
        print("Result for '.' directory:")
        for line in result.split("\n"):
            print(f"  {line}")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        
        # Should contain expected files
        self.assertIn("main.py:", result)
        self.assertIn("tests.py:", result)
        self.assertIn("pkg:", result)
        
        # Should have proper format
        self.assertIn("file_size=", result)
        self.assertIn("is_dir=", result)
    
    def test_calculator_pkg_subdirectory(self):
        """Test listing the calculator/pkg subdirectory"""
        result = get_files_info("calculator", "pkg")
        
        print(f"\nget_files_info('calculator', 'pkg'):")
        print("Result for 'pkg' directory:")
        for line in result.split("\n"):
            print(f"  {line}")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        
        # Should contain expected files
        self.assertIn("calculator.py:", result)
        self.assertIn("render.py:", result)
        
        # Should have proper format
        self.assertIn("file_size=", result)
        self.assertIn("is_dir=", result)
        
        # Verify it's not a directory
        self.assertIn("calculator.py: file_size=", result)
        self.assertIn("is_dir=False", result)
    
    def test_absolute_path_outside_working_directory(self):
        """Test that absolute paths outside working_directory are blocked"""
        result = get_files_info("calculator", "/bin")
        
        print(f"\nget_files_info('calculator', '/bin'):")
        print("Result for '/bin' directory:")
        for line in result.split("\n"):
            print(f"  {line}")
        
        # Should return an error string
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("outside the permitted working directory", result)
    
    def test_parent_directory_escape_attempt(self):
        """Test that parent directory escape attempts are blocked"""
        result = get_files_info("calculator", "../")
        
        print(f"\nget_files_info('calculator', '../'):")
        print("Result for '../' directory:")
        for line in result.split("\n"):
            print(f"  {line}")
        
        # Should return an error string
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("outside the permitted working directory", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
