import uuid
from datetime import datetime

class News():
    def __init__(self, title, href):
        self.id = str(uuid.uuid4())
        self.title = title
        self.href = href
        self.created_at = datetime.now()