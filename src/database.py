import sqlalchemy as sqlalchemy
from model.news import News
import yaml
import uuid
from datetime import datetime
import pyodbc
import urllib

config = yaml.safe_load(open("config.yml"))


class Database():
    server = "db-b3-news.database.windows.net"
    database = "db-b3-news"
    username = "mawippel"
    password = "Ivangoezeli14"

    driver = '{SQL Server}'

    odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID=' + \
        username+';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + \
        urllib.parse.quote_plus(odbc_str)
    engine = sqlalchemy.create_engine(connect_str)

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
                                        VALUES('{str(uuid.uuid4())}', :paragraph, '{news.id}', '{datetime.now()}')"""), paragraph = paragraph)
