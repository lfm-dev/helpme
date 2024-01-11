#!/usr/bin/python3
import os
import sys
from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown


class Guide:
    def __init__(self, filename: str, path: str, guides_path: str):
        self.filename = filename
        self.path = os.path.join(path, self.filename)
        self.partial_path = path.replace(guides_path, '')
        self.keywords = self.get_partial_path_split() + self.get_filename_split()

    def get_filename_split(self):
        return self.filename[:self.filename.rfind('.')].split('_')

    def get_partial_path_split(self):
        return self.partial_path.lstrip('/').split('/')

def color_to_comments(guide_text):
    guide_text = guide_text.split('\n')
    code_block = False
    for line_index, line in enumerate(guide_text):
        if line.strip().startswith('```'):
            code_block = not code_block
        elif code_block: # comments in code are rendered with the specific lexer
            continue
        if not line.startswith('#') and '# ' in line:
            guide_text[line_index] = f'{line[:line.find(" #")]} `{line[line.find(" #")+1:]}`'
    guide_text = ('\n').join(guide_text)
    return guide_text

def print_chosen_guide_content(fullpath: str):
    '''
    Prints the content of the .md file with format
    '''
    with open(fullpath, 'r') as f:
        file_text = f.read()
    file_text = color_to_comments(file_text)
    console = Console()
    md = Markdown(file_text, inline_code_lexer='Python', inline_code_theme='rrt')
    console.print(md)
    print() # empty line at EOF

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

def get_queries() -> list:
    queries = sys.argv[1:]
    if queries:
        return queries
    print_help()

def print_help():
    print('Usage: helpme query1 query2 ...')
    print('       helpme all (shows all guides)')
    sys.exit(1)

def all_queries_in_guide_keywords(queries: list, keywords: list) -> bool:
    for query in queries:
        if query.casefold() not in keywords:
            return False
    return True

def get_hits(queries: list, guides_path: str) -> list:
    '''
    Walks by the guides directory and searches for the user queries
    Query can be in the name of the .md file or in the directory name
    Returns a list of Guide objects
    '''
    hits = []
    for path, _, files in sorted(os.walk(guides_path)):
        for filename in files:
            guide = Guide(filename, path, guides_path)
            if 'all' in queries: # all guides are appended
                hits.append(guide)
                continue
            if all_queries_in_guide_keywords(queries, guide.keywords):
                hits.append(guide)

    return hits

def main():
    guides_path = '/path/to/your/guides/folder'
    os.chdir(guides_path)
    queries = get_queries()

    hits = get_hits(queries, guides_path)
    if not hits:
        print('No hits found.')
        sys.exit(0)
    if len(hits) == 1:
        print_chosen_guide_content(hits[0].path)
    else:
        print_hits(hits)
        chosen_guide_index = get_chosen_guide_index(max_guide_index = len(hits))
        print_chosen_guide_content(hits[chosen_guide_index].path)

if __name__ == '__main__':
    main()