

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


class Globals(Enum):
    CHARACTERS_LIST = get_characters()
    LEN_CHARACTER_LIST = len(CHARACTERS_LIST)


pointer_digit = 0