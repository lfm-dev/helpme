import sys
from view.print_content import print_help

def is_int(chosen_guide_index: str) -> bool:
    try:
        chosen_guide_index = int(chosen_guide_index)
        return True
    except ValueError:
        return False

def get_chosen_guide_index(max_guide_index: int) -> int:
    while True:
        chosen_guide_index = input('ID: ')
        if is_int(chosen_guide_index):
            if int(chosen_guide_index) in range(max_guide_index):
                return int(chosen_guide_index)
            if int(chosen_guide_index) == max_guide_index: # exit
                sys.exit(0)
        print('Wrong ID, try again.')

def get_queries() -> list[str]:
    usr_input = sys.argv[1:]
    if not usr_input:
        print_help()
    edit_mode = usr_input[0] == '-e'
    queries = usr_input[1:] if edit_mode else usr_input
    return edit_mode, queries
