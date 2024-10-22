from typing import List

from app.database.db import db
from app.tools.excel_reader import ModelSniker

from peewee import *

class ModelSniker(Model):
    brand = CharField()
    model = CharField()
    color = CharField()
    size = CharField()
    price = CharField()
    article = CharField()
    condition = CharField()
    city = CharField()
    place = CharField()
    fitting = CharField()
    vendor = CharField()


    def create_from_excel(self, data: List[ModelSniker]):
        print("test")

    class Meta:
        database = db 




def init_db():
    db.connect()
    db.create_tables([ModelSniker])
    db.close()

