import os
from config import MAX_CHARS

from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the content of a file as a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file which will have its contents returned as a string.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    truncate_message = f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'

    try:
        with open(abs_file_path, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(abs_file_path) > MAX_CHARS:
                file_content_string += truncate_message
                return file_content_string
            return file_content_string
    except Exception as error:
        return f"Error: unable to retrieve file contents. {error}"



