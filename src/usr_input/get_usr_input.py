import sys
from view.print_content import print_help

def get_chosen_guide_index(max_guide_index: int) -> int:
    while True:
        try:
            chosen_guide_index = int(input('ID: '))
        except ValueError:
            print('ID can only be numbers.')
        else:
            if chosen_guide_index in range(max_guide_index):
                return chosen_guide_index
            if chosen_guide_index == max_guide_index: # exit
                sys.exit(0)
            else:
                print('Wrong ID, try again.')

def get_queries() -> list[str]:
    queries = sys.argv[1:]
    if not queries:
        print_help()
    return queries
