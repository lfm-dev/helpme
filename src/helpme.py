#!/usr/bin/python3
import os
import sys
from utils.utils import get_hits, get_guide_index, open_text_editor
from view.print_content import print_guide_content
from usr_input.get_usr_input import get_queries


GUIDES_PATH = '/path/to/your/guides/folder'
EDIT_CMD = 'micro %path'

def main():
    edit_mode, queries = get_queries()

    hits = get_hits(queries, GUIDES_PATH)
    if not hits:
        print('No hits found.')
        sys.exit(0)

    guide_index = get_guide_index(hits)

    if edit_mode:
        open_text_editor(hits[guide_index].path, EDIT_CMD)
    else:
        print_guide_content(hits[guide_index])

if __name__ == '__main__':
    main()
