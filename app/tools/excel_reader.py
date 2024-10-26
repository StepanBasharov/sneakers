from typing import List
import pandas as pd


class ModelSniker:
    def __init__(
        self,
        brand: str,
        model: str,
        color: str,
        size: str,
        price: str,
        article: str,
        condition: str,
        city: str,
        place: str,
        fitting: str,
        vendor: str
    ) -> None:
        self.brand = brand
        self.model = model
        self.color = color
        self.size = size
        self.price = price
        self.article = article
        self.condition = condition
        self.city = city
        self.place = place
        self.fitting = fitting
        self.vendor = vendor

def load_from_excel(file_path: str) -> List[ModelSniker]:


    data = pd.read_excel(file_path)

    sneakers: list[ModelSniker] = []
    for index, row in data.iterrows():
        sneaker = ModelSniker(
            brand=str(row['Бренд']).lower(),
            model=str(row['Модель']).lower(),
            color=str(row['Цвет']).lower(),
            size=str(row['Размер']).lower(),
            price=str(row['Цена']).lower(),
            article=str(row['Артикул']).lower(),
            condition=str(row['Состояние']).lower(),
            city=str(row['Город']).lower(),
            place=str(row['Местоположение']).lower(),
            fitting=str(row['Примерка']).lower(),
            vendor=str(row['Продавец'])
            )
        sneakers.append(sneaker)


    return sneakers