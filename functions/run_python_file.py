import os
import subprocess

from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a chosen python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file which will be run.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
             return f'Error: "{file_path}" is not a Python file.'
        
        task = ["python", file_path] + args

        output = subprocess.run(task, text=True, capture_output=True, cwd=working_directory, timeout=30)

        stdout_str = output.stdout.strip() if output.stdout else ""
        stderr_str = output.stderr.strip() if output.stderr else ""

        formatted_parts = []
        if stdout_str:
            formatted_parts.append(f"STDOUT: {stdout_str}")
        if stderr_str:
            formatted_parts.append(f"STDERR: {stderr_str}")

        if output.returncode != 0:
            formatted_parts.append(f"Process exited with code {output.returncode}")

        if not formatted_parts:
            return "No output produced."
        
        return "\n".join(formatted_parts)        
        
    except Exception as error:
        return f"Error: executing Python file: {error}"
