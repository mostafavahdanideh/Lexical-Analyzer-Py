

def main():

    import globals
    from utils import write_error, write_token
    from tokenization import next_token

    LEN_CHARACTER_LIST = globals.LEN_CHARACTER_LIST
    index = globals.pointer_digit

    while index < LEN_CHARACTER_LIST - 1:
        
        created_token_dict = next_token()

        if created_token_dict:

            if created_token_dict["error_token"]:
                write_error(created_token_dict["token_type"], created_token_dict["token_value"],
                            created_token_dict["token_location"], created_token_dict["error_char"])
            else:
                write_token(created_token_dict["token_type"],
                            created_token_dict["token_value"], created_token_dict["token_location"])
        
        index = globals.pointer_digit


if __name__ == "__main__":
    main()
