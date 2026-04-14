import os
from config import MAX_FILE_CHARS


def get_file_content(working_directory, file_path):
    """
    Read the contents of a file relative to a working_directory.
    
    Args:
        working_directory: The base directory to restrict access to.
        file_path: The relative file path to read.
    
    Returns:
        The file contents as a string (up to MAX_FILE_CHARS characters),
        or an error message if validation fails or reading fails.
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # Construct the full path to the target file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Validate that target_file falls within working_dir_abs
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the target path exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read(MAX_FILE_CHARS)
            
            # Check if there's more content (truncation detection)
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
        
        return content
    
    except Exception as e:
        return f"Error: {str(e)}"
