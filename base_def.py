import os

def current_directory():
    return os.getcwd().replace("\\", '/')
