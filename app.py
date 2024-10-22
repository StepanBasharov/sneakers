from app.tools import excel_reader
from app.database.models import init_db, close_db,  ModelSniker

data = excel_reader.load_from_excel("./table.xlsx")
init_db()

for sniker in data:
    ModelSniker.create(
        brand=sniker.brand,
        model=sniker.model,
        color=sniker.color,
        size=sniker.size,
        price=sniker.price,
        article=sniker.article,
        condition=sniker.condition,
        city=sniker.city,
        place=sniker.place,
        fitting=sniker.fitting,
        vendor=sniker.vendor
    )


nike_sneakers = ModelSniker.select().where(ModelSniker.brand == "Nike")

for i in nike_sneakers:
    print(i)