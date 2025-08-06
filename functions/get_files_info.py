import os

def get_files_info(working_directory, directory="."):
    full_path_abs = os.path.abspath(os.path.join(working_directory, directory))
    working_directory_abs = os.path.abspath(working_directory)

    if full_path_abs.startswith(working_directory_abs) is False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(full_path_abs) is False:
        return f'Error: "{full_path_abs}" is not a directory'

    directory_content = []

    try:

        for item in os.listdir(full_path_abs):
            file_size = os.path.getsize(os.path.join(full_path_abs, item))
            dir_status = os.path.isfile(os.path.join(full_path_abs, item))
            directory_content.append(f"- {item}: file_size={file_size} bytes, is_dir={dir_status}")
    
    except Exception as error:
        return f"Error: unable to retrieve file details. {error}"

    content_string = "\n".join(directory_content)
    return content_string