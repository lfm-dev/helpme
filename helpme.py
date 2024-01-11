#!/usr/bin/python3
import os
import sys
from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown


GUIDES_PATH = '/path/to/your/guides/folder'

class Guide:
    '''
    Class for a markdown how-to guide
    '''
    def __init__(self, filename: str, path: str, guides_path: str) -> None:
        self.filename = filename
        self.path = os.path.join(path, self.filename)
        self.partial_path = path.replace(guides_path, '')
        self.keywords = self.get_partial_path_split() + self.get_filename_split()

    def get_filename_split(self) -> str:
        return self.filename[:self.filename.rfind('.')].split('_')

    def get_partial_path_split(self) -> str:
        return self.partial_path.lstrip('/').split('/')

    def get_guide_content(self) -> str:
        with open(self.path, 'r') as f:
            guide_text = f.read()
        guide_text = self.color_to_comments(guide_text)
        return guide_text

    def color_to_comments(self, guide_text: str) -> str:
        guide_text_lines = guide_text.split('\n')
        code_block = False
        for line_index, line in enumerate(guide_text_lines):
            if line.strip().startswith('```'):
                code_block = not code_block
            elif code_block: # comments in code are rendered with the specific lexer
                continue
            if not line.startswith('#') and '# ' in line:
                guide_text_lines[line_index] = f'{line[:line.find(" #")]} `{line[line.find(" #")+1:]}`' # so it is recognized as a python inline code block
        guide_text = ('\n').join(guide_text_lines)
        return guide_text

def print_chosen_guide_content(guide: Guide) -> None:
    '''
    Prints the content of the .md file with format
    '''
    guide_text = guide.get_guide_content()
    console = Console()
    md = Markdown(guide_text, inline_code_lexer='Python', inline_code_theme='rrt')
    console.print(md)
    print() # empty line at EOF

def print_hits(hits: list[Guide]) -> None:
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

def get_queries() -> list[str]:
    queries = sys.argv[1:]
    if not queries:
        print_help()
    return queries

def print_help() -> None:
    print('Usage: helpme query1 query2 ...')
    print('       helpme all (shows all guides)')
    sys.exit(1)

def all_queries_in_guide_keywords(queries: list[str], keywords: list[str]) -> bool:
    for query in queries:
        if query.casefold() not in keywords:
            return False
    return True

def get_hits(queries: list[str]) -> list[Guide]:
    '''
    Walks by the guides directory and searches for the user queries
    Query can be in the name of the .md file or in the directory name
    Returns a list of Guide objects
    '''
    hits = []
    for path, _, files in sorted(os.walk(GUIDES_PATH)):
        for filename in files:
            guide = Guide(filename, path, GUIDES_PATH)
            if 'all' in queries: # all guides are appended
                hits.append(guide)
                continue
            if all_queries_in_guide_keywords(queries, guide.keywords):
                hits.append(guide)

    return hits

def main():
    os.chdir(GUIDES_PATH)
    queries = get_queries()

    hits = get_hits(queries)
    if not hits:
        print('No hits found.')
        sys.exit(0)
    if len(hits) == 1:
        print_chosen_guide_content(hits[0])
    else:
        print_hits(hits)
        chosen_guide_index = get_chosen_guide_index(max_guide_index = len(hits))
        print_chosen_guide_content(hits[chosen_guide_index])

if __name__ == '__main__':
    main()