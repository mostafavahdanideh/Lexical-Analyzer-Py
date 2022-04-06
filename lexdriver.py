

from utils import next_token, write_error, write_token
from globals import Globals


def main():
    idx = 0

    while idx < Globals.LEN_CHARACTER_LIST.value - 1:
        
        next_token_tpl = next_token()
        created_token_obj = next_token_tpl[1]

        if created_token_obj:

            if created_token_obj.error:
                write_error(created_token_obj.token_type, created_token_obj.value,
                            created_token_obj.location, created_token_obj.error_char)
            else:
                write_token(created_token_obj.token_type,
                            created_token_obj.value, created_token_obj.location)
        
        idx = next_token_tpl[0]

if __name__ == "__main__":
    main()
