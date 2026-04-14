import unittest
from functions.write_file import write_file
from functions.get_file_content import get_file_content


class TestWriteFile(unittest.TestCase):
    def test_overwrite_existing_file(self):
        """Test overwriting an existing file"""
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        
        print(f"\nwrite_file('calculator', 'lorem.txt', 'wait, this isn\\'t lorem ipsum'):")
        print(f"Result:\n  {result}")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        self.assertIn("Successfully wrote", result)
        self.assertIn("28 characters written", result)
        
        # Verify the content was actually written
        content = get_file_content("calculator", "lorem.txt")
        self.assertEqual(content, "wait, this isn't lorem ipsum")
    
    def test_write_to_subdirectory(self):
        """Test writing to a file in a subdirectory that needs to be created"""
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        
        print(f"\nwrite_file('calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet'):")
        print(f"Result:\n  {result}")
        
        # Should not be an error
        self.assertFalse(result.startswith("Error:"))
        self.assertIn("Successfully wrote", result)
        self.assertIn("26 characters written", result)
        
        # Verify the content was actually written
        content = get_file_content("calculator", "pkg/morelorem.txt")
        self.assertEqual(content, "lorem ipsum dolor sit amet")
    
    def test_write_outside_working_directory(self):
        """Test that writes outside working_directory are blocked"""
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        
        print(f"\nwrite_file('calculator', '/tmp/temp.txt', 'this should not be allowed'):")
        print(f"Result:\n  {result}")
        
        # Should return an error string
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("outside the permitted working directory", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
