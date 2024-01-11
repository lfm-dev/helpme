#!/usr/bin/python3
import os
import sys
from classes.Guide import Guide
from view.print_content import print_chosen_guide_content, print_hits
from usr_input.get_usr_input import get_queries, get_chosen_guide_index


GUIDES_PATH = '/path/to/your/guides/folder'

#TODO unit tests
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
            if 'all' in queries or guide.all_queries_in_keywords(queries):
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