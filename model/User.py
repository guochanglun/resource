from peewee import CharField, ManyToManyField
from model.BaseModel import BaseModel
from model.Resource import Resource


class User(BaseModel):
    username = CharField(default='dog')
    password = CharField(default='dog')
    desc = CharField()
    saved = ManyToManyField(Resource)