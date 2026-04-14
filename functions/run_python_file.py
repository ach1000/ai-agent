import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    """
    Run a Python file within a working_directory with optional arguments.
    
    Args:
        working_directory: The base directory to restrict execution to.
        file_path: The relative path to the Python file to run.
        args: Optional list of command-line arguments to pass to the script.
    
    Returns:
        A string containing the execution output or an error message.
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # Construct the full path to the target file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Validate that target_file falls within working_dir_abs
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if the target path exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        # Check if the file is a Python file
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        # Build the command to run
        command = ["python", target_file]
        
        # Add any additional arguments
        if args:
            command.extend(args)
        
        # Run the command with a timeout
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Build the output string
        output_lines = []
        
        # Check exit code
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")
        
        # Check if there's any output
        if not result.stdout and not result.stderr:
            output_lines.append("No output produced")
        else:
            if result.stdout:
                output_lines.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_lines.append(f"STDERR:\n{result.stderr}")
        
        return "\n".join(output_lines)
    
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: execution exceeded 30-second timeout"
    except Exception as e:
        return f"Error: executing Python file: {e}"
