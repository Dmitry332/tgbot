import random

import telebot
import webbrowser
from telebot import types
import sqlite3
name = None

bot = telebot.TeleBot('6521613461:AAFRpv08yobW047Un0_HooFvYLCbkINZMf4')

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('testBot.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (userID, name varchar(50), surname varchar(50))""")
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Для регестрации введите ваше имя: ')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите фамилию: ')
    bot.register_next_step_handler(message, user_surname)

def user_surname(message):
    surname = message.text.strip()
    global userID
    userID = message.from_user.username
    conn = sqlite3.connect('testBot.db')
    cur = conn.cursor()

    cur.execute(f'INSERT INTO users (userID ,name, surname) VALUES ("%s", "%s", "%s")' % (userID ,name, surname))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Найти пару', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('testBot.db')
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM users WHERE userID != ("%s")' % (userID))
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Ваша пара: {el[1]},  фамилия: {el[2]},  ID: @{el[0]}\n'
        break
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)
