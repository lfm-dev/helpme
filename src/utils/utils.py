import os
from classes.Guide import Guide
from view.print_content import print_hits
from usr_input.get_usr_input import get_chosen_guide_index

def get_hits(queries: list[str], guides_path: str) -> list[Guide]:
    '''
    Walks by the guides directory and searches for the user queries
    Query can be in the name of the .md file or in the directory name
    Returns a list of Guide objects
    '''
    hits = []
    for path, _, files in sorted(os.walk(guides_path)):
        files = [xfile for xfile in files if xfile.endswith('.md')]
        for filename in files:
            guide = Guide(filename, path, guides_path)
            if 'all' in queries or guide.all_queries_in_keywords(queries):
                hits.append(guide)
    return hits

def get_guide_index(hits: list[Guide]) -> int:
    if len(hits) == 1:
        guide_index = 0
    else:
        print_hits(hits)
        guide_index = get_chosen_guide_index(max_guide_index = len(hits))
    return guide_index

def open_text_editor(guides_path: str, edit_cmd: str):
    os.system(edit_cmd.replace('%path', guides_path))
