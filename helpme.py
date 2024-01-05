#!/usr/bin/python3
import os
import sys
from rich.table import Table
from rich.console import Console
#TODO search inside files to show just a part of it
class Guide:
    # TODO self.guide_content with formated text
    def __init__(self, filename: str, path: str, guides_path: str):
        self.filename = filename
        self.filename_split = self.get_filename_split()
        self.path = os.path.join(path, self.filename)
        self.partial_path = path.replace(guides_path, '')
        self.partial_path_split = self.get_partial_path_split()

    def get_filename_split(self):
        return self.filename[:self.filename.rfind('.')].split('_')

    def get_partial_path_split(self):
        return self.partial_path.split('/')

def print_chosen_guide_content(fullpath: str):
    '''
    Prints the content of the .md file with format
    '''
    # TODO offer to print another related file
    # TODO * and number. in bold
    with open(fullpath) as handle:
        print('')
        for line in handle:
            line = line.rstrip()
            if line.startswith('##'):
                print(f'\033[1m{line.lstrip("## ")}\033[0m') # subtitles in bold
                continue
            if line.startswith('#'):
                print(f'\033[4;37m\033[1m{line.lstrip("# ")}\033[0m') # titles in bold and underlined
                continue
            if ' #' in line: # line has comments
                print(f'{line[:line.find(" #")]} \033[0;32m{line[line.find(" #"):]}\033[0m') # comments in green
            else:
                print(line)
        if line: # only if the .md file doesnt have empty lines at the end
            print('')

def print_hits(hits: list):
    table = Table(show_header=True, header_style='bold green')
    table.add_column('ID', justify='left')
    table.add_column('Path', justify='left')
    table.add_column('Name', justify='left')
    for id_, hit in enumerate(hits):
        if id_ == len(hits)-1:
            end_section = True
        else:
            end_section = hit.partial_path != hits[id_+1].partial_path
        table.add_row(str(id_), hit.partial_path, hit.filename, end_section=end_section)
    table.add_row(str(id_+1), "exit", "")
    console = Console()
    console.print(table)

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

def get_query() -> str:
    '''
    Gets query (casefold) from argv. If no query -> shows help and exits
    '''
    try:
        query = sys.argv[1].casefold()
        return query
    except IndexError:
        print_help()

def print_help():
    print('Usage: helpme query')
    print('       helpme all (shows all guides)')
    sys.exit(1)

def get_hits(query: str, guides_path: str) -> list:
    '''
    Walks by the guides directory and searches for the user query
    Words in file names are separated by "_", words in path are separated by "/"
    Query can be in the name of the .md file or in the directory name
    Returns a list of Guide objects
    if query == "all" -> every guide is appended
    '''
    hits = []
    for path, _, files in sorted(os.walk(guides_path)):
        for filename in files:
            guide = Guide(filename, path, guides_path)
            if query in guide.filename_split or query in guide.partial_path_split or query == 'all':
                hits.append(guide)
    return hits

def main():
    guides_path = '/path/to/your/guides/folder'
    os.chdir(guides_path)
    query = get_query()

    hits = get_hits(query, guides_path)
    if hits:
        print_hits(hits)
        chosen_guide_index = get_chosen_guide_index(max_guide_index = len(hits))
        print_chosen_guide_content(hits[chosen_guide_index].path)
    else:
        print('No hits found.')
        sys.exit(0)

if __name__ == '__main__':
    main()