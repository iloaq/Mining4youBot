import requests

def currency_data1(currency):
    data = requests.get(f'https://v6.exchangerate-api.com/v6/70f07d941238c281dd09dffe/latest/USD').json()
    return round(data['conversion_rates'][currency],3)
