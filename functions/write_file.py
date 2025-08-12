import os

from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file with a given string of content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file path": types.Schema(
                type=types.Type.STRING,
                description="The file that will be written or overwriten withh the given content.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        dir_name = os.path.dirname(abs_file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as error:
        return f"Error: unable to write to file {error}"