# from message_parts import get_message
from woocommerce import API

wcapi = API(
    url="https://mining4-you.com/",
    consumer_key="ck_c108305d724ec87d49c07bff46debc5356e493ef",
    consumer_secret="cs_293377acb30b49b0e7917c77617fa798859b13a6",
)


def api_minerinfo(id):
    minerinfo = wcapi.get(f'products/{id}').json()
    return minerinfo['name']

def api_miners(id):
    prods = wcapi.get(f'products/{id}').json()
    try:
        prods = prods[0]['slug']
    except IndexError:
        prods = '0'

    return prods

def api_minerenergy(id):
    minerenergy = wcapi.get(f'products/{id}').json()
    for th in minerenergy['attributes']:
        if th['id'] == 9:
            return float(th['options'][0])
    # if calcin == "antminer-s19-10" or calcin == "whatsminer-m50":
    #     return float(minerenergy[0]['attributes'][0]['options'][0])/1000
    # elif calcin == "whatsminer-m31s-5":
    #     return minerenergy[0]['attributes'][0]['options'][0]
    # elif calcin == "antminer-s19xp" or calcin == "antminer-s19j-pro-110th" or calcin == "antminer-s19j-pro-104th" or calcin == "antminer-s19j-pro-100th" or calcin == "antminer-s19-7" or calcin == "antminer-s19-2" or calcin == "whatsminer-m30s-7" or calcin == "whatsminer-m30s-6" or calcin == "whatsminer-m30s-5" or calcin == "whatsminer-m30s-4" or calcin == "whatsminer-m30s-3" or calcin == "whatsminer-m30s-2" or calcin == "whatsminer-m30s" or calcin == "whatsminer-m31s-3" or calcin == "whatsminer-m31s-2" or calcin == "whatsminer-m31s-4" or calcin == "whatsminer-m21s-5" or calcin == "whatsminer-m21s-3" or calcin == "whatsminer-m21s-2" or calcin == "whatsminer-m21s":
    #     return minerenergy[0]['attributes'][1]['options'][0]
    # else:
    #     return minerenergy[0]['attributes'][2]['options'][0]

def api_minerth(id):
    minerth = wcapi.get(f'products/{id}').json()
    for th in minerth['attributes']:
        if th['id'] == 5:
            return th['options'][0]
    # if calcin == "antminer-s19-10" or calcin == "whatsminer-m50" or calcin == "whatsminer-m30s-8" or calcin == "whatsminer-m31s-5":
    #     return minerth[0]['attributes'][1]['options'][0]
    # elif calcin == "whatsminer-m31s-4":
    #     return minerth[0]['attributes'][2]['options'][0]
    # else:
    #     return minerth[0]['attributes'][0]['options'][0]

def api_minercost(id, currency):
    datacost = wcapi.get(f'products/{id}').json()
    target_lang = 'ru' if currency == 'RUB' else 'en'
    if datacost['lang'] in ['ru', 'en'] and datacost['lang'] == target_lang:
        return int(datacost['price'])
    else:
        for lang, value in datacost['translations'].items():
            if lang in ['ru', 'en'] and lang == target_lang:
                datacost = wcapi.get(f'products/{value}').json()
                return int(datacost['price'])
                

        

    return None  # Return None if translation not found or currency doesn't match

def api_minersell(id,currency):
    datacost = wcapi.get(f'products/{id}').json()
    target_lang = 'ru' if currency == 'RUB' else 'en'
    if datacost['lang'] in ['ru', 'en'] and datacost['lang'] == target_lang:
        return float(datacost['price'])
    else:
        for lang, value in datacost['translations'].items():
            if lang in ['ru', 'en'] and lang == target_lang:
                datacost = wcapi.get(f'products/{value}').json()
                return float(datacost['price'])

def get_all_products(lang):
    all_ru_products = wcapi.get('products?per_page=100&category=599,611', params={'lang': f'{lang}'}).json()
    return all_ru_products
    
if __name__ == '__main__':
    import requests

    url = "https://api.amocrm.ru/v4/leads"
    headers = {
        "Authorization": "EOuNI2CQE1e5IxVlIVvr5StuRdLDkScQULEkeZ8VY5B7O66Zuiu9EeCeP7prjV9b",
        "Content-Type": "application/json"
    }

    data = {
        "name": "Тестовая сделка",
        "status_id": 142,  # Замените на нужный ID статуса сделки
        "price": 1000,
        "contacts_id": [123]  # Замените на нужный ID контакта
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:  # 201 - код успешного создания
        print("Сделка успешно создана")
    else:
        print("Произошла ошибка:", response.text)

    


    