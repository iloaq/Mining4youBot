import requests

responsedif = requests.get('https://blockchain.info/q/getdifficulty').json()
response = requests.get('https://blockchain.info/ticker?USD').json()
responseminestat = requests.get('https://api.minerstat.com/v2/coins?list=BTC').json()

def api_btc():
    datae = response['USD']
    return datae['last']


def get_difficulty():
    return int(responsedif)

def get_rewards():
    return responseminestat[0]['reward_block']
