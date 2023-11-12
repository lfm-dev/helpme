#!/usr/bin/python3
import os
import sys
from rich.table import Table
from rich.console import Console

def check_path(path):
    if path == '/path/to/your/guides/folder':
        print('You need to write the path to your guide`s folder')
        print("Modify this line -> guides_path = '/path/to/your/guides/folder'")
        print('Run the following command:')
        print('  nano /usr/local/bin/helpme')
        sys.exit(0)

def print_file_content(fullpath):
    # TODO offer to print another related file
    print()
    handle = open(fullpath)
    for n, line in enumerate(handle):
        if n == 0:
            print(f'\033[1m{line.rstrip()}\033[0m') # title in bold
        else:
            print(line.rstrip())
    handle.close()

def print_hits(hits):
    table = Table(show_header=True, header_style='bold green')
    table.add_column('ID', justify='left')
    table.add_column('Path', justify='left')
    table.add_column('Name', justify='left')
    for id_, hit in enumerate(hits):
        table.add_row(str(id_), hit[0], hit[1])
    console = Console()
    console.print(table)

def get_guide_id(max_file_number):
    while True:
        try:
            file_number = int(input('ID: '))
            if file_number in range(max_file_number):
                return file_number
            else:
                print('Wrong ID, try again.')
        except ValueError:
            print('ID can only be numbers.')

def get_query():
    try:
        query = sys.argv[1]
        return query
    except IndexError:
        print('Usage: helpme query')
        sys.exit(1)

def get_hits(query, guides_path):
    hits = []
    for path, _, filenames in os.walk(guides_path):
        partial_path = path.replace(guides_path, '')
        for filename in filenames:
            if query.casefold() in filename.casefold():
                hits.append((partial_path, filename, os.path.join(path, filename)))
    return hits

def main():
    guides_path = '/path/to/your/guides/folder'
    check_path(guides_path)
    os.chdir(guides_path)
    query = get_query()

    hits = get_hits(query, guides_path)
    if hits:
        print_hits(hits)
        file_index = get_guide_id(max_file_number = len(hits))
        file_fullpath = hits[file_index][2]
        print_file_content(file_fullpath)
    else:
        print('No hits found.')
        sys.exit(0)

if __name__ == '__main__':
    main()