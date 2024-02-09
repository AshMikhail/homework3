import requests
import json
from config import keys

class APIException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/c51a43d5715c484263ab085c/latest/{quote_ticker}')
        result = json.loads(r.content)['conversion_rates'][f'{base_ticker}']
        total_result = result * amount

        return round(total_result, 2)