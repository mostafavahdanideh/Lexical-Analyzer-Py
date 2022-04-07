

def main():

    import globals
    from utils import write_error, write_token
    from tokenization import next_token

    LEN_CHARACTER_LIST = globals.LEN_CHARACTER_LIST
    index = globals.pointer_digit

    while index < LEN_CHARACTER_LIST - 1:
        
        created_token_obj = next_token()

        if created_token_obj:

            if created_token_obj.error:
                write_error(created_token_obj.token_type, created_token_obj.value,
                            created_token_obj.location, created_token_obj.error_char)
            else:
                write_token(created_token_obj.token_type,
                            created_token_obj.value, created_token_obj.location)
        
        index = globals.pointer_digit


if __name__ == "__main__":
    main()
