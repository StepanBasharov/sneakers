from typing import List

from app.database.db import db
from app.tools.excel_reader import ModelSniker

from peewee import Model, CharField

class ModelSneaker(Model):
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


    class Meta:
        database = db 




def init_db():
    db.connect()
    db.create_tables([ModelSneaker])
    db.close()


def search(brand= None, model= None, color= None, size= None, condition= None, city= None, fitting= None, article = None):
    query = [
        ]
    if brand:
        query.append(ModelSneaker.brand == brand.lower())
    if model:
        query.append(ModelSneaker.model == model.lower())
    if color:
        query.append(ModelSneaker.color == color.lower())
    if size:
        query.append(ModelSneaker.size == size.lower())
    if condition:
        query.append(ModelSneaker.condition == condition.lower())
    if city:
        query.append(ModelSneaker.city == city.lower())
    if fitting:
        query.append(ModelSneaker.fitting == fitting.lower())
    if article:
        query.append(ModelSneaker.article == article.lower())
    print(query)
    data = ModelSneaker.select().where(*query)
    return data

    



