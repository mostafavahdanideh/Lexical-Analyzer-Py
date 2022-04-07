

import globals
from utils import (is_digit, is_letter, is_under_line, 
                    end_of_chars_list, next_char_tpl, next_idx,
                    is_dot, is_quotation, is_invalid_char, is_space,
                    make_up_token_value, error_token_location, token_location,
                   is_reserved_id, is_zero, is_nonzero,
                   is_e_letter, is_minus, is_plus)


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
    start_token_pointer = globals.pointer_digit
    id_value = char
    ID = globals.Globals.ID.value

    while is_digit(char) or is_letter(char) or is_under_line(char):
        char = next_char_tpl()[0]

        if end_of_chars_list():
            break

        id_value = make_up_token_value(id_value, char)

    if is_invalid_char(char) or is_dot(char):
        location_tpl = error_token_location(start_token_pointer, char)
        return ErrorToken(ID, id_value, location_tpl, True, char)
    else:
        id_value = id_value[:len(id_value) - 1]
        location_tpl = token_location(start_token_pointer)
        token_type = ID

        if is_reserved_id(id_value):
            RESERVED_ID = globals.Globals.RESERVED_ID.value
            token_type = RESERVED_ID

        return Token(token_type, id_value, location_tpl, False)


def match_string_token(char):
    start_token_pointer = globals.pointer_digit
    string_value = char
    STRING = globals.Globals.STRING.value

    char = next_char_tpl()[0]
    string_value += char

    while is_digit(char) or is_letter(char) or is_space(char):
        char = next_char_tpl()[0]
        string_value = make_up_token_value(string_value, char)

    if not(is_quotation(char)):
        location_tpl = error_token_location(start_token_pointer, char)
        return ErrorToken(STRING, string_value, location_tpl, True, char)

    location_tpl = token_location(start_token_pointer)
    next_idx()
    return Token(STRING, string_value, location_tpl, False)


def match_invalid_chars(char):
    INVALID_CHAR = globals.Globals.INVALID_CHAR.value

    start_token_pointer = globals.pointer_digit
    location_tpl = error_token_location(start_token_pointer, char)
    first_error_char = CHARACTERS_LIST[start_token_pointer][0]
    last_error_char = CHARACTERS_LIST[globals.pointer_digit][0]
    invalid_char_value = f"{first_error_char}...{last_error_char}"

    return ErrorToken(INVALID_CHAR, invalid_char_value, location_tpl, True, char)


def match_zero_integer(char):
    number_value = char
    start_token_pointer = globals.pointer_digit
    INTEGER = globals.Globals.INTEGER.value
    ZERO = globals.Globals.ZERO.value
    char = next_char_tpl()[0]
    number_value += char

    if is_invalid_char(char) or is_letter(char) or is_digit(char):
        location_tpl = error_token_location(
            start_token_pointer, char)
        return ErrorToken(INTEGER, number_value, location_tpl, True, char)

    elif not is_dot(char):
        location_tpl = token_location(start_token_pointer)
        return Token(INTEGER, ZERO, location_tpl, False)


def match_nonzero_integer(char):
    number_value = char
    start_token_pointer = globals.pointer_digit
    INTEGER = globals.Globals.INTEGER.value
    char = next_char_tpl()[0]
    number_value += char

    while is_digit(char):
        char = next_char_tpl()[0]
        number_value += char

    if is_invalid_char(char) or is_letter(char):
        location_tpl = error_token_location(
            start_token_pointer, char)
        return ErrorToken(INTEGER, number_value, location_tpl, True, char)

    elif not is_dot(char):
        number_value = number_value[:len(number_value) - 1]
        location_tpl = token_location(start_token_pointer)
        return Token(INTEGER, number_value, location_tpl, False)


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
    DOT = globals.Globals.DOT.value
    FLOAT = globals.Globals.FLOAT.value
    start_token_pointer = globals.pointer_digit
    float_value = integer_value + DOT + next_char
    first_char_in_fraction = next_char

    if is_digit(next_char):
        swap, next_char = True, next_char_tpl()[0]
        float_value += next_char

        if is_zero(next_char):
            # if nonzero flag is False, It means we will read zero digit chars
            nonzero_flag = False
        else:
            # if nonzero flag is True, It means we will read nonzero digit chars
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

            if not nonzero_flag and is_e_letter(next_char) and is_nonzero(first_char_in_fraction):
                # for example:
                # if we have this -> "19.23400e-34", this contion will work
                nonzero_flag = True

        if nonzero_flag:
            if not (is_invalid_char(next_char) or is_letter(next_char) or is_dot(next_char)):
                float_value = float_value[:len(float_value) - 1]
                location_tpl = token_location(start_token_pointer)
                return Token(FLOAT, float_value, location_tpl, False)

            elif is_e_letter(next_char):
                next_char = next_char_tpl()[0]
                float_value += next_char
                if is_plus(next_char) or is_minus(next_char):
                    next_char = next_char_tpl()[0]
                    integer_token = match_integer(next_char)
                    if integer_token:
                        float_value += integer_token.value
                        location_tpl = token_location(start_token_pointer)
                        return Token(FLOAT, float_value, location_tpl, False)

    location_tpl = error_token_location(
        start_token_pointer, next_char)
    return ErrorToken(FLOAT, float_value, location_tpl, True, next_char)


def match_integer(char):
    if is_zero(char):
        token = match_zero_integer(char)

    elif is_nonzero(char):
        token = match_nonzero_integer(char)

    return token


def match_number_token(char):
    "Match interger or float number"

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

    return matched_token
