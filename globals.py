

from enum import Enum


def get_characters():

    characters_list = list()

    with open("originalfilename.txt", "r") as file_handler:
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
            "void", "continue")


class Globals(Enum):
    CHARACTERS_LIST = get_characters()
    LEN_CHARACTER_LIST = len(CHARACTERS_LIST)
    RESERVED_IDS = get_reserved_ids()


CHARACTERS_LIST = Globals.CHARACTERS_LIST.value
LEN_CHARACTER_LIST = Globals.LEN_CHARACTER_LIST.value
RESERVED_IDS = Globals.RESERVED_IDS.value

pointer_digit = 0
