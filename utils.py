

import globals


CHARACTERS_LIST = globals.CHARACTERS_LIST
LEN_CHARACTER_LIST = globals.LEN_CHARACTER_LIST
        

def write_token(type, value, location):
    with open("source_code.outlextokens.txt", "a") as handler:
        handler.write(f"<{type}, {value}, {location}>\n")


def write_error(type, value, location, error_char):
    with open("source_code.outlexerrors.txt", "a") as handler:
        handler.write(f"<{type}, {value}, {location}, {error_char}>\n")


def is_invalid_char(char):
    if char in ["#", "$", "~", "`"]:
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
    if char == "_":
        return True
    return False


def is_dot(char):
    if char == ".":
        return True
    return False


def reach_to_special_char(char):
    while char:
        if char in [";", "{", ":"]:
            break
        elif end_of_chars_list():
            return "EOF"
        char = next_char_tpl()[0]


def error_token_location(start_token_pointer, char):
    if reach_to_special_char(char) == "EOF":
        character_end_loc = "EOF"
        line_number = CHARACTERS_LIST[start_token_pointer][1]
    else:
        character_end_loc = CHARACTERS_LIST[globals.pointer_digit][2] + 1
        line_number = CHARACTERS_LIST[globals.pointer_digit][1]

    character_start_loc = CHARACTERS_LIST[start_token_pointer][2] + 1
        
    character_location_in_line = (
        character_start_loc,
        character_end_loc)

    location_tpl = (
        line_number,
        character_location_in_line)
    
    return location_tpl


def token_location(start_token_pointer):
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
    "concatinating string, id, integer and float value"
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
    if char == '"':
        return True
    return False


def is_space(char):
    if char == " ":
        return True
    return False


def is_zero(char):
    if char == "0":
        return True
    return False

def is_reserved_id(value):
    RESERVED_IDS = globals.RESERVED_IDS

    if value in RESERVED_IDS:
        return True
        
    return False
