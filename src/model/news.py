import uuid
from datetime import datetime

class News():
    def __init__(self, title, href, paragraphs, website_name, website_photo, datetime_object):
        self.id = str(uuid.uuid4())
        self.title = title
        self.href = href
        self.website_name = website_name
        self.website_photo = website_photo
        self.paragraphs = paragraphs
        self.created_at = datetime_object