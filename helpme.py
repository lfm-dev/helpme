#!/usr/bin/python3
import os
import sys
from rich.table import Table
from rich.console import Console

class Guide():
    def __init__(self, filename, path, partial_path):
        self.filename = filename
        self.partial_path = partial_path
        self.path = os.path.join(path, self.filename)

def print_file_content(fullpath):
    '''
    Prints the content of the .md file with format
    '''
    # TODO offer to print another related file
    handle = open(fullpath)
    print('')
    for line in handle:
        line = line.rstrip()
        if line.startswith('##'):
            print(f'\033[1m{line.lstrip("## ")}\033[0m') # subtitles in bold
            continue
        elif line.startswith('#'):
            print(f'\033[4;37m\033[1m{line.lstrip("# ")}\033[0m') # titles in bold and underlined
            continue
        elif ' #' in line: # line has comments
            print(f'{line[:line.find(" #")]} \033[0;32m{line[line.find(" #"):]}\033[0m') # comments in green
        else:
            print(line)
    if line: # only if the .md file doesnt have empty lines at the end
        print('')
    handle.close()

def print_hits(hits):
    table = Table(show_header=True, header_style='bold green')
    table.add_column('ID', justify='left')
    table.add_column('Path', justify='left')
    table.add_column('Name', justify='left')
    for id_, hit in enumerate(hits):
        table.add_row(str(id_), hit.partial_path, hit.filename)
    table.add_row(str(id_+1), "exit", "")
    console = Console()
    console.print(table)

def get_guide_id(max_file_number):
    while True:
        try:
            file_number = int(input('ID: '))
            if file_number in range(max_file_number):
                return file_number
            elif file_number == max_file_number: # exit
                sys.exit(0)
            else:
                print('Wrong ID, try again.')
        except ValueError:
            print('ID can only be numbers.')

def get_query():
    '''
    Gets query from argv. If no query -> shows help
    '''
    try:
        query = sys.argv[1]
        return query
    except IndexError:
        print('Usage: helpme query')
        sys.exit(1)

def get_hits(query, guides_path):
    '''
    Walks by the guides directory and searches for the user query
    File names are separated by _
    Query can be in the name of the .md file or in the directory name
    Returns a list of tuples -> [(partial_path, file_name, full_path)]
    if query == "all" -> returns a list with all .md files
    '''
    query = query.casefold()
    hits = []
    for path, _, files in os.walk(guides_path):
        partial_path = path.replace(guides_path, '')
        partial_path_split = partial_path.casefold().split('/')
        for filename in files:
            filename_split_noext = filename[:filename.rfind('.')].casefold().split('_')
            if query in filename_split_noext or query in partial_path_split or query == 'all'.casefold():
                hit = Guide(filename, path, partial_path)
                hits.append(hit)
    return hits

def main():
    guides_path = '/path/to/your/guides/folder'
    os.chdir(guides_path)
    query = get_query()

    hits = get_hits(query, guides_path)
    if hits:
        print_hits(hits)
        file_index = get_guide_id(max_file_number = len(hits))
        file_fullpath = hits[file_index].path
        print_file_content(file_fullpath)
    else:
        print('No hits found.')
        sys.exit(0)

if __name__ == '__main__':
    main()