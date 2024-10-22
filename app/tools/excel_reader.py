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
            brand=row['Бренд'],
            model=row['Модель'],
            color=row['Цвет'],
            size=row['Размер'],
            price=row['Цена'],
            article=row['Артикул'],
            condition=row['Состояние'],
            city=row['Город'],
            place=row['Местоположение'],
            fitting=row['Примерка'],
            vendor=row['Продавец']
            )
        sneakers.append(sneaker)


    return sneakers