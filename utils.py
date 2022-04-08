

import globals
import settings

CHARACTERS_LIST = globals.CHARACTERS_LIST
LEN_CHARACTER_LIST = globals.LEN_CHARACTER_LIST
        

def write_token(type, value, location):
    with open(settings.outlextokens_file_path(), "a") as handler:
        handler.write(f"<{type}, {value}, {location}>\n")


def write_error(type, value, location, error_char):
    with open(settings.outlexerrors_file_path(), "a") as handler:
        handler.write(f"<{type}, {value}, {location}, {error_char}>\n")


def is_invalid_char(char):
    decimal_ascii_code = ord(char)
    # invalid chars are -> [#, $, ~, `, @]
    if decimal_ascii_code in [35, 36, 126, 96, 64]:
        return True
    return False


def is_reserved_special_char(char):
    if char in ["&", "!", "|", "[", "]", "{", "}", "(", ")", ";", ".", ",", "?"]:
        return True
    return False


def is_operator(char):
    if char in ["+", "-", "<", ">", "=", ":"]:
        return True
    return False

def is_letter(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code in range(65, 91) \
            or decimal_ascii_code in range(97, 123):
        return True

    return False


def is_digit(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code in range(48, 58):
        return True
    return False


def is_nonzero(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code in range(49, 58):
        return True
    return False


def is_under_line(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 95:
        return True
    return False


def is_dot(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 46:
        return True
    return False


def reach_to_special_char_seperator(char):
    # special chars are -> [";", "{", ":"]
    while char:
        decimal_ascii_code = ord(char)

        if decimal_ascii_code in [59, 123, 58]:
            break

        elif end_of_chars_list():
            EOF = globals.Globals.EOF.value
            return EOF

        char = next_char_tpl()[0]


def error_state_location(start_token_pointer, char):
    EOF = globals.Globals.EOF.value
    begin_line_number = CHARACTERS_LIST[start_token_pointer][1]
    character_start_loc = CHARACTERS_LIST[start_token_pointer][2] + 1

    if reach_to_special_char_seperator(char) == EOF:
        character_end_loc = EOF
    else:
        character_end_loc = CHARACTERS_LIST[globals.pointer_digit][2] + 1

    end_line_number = CHARACTERS_LIST[globals.pointer_digit][1]
    character_location = [(begin_line_number, character_start_loc),
                            (end_line_number, character_end_loc)]
    
    return character_location


def final_state_location(start_token_pointer):
    line_number = CHARACTERS_LIST[globals.pointer_digit][1]
    character_start_loc = CHARACTERS_LIST[start_token_pointer][2] + 1
    character_end_loc = CHARACTERS_LIST[globals.pointer_digit][2]

    character_location_in_line = (
        character_start_loc,
        character_end_loc)

    location_tpl = (
        line_number,
        character_location_in_line)

    return location_tpl


def make_up_token_value(pre_value, next_value):
    "Concatinating string, id, integer and float value"

    pre_value += next_value
    return pre_value


def end_of_chars_list():
    if globals.pointer_digit + 1 == LEN_CHARACTER_LIST:
        return True
    return False


def next_char_tpl():
    if not(end_of_chars_list()):
        globals.pointer_digit += 1

    return CHARACTERS_LIST[globals.pointer_digit]


def next_idx():
    if not(end_of_chars_list()):
        globals.pointer_digit += 1


def is_quotation(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 34:
        return True
    return False


def is_space(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 32:
        return True
    return False


def is_zero(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 48:
        return True
    return False


def is_plus(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 43:
        return True
    return False


def is_minus(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 45:
        return True
    return False


def is_e_letter(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 101:
        return True
    return False


def is_reserved_id(value):
    RESERVED_IDS = globals.RESERVED_IDS

    if value in RESERVED_IDS:
        return True
        
    return False


def is_star(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 42:
        return True
    return False


def is_slash(char):
    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 47:
        return True
    return False


def is_newline(char):
    "Check we have line feed/newline or not"

    decimal_ascii_code = ord(char)

    if decimal_ascii_code == 10:
        return True
    return False


def is_white_space(char):
    decimal_ascii_code = ord(char)

    # whitespace -> [ht(\t), nl(\n), vt, sp]

    if decimal_ascii_code in [9, 10, 11, 32]:
        return True
    return False
