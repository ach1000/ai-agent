import os


def get_files_info(working_directory, directory="."):
    """
    List the contents of a directory relative to a working_directory.
    
    Args:
        working_directory: The base directory to restrict access to.
        directory: The relative directory path to list (defaults to ".").
    
    Returns:
        A string representing the directory contents with metadata,
        or an error message if validation fails.
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # Construct the full path to the target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # Validate that target_dir falls within working_dir_abs
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the target directory exists and is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        # List the contents of the directory
        items = os.listdir(target_dir)
        
        # Build the output string
        lines = []
        for item in sorted(items):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            
            # Get file size
            if is_dir:
                # For directories, get the total size of contents (simplified)
                try:
                    file_size = sum(
                        os.path.getsize(os.path.join(root, f))
                        for root, dirs, files in os.walk(item_path)
                        for f in files
                    )
                except (OSError, IOError):
                    file_size = 0
            else:
                try:
                    file_size = os.path.getsize(item_path)
                except (OSError, IOError):
                    file_size = 0
            
            lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(lines)
    
    except Exception as e:
        return f"Error: {str(e)}"
