from peewee import IntegerField, CharField, TextField
from model.BaseModel import BaseModel


class Resource(BaseModel):
    title = CharField(default='')
    markdowm = TextField(default='')
    html = TextField(default='')
    disable_count = IntegerField(default=0)
    save_count = IntegerField(default=0)
