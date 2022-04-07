

import globals
from utils import (is_digit, is_letter, is_under_line, 
                    end_of_chars_list, next_char_tpl, next_idx,
                    is_dot, is_quotation, is_invalid_char, is_space,
                    make_up_token_value, error_token_location, token_location,
                   is_reserved_id, is_zero, is_nonzero)


CHARACTERS_LIST = globals.CHARACTERS_LIST
LEN_CHARACTER_LIST = globals.LEN_CHARACTER_LIST


class Token:
    def __init__(self, token_type, value, location, error) -> None:
        self.token_type = token_type
        self.value = value
        self.location = location
        self.error = error


class ErrorToken(Token):
    def __init__(self, token_type, value, location, error, error_char) -> None:
        super().__init__(token_type, value, location, error)
        self.error_char = error_char


def match_id_token(char):
    start_token_pointer, id_value = globals.pointer_digit, char

    while is_digit(char) or is_letter(char) or is_under_line(char):
        char = next_char_tpl()[0]

        if end_of_chars_list():
            break

        id_value = make_up_token_value(id_value, char)

    if is_invalid_char(char) or is_dot(char):
        location_tpl = error_token_location(start_token_pointer, char)
        return ErrorToken("ID", id_value, location_tpl, True, char)
    else:
        id_value = id_value[:len(id_value) - 1]
        location_tpl = token_location(start_token_pointer)
        token_type = "ID"

        if is_reserved_id(id_value):
            token_type = "RESERVED_ID"

        return Token(token_type, id_value, location_tpl, False)


def match_string_token(char):
    start_token_pointer, string_value = globals.pointer_digit, char

    char = next_char_tpl()[0]
    string_value += char

    while is_digit(char) or is_letter(char) or is_space(char):
        char = next_char_tpl()[0]
        string_value = make_up_token_value(string_value, char)

    if not(is_quotation(char)):
        location_tpl = error_token_location(start_token_pointer, char)
        return ErrorToken("STRING", string_value, location_tpl, True, char)

    location_tpl = token_location(start_token_pointer)
    next_idx()
    return Token("STRING", string_value, location_tpl, False)


def match_invalid_chars(char):
    start_token_pointer = globals.pointer_digit
    location_tpl = error_token_location(start_token_pointer, char)
    invalid_char_value = f"{CHARACTERS_LIST[start_token_pointer][0]}...{CHARACTERS_LIST[globals.pointer_digit][0]}"
    return ErrorToken("INVALID_CHAR", invalid_char_value, location_tpl, True, char)


def match_zero_integer(char):
    number_value = char
    start_token_pointer = globals.pointer_digit
    char = next_char_tpl()[0]
    number_value += char

    if is_invalid_char(char) or is_letter(char) or is_digit(char):
        location_tpl = error_token_location(
            start_token_pointer, char)
        return ErrorToken("Integer", number_value, location_tpl, True, char)

    elif not is_dot(char):
        location_tpl = token_location(start_token_pointer)
        return Token("Integer", "0", location_tpl, False)


def match_nonzero_integer(char):
    number_value = char
    start_token_pointer = globals.pointer_digit
    char = next_char_tpl()[0]
    number_value += char

    while is_digit(char):
        char = next_char_tpl()[0]
        number_value += char

    if is_invalid_char(char) or is_letter(char):
        location_tpl = error_token_location(
            start_token_pointer, char)
        return ErrorToken("Integer", number_value, location_tpl, True, char)

    elif not is_dot(char):
        number_value = number_value[:len(number_value) - 1]
        location_tpl = token_location(start_token_pointer)
        return Token("Integer", number_value, location_tpl, False)


def get_integer_value_before_dot():
    previous_idx = globals.pointer_digit - 1
    previous_char = CHARACTERS_LIST[previous_idx][0]
    integer_value_before_dot = previous_char

    while is_digit(previous_char):
        previous_idx = previous_idx - 1
        previous_char = CHARACTERS_LIST[previous_idx][0]
        integer_value_before_dot = previous_char + integer_value_before_dot

    return integer_value_before_dot[1:]


def match_float_token(integer_value, next_char):
    start_token_pointer = globals.pointer_digit
    float_value = integer_value + "." + next_char

    if is_digit(next_char):
        swap = True
        next_char = next_char_tpl()[0]
        float_value += next_char

        if is_zero(next_char):
            nonzero_flag = False
        else:
            nonzero_flag = True

        while swap:
            while is_nonzero(next_char):
                next_char = next_char_tpl()[0]
                if is_zero(next_char):
                    nonzero_flag = False
                float_value += next_char

            while is_zero(next_char):
                next_char = next_char_tpl()[0]
                if is_nonzero(next_char):
                    nonzero_flag = True
                float_value += next_char
            
            if not(is_nonzero(next_char)):
                swap = False

        if nonzero_flag:
            if not (is_invalid_char(next_char) or is_letter(next_char) or is_dot(next_char)):
                float_value = float_value[:len(float_value) - 1]
                location_tpl = token_location(start_token_pointer)
                return Token("Float", float_value, location_tpl, False)

            elif next_char == "e":
                next_char = next_char_tpl()[0]
                float_value += next_char
                if next_char == "+" or next_char == "-":
                    next_char = next_char_tpl()[0]
                    integer_token = match_integer(next_char)
                    if integer_token:
                        float_value += integer_token.value
                        location_tpl = token_location(start_token_pointer)
                        return Token("Float", float_value, location_tpl, False)
            swap = False
        else: # float here is -> 0.000, 0.000?, 0.000#, 0.000s 10.0s 10.111.
            swap = False

    location_tpl = error_token_location(
        start_token_pointer, next_char)
    return ErrorToken("Float", float_value, location_tpl, True, next_char)


def match_integer(char):
    if is_zero(char):
        token = match_zero_integer(char)

    elif is_nonzero(char):
        token = match_nonzero_integer(char)

    return token


def match_number_token(char):
    "match interger or float number"

    integer_token = match_integer(char)
    
    if integer_token:
        return integer_token
    else:
        char = CHARACTERS_LIST[globals.pointer_digit][0]

    if is_dot(char):
        # dot is matched and when we see dot, we will have to match float number
        integer_value_before_dot = get_integer_value_before_dot()
        char = next_char_tpl()[0]
        return match_float_token(integer_value_before_dot, char)


def next_token():
    "Get next token, create then return it."

    char = CHARACTERS_LIST[globals.pointer_digit][0]

    if is_letter(char):
        matched_token = match_id_token(char)

    elif is_invalid_char(char):
        matched_token = match_invalid_chars(char)

    elif is_quotation(char):
        matched_token = match_string_token(char)

    elif is_digit(char):
        matched_token = match_number_token(char)

    else:
        next_idx()
        matched_token = None

    return globals.pointer_digit, matched_token
