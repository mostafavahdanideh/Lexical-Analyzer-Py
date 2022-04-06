

from globals import Globals, pointer_digit


CHARACTERS_LIST = Globals.CHARACTERS_LIST.value
LEN_CHARACTER_LIST = Globals.LEN_CHARACTER_LIST.value


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
        

def write_token(type, value, location):
    with open("originalfile.outlextokens.txt", "a") as handler:
        handler.write(f"<{type}, {value}, {location}>\n")


def write_error(type, value, location, error_char):
    with open("originalfile.outlexerrors.txt", "a") as handler:
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


def is_under_line(char):
    if char == "_":
        return True
    return False


def is_dot(char):
    if char == ".":
        return True
    return False


def reach_to_finisher_char(char):
    while char:
        if char in [";", "{", ":"]:
            break
        elif end_of_chars_list():
            return "EOF"
        char = next_char_tpl()[0]


def error_token_location(start_token_pointer, char):
    if reach_to_finisher_char(char) == "EOF":
        character_end_loc = "EOF"
        line_number = CHARACTERS_LIST[start_token_pointer][1]
    else:
        character_end_loc = CHARACTERS_LIST[pointer_digit][2] + 1
        line_number = CHARACTERS_LIST[pointer_digit][1]

    character_start_loc = CHARACTERS_LIST[start_token_pointer][2] + 1
        
    character_location_in_line = (
        character_start_loc,
        character_end_loc)

    location_tpl = (
        line_number,
        character_location_in_line)
    
    return location_tpl


def token_location(start_token_pointer):
    line_number = CHARACTERS_LIST[pointer_digit][1]
    character_start_loc = CHARACTERS_LIST[start_token_pointer][2] + 1
    character_end_loc = CHARACTERS_LIST[pointer_digit][2]

    character_location_in_line = (
        character_start_loc,
        character_end_loc)

    location_tpl = (
        line_number,
        character_location_in_line)

    return location_tpl


def match_id_token(char):
    start_token_pointer, id_value = pointer_digit, char

    while is_digit(char) or is_letter(char) or is_under_line(char):
        char = next_char_tpl()[0]

        if end_of_chars_list():
            break

        id_value = make_up_token_value(id_value, char)
        
    if is_invalid_char(char) or is_dot(char):
        location_tpl = error_token_location(start_token_pointer, char)
        return ErrorToken("ID", id_value, location_tpl, True, char)
    
    location_tpl = token_location(start_token_pointer)
    id_value = id_value[:len(id_value) - 1]
    return Token("ID", id_value, location_tpl, False)


def make_up_token_value(pre_value, next_value):
    "concatinating string, id, integer and float value"
    pre_value += next_value
    return pre_value


def end_of_chars_list():
    if pointer_digit + 1 == LEN_CHARACTER_LIST:
        return True
    return False


def next_char_tpl():
    global pointer_digit

    if not(end_of_chars_list()):
        pointer_digit += 1

    return CHARACTERS_LIST[pointer_digit]


def next_idx():
    global pointer_digit
    if not(end_of_chars_list()):
        pointer_digit += 1


def is_quotation(char):
    if char == '"':
        return True
    return False


def is_space(char):
    if char == " ":
        return True
    return False

def match_string_token(char):
    start_token_pointer, string_value = pointer_digit, char

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
    start_token_pointer = pointer_digit
    location_tpl = error_token_location(start_token_pointer, char)
    invalid_char_value = f"{CHARACTERS_LIST[start_token_pointer][0]}...{CHARACTERS_LIST[pointer_digit][0]}"
    return ErrorToken("INVALID_CHAR", invalid_char_value, location_tpl, True, char)


def next_token():
    "Get next token, create then return it."

    global pointer_digit
    char = CHARACTERS_LIST[pointer_digit][0]

    if is_letter(char):
        matched_token = match_id_token(char)

    elif is_invalid_char(char):
        matched_token = match_invalid_chars(char)

    elif is_quotation(char):
        matched_token = match_string_token(char)
    else:
        pointer_digit += 1
        matched_token = None
    
    return pointer_digit, matched_token
