import sqlalchemy as sqlalchemy
from model.news import News
import yaml
import uuid
from datetime import datetime

config = yaml.safe_load(open("config.yml"))


class Database():
    user = config['DB_USER']
    password = config['DB_PASS']
    hostname = config['DB_HOST']
    database_name = config['DATABASE_NAME']
    full_string = f'postgresql://{user}:{password}@{hostname}/{database_name}'
    engine = sqlalchemy.create_engine(full_string)

    def __init__(self):
        self.connection = self.engine.connect()

    def get_fetched_links(self):
        fetchQuery = self.connection.execute(f"SELECT href FROM news")
        return list(map(lambda x: x.href, fetchQuery.fetchall()))

    def save_all_news(self, news):
        for el in news:
            self.save_news(el)
            self.save_paragraphs(el)

    def save_news(self, news):
        self.connection.execute(sqlalchemy.text(f"""INSERT INTO news(id, title, href, website_name, website_photo, created_at) 
                                    VALUES('{news.id}', '{news.title}', '{news.href}', '{news.website_name}', '{news.website_photo}', '{news.created_at}')"""))

    def save_paragraphs(self, news):
        for paragraph in news.paragraphs:
            self.connection.execute(sqlalchemy.text(f"""INSERT INTO paragraphs(id, text, news_id, created_at)
                                        VALUES('{str(uuid.uuid4())}', '{paragraph}', '{news.id}', '{datetime.now()}')"""))
