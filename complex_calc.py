import telegram
import telebot
from telegram import Update, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler, CallbackQueryHandler
from logger import log
from datetime import datetime as dt

TOKEN = '5781757152:AAH6PcpYeE9EkDOXcotVv4sx--8jOqWVUXg'
bot = telebot.TeleBot(TOKEN)

value1, value2, old_value = '', '', ''
variant = ''


keyboard_complex = telebot.types.InlineKeyboardMarkup()
keyboard_complex.row(InlineKeyboardButton('C', callback_data='c'),
                     InlineKeyboardButton('<=', callback_data='<='),
                     InlineKeyboardButton('.', callback_data='.'),
                     InlineKeyboardButton('/', callback_data='/'))

keyboard_complex.row(InlineKeyboardButton('7', callback_data='7'),
                     InlineKeyboardButton('8', callback_data='8'),
                     InlineKeyboardButton('9', callback_data='9'),
                     InlineKeyboardButton('*', callback_data='*'))

keyboard_complex.row(InlineKeyboardButton('4', callback_data='4'),
                     InlineKeyboardButton('5', callback_data='5'),
                     InlineKeyboardButton('6', callback_data='6'),
                     InlineKeyboardButton('-', callback_data='-'))

keyboard_complex.row(InlineKeyboardButton('1', callback_data='1'),
                     InlineKeyboardButton('2', callback_data='2'),
                     InlineKeyboardButton('3', callback_data='3'),
                     InlineKeyboardButton('+', callback_data='+'))

keyboard_complex.row(InlineKeyboardButton('0', callback_data='0'),
                     InlineKeyboardButton('1 число', callback_data='first'),
                     InlineKeyboardButton('2 число', callback_data='second'),
                     InlineKeyboardButton(',', callback_data=','),
                     InlineKeyboardButton('=', callback_data='='))

keyboard_real = telebot.types.InlineKeyboardMarkup()
keyboard_real.row(InlineKeyboardButton('C', callback_data='c'),
                  InlineKeyboardButton('<=', callback_data='<='),
                  InlineKeyboardButton('.', callback_data='.'),
                  InlineKeyboardButton('/', callback_data='/'))

keyboard_real.row(InlineKeyboardButton('7', callback_data='7'),
                  InlineKeyboardButton('8', callback_data='8'),
                  InlineKeyboardButton('9', callback_data='9'),
                  InlineKeyboardButton('*', callback_data='*'))

keyboard_real.row(InlineKeyboardButton('4', callback_data='4'),
                  InlineKeyboardButton('5', callback_data='5'),
                  InlineKeyboardButton('6', callback_data='6'),
                  InlineKeyboardButton('-', callback_data='-'))

keyboard_real.row(InlineKeyboardButton('1', callback_data='1'),
                  InlineKeyboardButton('2', callback_data='2'),
                  InlineKeyboardButton('3', callback_data='3'),
                  InlineKeyboardButton('+', callback_data='+'))

keyboard_real.row(InlineKeyboardButton('0', callback_data='0'),
                  InlineKeyboardButton('//', callback_data='//'),
                  InlineKeyboardButton('%', callback_data='%'),
                  InlineKeyboardButton('=', callback_data='='))


@bot.message_handler(commands=['start'])
def get_message(message):
    log(f'сообщение от пользователя: {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}')
    bot.send_message(message.from_user.id,
                     text='Добрый день! Чтобы начать работу, выберите одно из возможных действий:\n'
                          '/real - вещественный калькуляьор\n'
                          '/complex - комплексный калькулятор')


@bot.message_handler(commands=['real'])
def get_message(message):
    global variant
    variant = 'real'
    log(f'сообщение от пользователя: {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}')
    bot.send_message(message.from_user.id, text='0', reply_markup=keyboard_real)


@bot.message_handler(commands=['complex'])
def get_message(message):
    global variant
    variant = 'complex'
    log(f'сообщение от пользователя: {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name}')
    bot.send_message(message.from_user.id, text='-------', reply_markup=keyboard_complex)


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value1, value2, old_value
    if variant == 'real':
        global value1
        data = query.data

        if data == 'c':
            value1 = ''
        elif data == '<=':
            value1 = value1[:-1]
        elif data == '=':
            try:
                value1 = str(eval(value1))
            except ZeroDivisionError:
                value1 = 'Ошибка!'
        else:
            value1 += data

        if value1 == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0',
                                  reply_markup=keyboard_real)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value1,
                                  reply_markup=keyboard_real)

    if variant == 'complex':
        pass


bot.polling(none_stop=False, interval=0)