import sqlalchemy as sqlalchemy
from model.news import News
import yaml
import uuid
from datetime import datetime

# Load the config file into memory
config = yaml.safe_load(open("config.yml"))


class Database():
    user = config['DB_USER']
    password = config['DB_PASS']
    hostname = 'b3-news-db.postgres.database.azure.com'
    database_name = 'postgres'
    full_string = f'postgresql://{user}:{password}@{hostname}/{database_name}'
    print(full_string)
    engine = sqlalchemy.create_engine(full_string)

    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")

    def save(self, news):
        self.save_news(news)
        self.save_paragraphs(news)

    def save_news(self, news):
        self.connection.execute(sqlalchemy.text(f"""INSERT INTO news(id, title, href, created_at) 
                                    VALUES('{news.id}', '{news.title}', '{news.href}', '{news.created_at}')"""))

    def save_paragraphs(self, news):
        for paragraph in news.paragraphs:
            self.connection.execute(sqlalchemy.text(f"""INSERT INTO paragraphs(id, text, news_id, created_at)
                                        VALUES('{str(uuid.uuid4())}', '{paragraph}', '{news.id}', '{datetime.now()}')"""))


if __name__ == "__main__":
    db = Database()
    db.save(News('título de teste', 'https://aefaef.com.br',
                 ['paragrafo 1', 'paragrafo 2', 'paragrafo 3']))
