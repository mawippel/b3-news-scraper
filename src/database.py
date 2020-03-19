import sqlalchemy as db
from model.news import News
import yaml

# Load the config file into memory
config = yaml.safe_load(open("config.yml"))

class Database():
    user = config['DB_USER']
    password = config['DB_PASS']
    hostname = 'b3-news-db.postgres.database.azure.com'
    database_name = 'postgres'
    full_string = f'postgresql://{user}:{password}@{hostname}/{database_name}'
    print(full_string)
    engine = db.create_engine(full_string)

    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")

    def saveData(self, news):
        self.connection.execute(f"""INSERT INTO news(id, title, href, created_at) 
                                    VALUES('{news.id}', '{news.title}', '{news.href}', '{news.created_at}')""")

if __name__ == "__main__":
    db = Database()
    db.saveData(News('título de teste', 'https://aefaef.com.br'))