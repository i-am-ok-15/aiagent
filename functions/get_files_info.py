def get_files_info(working_directory, directory=None):
    if directory != working_directory:
        return f"Error: Cannot list "{directory}" as it is outside th epermitted working directory"
    elif os.path.isdir() = False:
        return f"Error: {directory} is not a directory"
    else:
        return "- README.md: file_size=1032 bytes, is_dir=False\n- src: file_size=128 bytes, is_dir=True\n- package.json: file_size=1234 bytes, is_dir=False"
    