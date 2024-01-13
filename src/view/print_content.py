import sys
from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown
from classes.Guide import Guide

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
        end_section = True if id_ == len(hits)-1 else hit.partial_path != hits[id_+1].partial_path
        table.add_row(str(id_), hit.partial_path, hit.filename, end_section=end_section)
    table.add_row(str(id_+1), "exit", "")
    console = Console()
    console.print(table)

def print_help() -> None:
    print('Usage: helpme query1 query2 ...')
    print('       helpme all (shows all guides)')
    sys.exit(1)