from peewee import *
import yaml

# Load the config file into memory
config = yaml.safe_load(open("config.yml"))

db = PostgresqlDatabase(
    'postgres',
    user=config['DB_USER'],
    password=config['DB_PASS'],
    host='b3-news-db.postgres.database.azure.com')

class MySQLModel(Model):
    # A base model that will use our MySQL database
    class Meta:
        database = db


class News(MySQLModel):
    id = IdentityField()
    title = CharField()
    site = CharField()
    score = CharField()
    lastUpdated = DateTimeField()


def insertNews(news):
    db.connect()
    news.save()
    db.close()


if __name__ == "__main__":
    insertNews(News())
