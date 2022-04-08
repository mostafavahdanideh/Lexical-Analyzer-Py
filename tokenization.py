

import globals
from utils import (error_state_location, final_state_location, is_digit, 
                    is_letter, is_newline, is_slash, is_star, is_under_line, 
                    end_of_chars_list, is_white_space, next_char_tpl, next_idx,
                    is_dot, is_quotation, is_invalid_char, is_space,
                    make_up_token_value, is_reserved_id, is_zero, 
                    is_nonzero, is_e_letter, is_minus, is_plus)


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


def error_state(token_type, token_value, error_char):
    "Figure out how to run from error/trap/loop state"

    start_token_pointer = globals.pointer_digit
    location_lst = error_state_location(start_token_pointer, error_char)
    return ErrorToken(token_type, token_value, location_lst, True, error_char)


def final_state(start_token_pointer, token_type, token_value):
    location_tpl = final_state_location(start_token_pointer)
    return Token(token_type, token_value, location_tpl, False)


def id_tokenizer(char):
    id_value = char
    token_type = globals.Globals.ID.value
    start_token_pointer = globals.pointer_digit

    while is_digit(char) or is_letter(char) or is_under_line(char):
        char = next_char_tpl()[0]
        id_value = make_up_token_value(id_value, char)
        if end_of_chars_list():
            break

    if is_invalid_char(char) or is_dot(char):
        return error_state(token_type, id_value, char)

    id_value = id_value[:len(id_value) - 1]

    if is_reserved_id(id_value):
        RESERVED_ID = globals.Globals.RESERVED_ID.value
        token_type = RESERVED_ID

    return final_state(start_token_pointer, token_type, id_value)


def string_tokenizer(char):
    string_value = char
    STRING = globals.Globals.STRING.value
    start_token_pointer = globals.pointer_digit

    char = next_char_tpl()[0]
    string_value += char

    while is_digit(char) or is_letter(char) or is_space(char):
        char = next_char_tpl()[0]
        string_value = make_up_token_value(string_value, char)

    if not(is_quotation(char)):
        return error_state(STRING, string_value, char)

    next_idx() # read next char after final quotation
    return final_state(start_token_pointer, STRING, string_value)


def invalid_character_tokenizer(char):
    INVALID_CHAR = globals.Globals.INVALID_CHAR.value
    start_token_pointer = globals.pointer_digit
    invalid_char_value = CHARACTERS_LIST[start_token_pointer][0]
    return error_state(INVALID_CHAR, invalid_char_value, char)


def match_zero_integer(char):
    INTEGER = globals.Globals.INTEGER.value
    ZERO = globals.Globals.ZERO.value
    start_token_pointer = globals.pointer_digit
    number_value = char
    char = next_char_tpl()[0]
    number_value += char

    if is_invalid_char(char) or is_letter(char) or is_digit(char):
        return error_state(INTEGER, number_value, char)

    elif not is_dot(char):
        return final_state(start_token_pointer, INTEGER, ZERO)


def match_nonzero_integer(char):
    INTEGER = globals.Globals.INTEGER.value
    start_token_pointer = globals.pointer_digit
    number_value = char
    char = next_char_tpl()[0]
    number_value += char

    while is_digit(char):
        char = next_char_tpl()[0]
        number_value += char

    if is_invalid_char(char) or is_letter(char):
        return error_state(INTEGER, number_value, char)

    elif not is_dot(char):
        number_value = number_value[:len(number_value) - 1]
        return final_state(start_token_pointer, INTEGER, number_value)


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
    start_token_pointer = globals.pointer_digit - len(integer_value) - 1
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
                return final_state(start_token_pointer, FLOAT, float_value)

            elif is_e_letter(next_char):
                next_char = next_char_tpl()[0]
                float_value += next_char
                if is_plus(next_char) or is_minus(next_char):
                    next_char = next_char_tpl()[0]
                    integer_token = match_integer(next_char)
                    if integer_token:
                        float_value += integer_token.value
                        return final_state(start_token_pointer, FLOAT, float_value)

    return error_state(FLOAT, float_value, next_char)


def match_integer(char):
    if is_zero(char):
        token = match_zero_integer(char)

    elif is_nonzero(char):
        token = match_nonzero_integer(char)

    return token


def rational_number_tokenizer(char):
    "Match interger, float and natural number"

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


def multiply_or_pow_tokenizer(char):
    "Match multiply or pow"

    MULTIPLY = globals.Globals.MULTIPLY.name
    POW = globals.Globals.POW.name
    INVALID_CHAR = globals.Globals.INVALID_CHAR.value
    COMMENT = globals.Globals.COMMENT.value
    start_token_pointer = globals.pointer_digit
    value = char
    char = next_char_tpl()[0]
    value += char

    if is_star(char):
        next_idx()
        return final_state(start_token_pointer, POW, value)
    elif is_slash(char):
        char = next_char_tpl()[0]
        while not(is_slash(char)):
            char = next_char_tpl()[0]
        char = next_char_tpl()[0]
        
        if is_star(char):
            # when we read star, It means we are in the end of comment and we don't need comment tokens
            next_idx()  # next char after final quotation
        else:
            return error_state(COMMENT, value, char)
    elif is_invalid_char(char):
        return error_state(INVALID_CHAR, value, char)
    else:
        value = value[:len(value) - 1]
        return final_state(start_token_pointer, MULTIPLY, value)


def division_operator_tokenizer(char):
    DIVISION = globals.Globals.DIVISION.name
    start_token_pointer = globals.pointer_digit
    op_value = char
    char = next_char_tpl()[0]

    if is_slash(char):
        while not (is_newline(char) or end_of_chars_list()):
            char = next_char_tpl()[0]
    elif is_invalid_char(char):
        op_value += char
        return error_state(DIVISION, op_value)
    else:
        return final_state(start_token_pointer, DIVISION, op_value)


def less_than_operator_tokenizer(char):
    start_token_pointer = globals.pointer_digit
    token_value = char
    char = next_char_tpl()[0]
    token_value += char

    if char == "=":
        next_idx()
        token_type = globals.Globals.LESS_EQUAL.name
    elif char == ">":
        next_idx()
        token_type = globals.Globals.NOT_EQUAL.name
    elif is_invalid_char(char):
        token_type = globals.Globals.INVALID_CHAR.name
        return error_state(token_type, token_value, char)
    else:
        token_type = globals.Globals.LESS_THAN.name
        token_value = token_value[:len(token_value) - 1]
    return final_state(start_token_pointer, token_type, token_value)


def next_token():
    "Get next token, create then return it."

    char = CHARACTERS_LIST[globals.pointer_digit][0]
    matched_token = None

    if is_white_space(char):
        next_idx()
    elif is_invalid_char(char):
        matched_token = invalid_character_tokenizer(char)
    elif is_letter(char):
        matched_token = id_tokenizer(char)
    elif is_quotation(char):
        matched_token = string_tokenizer(char)
    elif is_digit(char):
        matched_token = rational_number_tokenizer(char)
    elif is_star(char):
        matched_token = multiply_or_pow_tokenizer(char)
    elif is_slash(char):
        matched_token = division_operator_tokenizer(char)
    elif char == "<":
        matched_token = less_than_operator_tokenizer(char)
    else:
        next_idx()
        # UNKNOWN_CHAR = globals.Globals.UNKNOWN_CHAR.value
        # matched_token = error_state(UNKNOWN_CHAR, char, char) # It returns error token

    return matched_token
