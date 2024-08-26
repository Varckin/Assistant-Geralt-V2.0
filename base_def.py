from pathlib import Path


def current_directory():
    return str(Path.cwd()).replace("\\", '/')
