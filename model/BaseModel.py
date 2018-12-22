from playhouse.db_url import connect
from peewee import Model

db = connect('mysql://root:root@localhost:3306/warehouse')


class BaseModel(Model):
    class Meta:
        database = db