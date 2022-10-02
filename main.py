# Ссылка на бота: t.me/currconverter_dvm_bot
# Имя бота: CurConverterBot
# Он, по идее, должен хоть сейчас работать; я его на pythonanywhere.com запустил
# !!! Без VPN, увы, сервис ExchangeRate-API не работает !!!

from config import TOKEN, currencies
from extensions import CurrencyConverter, APIException
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler (commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, "Здравствуйте! Этот бот умеет переводить одну валюту в другую.")
    bot.send_message(message.chat.id, "_Формат запроса_: \n\n *\<Валюта1\> \<Валюта2\> \<Количество\>* \n\n Например, введите \n\n *рубль доллар 25* \n\n чтобы узнать, сколько будет 25 рублей в долларах по текущему курсу\.", parse_mode="MarkdownV2")
    bot.send_message(message.chat.id, "Используйте команду /values для вывода списка доступных валют. Используйте команду /about для... нет, не используйте эту команду.")

@bot.message_handler (commands=['about'])
def about_message(message):
    bot.send_message(message.chat.id, "Бот создан при изучении курса «<a href='https://skillfactory.ru/python-fullstack-web-developer'>Fullstack разработчик на Python</a>» в школе SkillFactory.", parse_mode="HTML")

@bot.message_handler (commands=['values'])
def values_message(message):
    msg = "_Доступные валюты_: \n\n"
    for key in currencies.keys():
        msg += key + '\n'
    bot.send_message(message.chat.id, msg, parse_mode="MarkdownV2")

@bot.message_handler(content_types=['text'])
def converter(message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неправильный формат запроса. Используйте команду /help для дополнительной информации.')
        answer = CurrencyConverter.get_price(values[0], values[1], values[2])
    except APIException as errmsg:
        bot.send_message(message.chat.id, errmsg)
    except Exception as errmsg:
        bot.send_message(message.chat.id, "Что-то пошло не так.\n"+errmsg)
    else:
        bot.send_message(message.chat.id, answer)

bot.polling()