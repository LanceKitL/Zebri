from peewee import *

db = SqliteDatabase('zebri.db')

class BaseModel(Model):
    class Meta:
        database = db
        
class Quest(BaseModel):
    title = CharField()
    description = TextField()
    difficulty = CharField() # enum => easy, medium, hard
    is_completed = BooleanField(default=False)

class User(BaseModel):
    name = CharField()
    xp = IntegerField(default=0)
    level = IntegerField(default=1)
    
class CompletionLog(BaseModel):
    quest = ForeignKeyField(Quest)
    completed_at = DateField()

db.connect()
db.create_tables([Quest,User,CompletionLog])
        

