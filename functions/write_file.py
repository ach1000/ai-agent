import os
from config import MAX_FILE_CHARS


def write_file(working_directory, file_path, content):
    """
    Write content to a file relative to a working_directory.
    
    Args:
        working_directory: The base directory to restrict access to.
        file_path: The relative file path to write to.
        content: The content to write to the file.
    
    Returns:
        A success message if the file was written,
        or an error message if validation fails or writing fails.
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # Construct the full path to the target file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Validate that target_file falls within working_dir_abs
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Check if the target path is a directory
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Create parent directories if needed
        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        
        # Write the file
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"
