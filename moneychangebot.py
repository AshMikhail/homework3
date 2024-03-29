import telebot
from config import TOKEN, keys
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Добро пожаловать! Что бы начать работу введите команду в следующем формате:\n' \
    '<имя валюты> \
    <в какую валюту перевести> \
    <сумма которую хотите перевести>\nсписок доступных валют: /values'
    bot.reply_to(message, f'{message.chat.username}, {text}')

@bot.message_handler(commands=['values'])
def values(meeage: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(meeage, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_result = MoneyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_result}'
        bot.send_message(message.chat.id, text)

bot.polling()