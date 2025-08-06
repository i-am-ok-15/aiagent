import os
from functions.get_files_info import get_files_info

def get_file_content(working_directory, file_path):
    full_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if file_path not in get_files_info(full_path_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(full_path_abs) is False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    file_content = ""

    MAX_CHARS = 10000
    truncate_message = f' [...File "{file_path}" truncated at 10000 characters]'

    try:
        with open(full_path_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content += file_content_string + truncate_message
                return file_content
            file_content += file_content_string
            return file_content
    except Exception as error:
        return f"Error: unable to retrieve file contents. {error}"



