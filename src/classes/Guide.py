import os

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

    def all_queries_in_keywords(self, queries: list[str]) -> bool:
        for query in queries:
            if query.casefold() not in self.keywords:
                return False
        return True

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