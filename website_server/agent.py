from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SITES_DIR = BASE_DIR / "sites"

class ChatBot:
    def __init__(self, site: str):
        content_file = SITES_DIR / site / "content.md"
        if content_file.exists():
            with open(content_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            raise ValueError(f"Content file not found for site '{site}'")
        self.site = site
        self.content = content

    def respond(self, message):
        return f"I received your message '{message}', {self.site} , {self.content}"
    
