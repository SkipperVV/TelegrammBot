'''Все виды месаджей здесь: https://core.telegram.org/bots/api#message'''
import emoji
import telebot

from config import currency, TOKEN
from extensions import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)
emo = emoji.emojize


@bot.message_handler(commands=['help', 'start'])
def help(message: telebot.types.Message):
    text = 'введите команду боту:\n<имя валюты>\n<в какую перевести>\n<количество>\nПосмотреть возможные валюты: /values'
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
        convertion_result = amount_float * rate
    except ConversionException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос\n{e}')
    else:
        text = emo(
            f'Курс {base} к {quote} = {rate}\n Для покупки {amount_float} {base} потребуется {convertion_result} {quote}     🤔')
        print('text= ', text)
        bot.send_message(message.chat.id, text)


print(emo('Bot started>>>>>>>>>>>>:thumbs_up:'))

bot.polling()
