

from enum import Enum
import settings


def get_characters():
    characters_list = list()

    with open(settings.source_file_path(), "r") as file_handler:
        line_number, char_number_in_line = 1, 0
        char = file_handler.read(1)

        while char: # while char != EOF
            characters_list.append((
                char,
                line_number,
                char_number_in_line))

            char_number_in_line += 1

            if char == "\n":
                line_number += 1
                char_number_in_line = 0

            char = file_handler.read(1)

    return characters_list


def get_reserved_ids():
    return ("main", "if", "else",
            "public", "read", "then",
            "private", "write", "func",
            "return", "integer", "var",
            "float", "class", "inherits",
            "string", "while", "break",
            "void", "continue", 'true', 'false')


class Globals(Enum):
    CHARACTERS_LIST = get_characters()
    LEN_CHARACTER_LIST = len(CHARACTERS_LIST)
    RESERVED_IDS = get_reserved_ids()

    INVALID_CHAR = "INVALID_CHAR"
    FLOAT = "FLOAT"
    STRING = "STRING"
    INTEGER = "INTEGER"
    ID = "ID"
    RESERVED_ID = "RESERVED_ID"
    EOF = "EOF"
    COMMENT = "COMMENT"

    ZERO = "0"
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    SINGLE_COLON = ":"
    DOUBLE_COLON = "::"
    ASSIGN = "="
    EQUAL = "=="
    NOT_EQUAL = "<>"
    DIVIDER = "/"
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    POW = "**"
    VERTICAL_BAR = "|"
    EXCLAMATION_MARK = "!"
    QUESTION_MARK = "?"
    OPEN_PARENTHESE = "("
    CLOSE_PARENTHESE = ")"
    OPEN_CURLY_BRACKET = "{"
    CLOSE_CURLY_BRACKET = "}"
    OPEN_SQUARE_BRACKET = "["
    CLOSE_SQUARE_BRACKET = "]"
    SEMICOLON = ";"
    DOT = "."
    COMMA = ","


CHARACTERS_LIST = Globals.CHARACTERS_LIST.value
LEN_CHARACTER_LIST = Globals.LEN_CHARACTER_LIST.value
RESERVED_IDS = Globals.RESERVED_IDS.value

pointer_digit = 0
