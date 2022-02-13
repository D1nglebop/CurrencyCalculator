import telebot
from config import TOKEN, available_values
from extensions import APIException, CurrencyCalculator

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = 'Для конвертации одной валюты в другую введите их названия в следующем формате:\n<название продаваемой валюты> \
<название покупаемой валюты> <количество продаваемой валюты>.\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for av_val in available_values.keys():
        text = '\n'.join((text, av_val + ' ' + available_values[av_val]))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        data = message.text.title().split(' ')

        if len(data) != 3:
            raise APIException('Неверный формат ввода. Конвертация невозможна.')

        quote, base, amount = data
        calc_res = CurrencyCalculator.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        text = f'На {amount} {available_values[quote]} можно приобрести {calc_res} {available_values[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()
