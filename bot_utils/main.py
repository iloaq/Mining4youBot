from db import dbase
from .curapibot import currency_data1 as get_currency_data
from .defdatetime import date as get_date,time as get_time
from .mathrew import api_rew as get_api_rew
from .apibtc import api_btc as get_api_btc, get_difficulty, get_rewards
from WooAPi import main as APIminers

def get_language_code(lang):
    if lang == "🇷🇺":
        return "ru"
    elif lang == "🇺🇸":
        return "en"
    else:
        return lang

def get_language_in_db(id):
    lang = dbase.select(id, "lang")
    return lang[0]

def datetimedef():
    date = get_date()
    time = get_time()
    return {"date": f"{date}", "time": f"{time}"}

def get_currency_datas(currency):
    if currency == "USD":
        cur = round(float(4.32 / get_currency_data('RUB')), 3)
    else:
        cur = 4.32
    return {"pay": f"{cur}"}

def get_datetime():
    return datetimedef()

def get_miner_data(id, chat_id):
    currency = dbase.select(chat_id, "currency")[0]
    pay = float(dbase.select(chat_id, "electricity")[0])
    btc_th = float(get_api_rew())
    th = float(APIminers.api_minerth(id))
    mes = float(30.33)
    Minername = APIminers.api_minerinfo(id)
    minercost = APIminers.api_minercost(id, currency)
    btcapi = float(get_api_btc())
    curapi = float(get_currency_data(currency))
    dohod = round(float(btc_th * th * mes * btcapi * curapi), 2)
    dohod1 = f'{dohod:,.2f}'.replace(',', ' ')
    rashod = round(float(APIminers.api_minerenergy(id)) * 24 * mes * pay, 2)
    rashod1 = f'{rashod:,.2f}'.replace(',', ' ')
    cash = round(dohod - rashod, 2)
    cash1 = f'{cash:,.2f}'.replace(',', ' ')
    okup = round(float(minercost / cash))
    
    return {"dohod": f"{dohod1}",
            "rashod": f"{rashod1}",
            "pribyl": f"{cash1}",
            "okup": f"{okup}",
            "name": f"{Minername}",
            "th": f"{th}"}

def get_api_data(currency):
    api_btc = round(float(get_api_btc()), 2)
    api_btc1 = f'{api_btc:,.2f}'.replace(',', ' ')
    return {"binancecrs": f"{api_btc1}",
            "courseusd": f"{get_currency_data(currency)}",
            "dif": f"{get_difficulty()}",
            "reward": f"{get_rewards()}",
            "reward1th": f"{get_api_rew()}"}

def get_miner_info(id, currency):
    minername = APIminers.api_minerinfo(id)
    cost = int(APIminers.api_minercost(id, currency))
    sell = float(APIminers.api_minersell(id, currency))
    th = APIminers.api_minerth(id)
    sell1 = f'{sell:,.2f}'.replace(',', ' ')
    return {"minername": f"{minername}",
            "sell": f"{sell1}",
            "cost": f"{cost}",
            "th": f"{th}"}
