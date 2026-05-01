from peewee import *

db = SqliteDatabase('automatik.db')

class BaseModel(Model):
    class Meta:
        database = db