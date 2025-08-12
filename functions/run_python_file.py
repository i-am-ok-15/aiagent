import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        if abs_file_path[-3:] != ".py":
             return f'Error: "{file_path}" is not a Python file.'
        
        task = ["python", file_path] + args

        output = subprocess.run(task, text=True, stdout=True, stderr=True, cwd=working_directory, timeout=30)

        formatted_output = f"""
                            STDOUT: {output.stdout}\n
                            STDERR: {output.stderr}\n
                            """

        if output.returncode != 0:
            formatted_output += f"Process existed with code {output.returncode}"
        
        if output.stdout is None:
            formatted_output += f"No output produced."

        return formatted_output
        
    except Exception as error:
        return f"Error: executing Python file: {error}"
