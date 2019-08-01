import peewee as pw
import yaml

# Load the config file into memory
config = yaml.safe_load(open("config.yml"))

db = pw.MySQLDatabase("b3news", host="b3news.chhyfcmj1pi4.us-east-2.rds.amazonaws.com",
                        port=3306, user=config['DB_USER'], passwd=config['DB_PASS'])


class MySQLModel(pw.Model):
    # A base model that will use our MySQL database
    class Meta:
        database = db


class News(MySQLModel):
    id = pw.IdentityField()
    title = pw.CharField()
    site = pw.CharField()
    score = pw.CharField()
    lastUpdated = pw.DateTimeField()


def insertNews(news):
    db.connect()
    news.save()
    db.close()


if __name__ == "__main__":
    pass
