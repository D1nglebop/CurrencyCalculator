import requests
import json
from config import available_values


class APIException(Exception):
    pass


class CurrencyCalculator:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Имена валют совпадают, перевод невозможен.')

        if quote not in available_values.keys():
            raise APIException(f'Не удалось обработать валюту {quote}.')

        if base not in available_values.keys():
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            float(amount)
        except ValueError:
            raise APIException('Некорректный ввод суммы конвертации.')

        if float(amount) <= 0:
            raise APIException('Недопустимая сумма конвертации.')

        r = requests.get('http://api.exchangeratesapi.io/v1/latest?access_key=918ad55c84e8d25555fcb78d9788dc89')
        av_val = json.loads(r.content)['rates']
        convert_res = float(amount) / av_val[available_values[quote]] * av_val[available_values[base]]

        return str(round(convert_res, 2))
