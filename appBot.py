'''Все виды месаджей здесь: https://core.telegram.org/bots/api#message'''
import emoji
import telebot

from config import currency, TOKEN
from extensions import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)
emo = emoji.emojize


@bot.message_handler(commands=['help', 'start'])
def help(message: telebot.types.Message):
    text = 'введите команду боту:\n<имя валюты>\n<в какую перевести>\n<количество>\n' \
           'Посмотреть возможные валюты: /values\n' \
           '---------------------------------\nПолучить курс валют:\n' \
           '/btc_to_usd\n/euro_to_rub\n/usd_to_euro\n/usd_to_rub'
    bot.reply_to(message, text)


@bot.message_handler(commands=['btc_to_usd','euro_to_rub','usd_to_euro','usd_to_rub'])
def quick_rate(message: telebot.types.Message):
    values = []
    if message.text == '/btc_to_usd':
        values = ['btc', 'usd', '1']
    elif message.text == '/euro_to_rub':
        values = ['euro', 'rub', '1']
    elif message.text == '/usd_to_euro':
        values = ['usd', 'euro', '1']
    elif message.text == '/usd_to_rub':
        values = ['usd', 'rub', '1']
    text = CryptoConverter.get_rate(values)
    print(text)
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for cur in currency.keys():
        text += cur + '\n'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConversionException(emo('Неправильный ввод. Слишком много параметров 🤨'))
        elif len(values) < 2:
            raise ConversionException(emo('Неправильный ввод. Слишком мало параметров 🤷‍♀️'))
        elif len(values) == 2:
            values.append('1')

        base, quote, amount = values
        amount_float = float(amount)
        rate = CryptoConverter.convert(values)
        convertion_result = round((amount_float * rate), 2)
    except ConversionException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос\n{e}')
    else:
        text = emo(
            f'Курс {base} к {quote} = {rate}\n Для покупки {amount_float} {base} потребуется {convertion_result} {quote}     🤔')
        print(text)
        bot.send_message(message.chat.id, text)


print(emo('Bot started>>>>>>>>>>>>:thumbs_up:'))

bot.polling()
