from config import currencies
import requests
import json

class APIException (Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price (base, quote, amount):
        try:
            base_key = currencies[base]
        except KeyError:
            raise APIException(f"Валюта {base} не поддерживается. Используйте команду /values для вывода списка доступных валют.")

        try:
            quote_key = currencies[quote]
        except KeyError:
            raise APIException(f"Валюта {quote} не поддерживается. Используйте команду /values для вывода списка доступных валют.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Вероятно, неправильно указано количество {amount}.")

        if base_key!=quote_key:
            req = requests.get(f"https://v6.exchangerate-api.com/v6/102b90c4bb31985d0b620e60/pair/{base_key}/{quote_key}/{amount}")
            answer = json.loads(req.content)
            price = answer['conversion_result']
            return (f"Результат: {amount} {base} = {price} {quote}")
        else:
            return (f"Вы указали одну и ту же валюту. Очевидно, {amount} {base} так и стоит {amount} {base}.")