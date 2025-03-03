from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from .import_stat import match_import
from .clear_stat import match_clear

class ImportStatPlugin(BasePlugin):
    def on_page_markdown(self, markdown: str, page: Page, **kwargs):
        lines = markdown.split("\n")
        opt = False
        for i, line in enumerate(lines):
            res = match_clear(line)
            if res:
                opt = True
                lines[i] = res
                continue
            res = match_import(line, page)
            if not res:
                continue
            lines[i] = res
            opt = True
            
        if opt:
            markdown = "\n".join(lines) 
        
        return markdown
