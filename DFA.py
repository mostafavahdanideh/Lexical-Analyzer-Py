

def get_characters():
    characters = list()

    with open("originalfilename.txt", "r") as handler:
        while True:
            char = handler.read(1)
            if not char:
                break
            else:
                characters.append(char)
    return characters


def write_token(type, value):
    with open("originalfile.outlextokens.txt", "a") as handler:
        handler.write(f"<{type}, {value}>\n")
    

def write_error(type, value, line):
    with open("originalfile.outlexerrors.txt", "a") as handler:
        handler.write(f"<{type}, {value}, {line}>\n")


def finisher_char_idx(chars_lst, idx):
    char  = chars_lst[idx]
    while char not in [";", "{", "\n", ":"]:
        idx += 1
        char = chars_lst[idx]
    return idx


def is_char_invalid(char):
    if char in ["#", "$", "~", "`"]:
        return True
    return False


def next_token():
    characters_lst = get_characters()
    idx, line_number, len_characters_lst = 0, 1, len(characters_lst)

    while idx < len_characters_lst - 1:
        char = characters_lst[idx]

        if char == "\n":
            line_number += 1
        
        # ID_DFA
        if char.isalpha():
            id_value = char

            while char.isalnum() or char == "_":
                idx += 1
                char = characters_lst[idx]
                id_value += char

            if char == "." or char =='"' or is_char_invalid(char):
                idx = finisher_char_idx(characters_lst, idx)
                write_error("ID", id_value, line_number)
            else:
                write_token("ID", id_value[:idx].strip())

            idx - 1 #BackTrack => Back to previous character
        
        #String_DFA
        elif char == '"':
            string_value = char
            idx += 1
            char = characters_lst[idx]
            string_value += char
            while char.isalnum() or char.isspace():
                idx += 1
                char = characters_lst[idx]
                string_value += char
            if char == '"':
                write_token("String", string_value[:idx])
            else:
                idx = finisher_char_idx(characters_lst, idx)
                write_error("String", string_value, line_number)
            idx - 1
        idx += 1

next_token()
