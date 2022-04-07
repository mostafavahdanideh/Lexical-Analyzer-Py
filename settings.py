
from enum import Enum

import os
import platform


class Settings(Enum):
    SOURCE_FILE_NAME = "source_code.txt"
    OUTLEXTOKENS_FILE_NAME = "source_code.outlextokens.txt"
    OUTLEXERRORS_FILE_NAME = "source_code.outlexerrors.txt"


def file_seperator_path():
    user_os = platform.system()

    if user_os == "Linux" or user_os == "Darwin":
        path_seperator = "/"
    else:
        path_seperator = "\\"

    return path_seperator


def current_abspath():
    return os.path.dirname(os.path.abspath(__file__)) + file_seperator_path()


def source_file_path():
    return current_abspath() + Settings.SOURCE_FILE_NAME.value


def outlextokens_file_path():
    return current_abspath() + Settings.OUTLEXTOKENS_FILE_NAME.value


def outlexerrors_file_path():
    return current_abspath() + Settings.OUTLEXERRORS_FILE_NAME.value
