import time
from app.tools import excel_reader
from app.database.models import init_db, ModelSneaker, search

import time
import os
from vk_api import longpoll, VkApi
from random import randrange

def crop_filter(s: str):
    return s.split(": ")[1].strip()

def main():
    data = excel_reader.load_from_excel("./table.xlsx")
    init_db()
    for sniker in data:
        ModelSneaker.create(
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
    print("Success")
    vk = VkApi(token="vk1.a.Wx7cZFZJAHHcObQRIXNPEHDRK3twNUrdJzp0FN23xm17ZggKqMMN6N0B4YitRp2OM6rEJQBLTqvHk9BsPKThfCY_nwvqY8_tnWH2SInNoJpQVETFFa9rJ2eGjrUhcyUT_-oHz0cJquvyBlse0dUlo_gussDvA9oXyVGv7_P7xBqIL0Ve2hE2Xobv5YTXSuaakFu7YMuxTOd7MviAmN35_Q")
    api = vk.get_api()

    lp = longpoll.VkLongPoll(vk)

    def listen():
        while True:
            try:
                yield from lp.check()
            except:
                pass
            time.sleep(1)

    for e in listen():
        if e.type == longpoll.VkEventType.MESSAGE_NEW and not e.from_me and 'ищу' in e.message.lower():
            search_map = {
                "brand": None, 
                "model": None, 
                "color": None, 
                "size": None, 
                "condition": None, 
                "city": None, 
                "fitting": None, 
                "article": None
            }
            message = e.message.split("\n")
            for i in message:
                if "бренд" in i.lower():
                    search_map["brand"] = crop_filter(i)
                if "модель" in i.lower():
                    search_map["model"] = crop_filter(i)
                if "цвет" in i.lower():
                    search_map["color"] = crop_filter(i)
                if "размер" in i.lower():
                    search_map["size"] = crop_filter(i)
                if "состояние" in i.lower():
                    search_map["condition"] = crop_filter(i)
                if "город" in i.lower():
                    search_map["city"] = crop_filter(i)
                if "примерка" in i.lower():
                    search_map["fitting"] = crop_filter(i)
                if "артикул" in i.lower():
                    search_map["article"] = crop_filter(i)


            sneakers: list[ModelSneaker] = search(**search_map)
            for i in sneakers:
                message = f'''
                    Модель: {i.brand}  {i.model}
                    Цвет: {i.color}
                    Размер: {i.size}
                    Артикул: {i.article}
                    Цена: {i.price}
                    Город: {i.city}
                    Местоположение: {i.place}
                    Примерка: {i.fitting}
                    Продавец: {i.vendor} 
                    ✅верифицированный продавец
                '''
                api.messages.send(
                        user_id=e.user_id, random_id=randrange(2**31),
                        message=message)
                time.sleep(1)

    
    # sneakers: list[ModelSneaker] = search(brand="Nike", model="Air Force 1 Low")
    # for i in sneakers:
    #    message = f'''
    #            Модель: {i.brand}  {i.model}
    #            Цвет: {i.color}
    #            Размер: {i.size}
    #            Артикул: {i.article}
    #            Цена: {i.price}
    #            Город: {i.city}
    #            Местоположение: {i.place}
    #            Примерка: {i.fitting}
    #            Продавец: {i.vendor} 
    #            ✅верифицированный продавец
    #            '''
    #    

    #    print(message)


if __name__ == "__main__":
    main()