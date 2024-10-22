import sys
import time
import os
from vk_api import longpoll, VkApi
from random import randrange
import pandas as pd
from textdistance import levenshtein

df = pd.read_excel(sys.argv[1])
df = df.rename({'Размер (US)': 'Размер'})
print(df.columns)
def parse_size(s):
    if type(s) == float:
        return s
    if type(s) == int:
        return float(s)
    num = ''.join(filter(lambda c: c.isdigit() or c == '.', s))
    if num != '':
        try:
            return float(num)
        except:
            return 0.0
    if s.strip() == 'XL':
        return 52.0
    return 0.0

df['Размер'] = df['Размер'].transform(parse_size)

def search(query):
    query = query.lower()
    entries = list(filter(lambda s: len(s) != 0, map(lambda t: t.strip(), query.split('\n'))))
    order = df.apply(
        lambda x: levenshtein.distance((str(x['Бренд']) + str(x['Модель']) + str(x['Цвет'])).lower(), entries[1]), axis=1
    ).argsort()
    cands = df.iloc[order]
    try:
        size = float(next(filter(lambda s: 'us' in s, entries)).removesuffix('us').strip())
    except:
        size = None
    if size != None:
        cands = cands.loc[abs(cands['Размер'] - size) <= 0.001]
    if 'новые' in query:
        cands = cands.loc[cands['Состояние'] == 'Новое']
    if 'примерка' in query or 'примеркой' in query:
        cands = cands.loc[cands['Примерка'] == 'Да']
    if len(cands) > 0:
        # if size != None:
        #    cands = cands.iloc[:3].sort_values(by='Размер', key=lambda t: abs(t - size))
        return cands.iloc[0]
    return None

vk = VkApi(token=os.environ['VK_TOKEN'])
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
        try:
            r = search(e.message)
            if r is not None:
                api.messages.send(
                    user_id=e.user_id, random_id=randrange(2**31),
                    message=f'''Модель: {r['Бренд']}  {r['Модель']}
Цвет: {r['Цвет']}
Размер: {r['Размер']}
Артикул: {r['Артикул']}
Цена: {r['Цена']}
Город: {r['Город']}
Местоположение: {r['Местоположение']}
Примерка: {r['Примерка']}
Продавец: {r['Продавец']} 
✅верифицированный продавец''')
        except Exception as e:
            print(e)
            continue
