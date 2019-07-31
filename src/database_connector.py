import peewee as pw
import yaml

# Load the config file into memory
config = yaml.safe_load(open("config.yml"))

myDB = pw.MySQLDatabase("b3news", host="b3news.chhyfcmj1pi4.us-east-2.rds.amazonaws.com", port=3306, user=config['DB_USER'], passwd=config['DB_PASS'])

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

class Person(MySQLModel):
    id = pw.IdentityField()
    firstname = pw.CharField()
    surname = pw.CharField()


# when you're ready to start querying, remember to connect
# myDB.connect()

if __name__ == "__main__":
    myDB.connect()
    print(Person.select().get())
    myDB.close()