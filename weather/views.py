from django.shortcuts import render
from django.http import HttpResponse
from .webhook import bot
from .functions import format_weather_message, fetch_weather
from telebot import types
import requests

with open('bot_weather_api.txt', 'r') as f:
    weather_api = f.read()


# Create your views here.

def base(request):
    return HttpResponse('Welcome')

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('help', callback_data='help')
    btn_2 = types.InlineKeyboardButton('Search here', callback_data='search')
    markup.add(btn_1, btn_2)

    if message.from_user.last_name != None:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} {message.from_user.last_name} 😀 \n\nIn this weather bot you can search for weater information all over the World! \nIf you need /help click here.""", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"""Welcome, {message.from_user.first_name} 😀 \n\nIn this weather bot you can search for weater information all over the World! \nIf you need /help click here.""", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'help':
        bot.send_message(call.message.chat.id, f"""The following commands are availabe: \n\n/start -> Welcome message \n/help -> Show Available Commands""")
    if call.data == 'search':
        bot.send_message(call.message.chat.id, "Ob-havo malumoti uchun shaxar nomini kirting.")


@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city_name = message.text
    weather_data = fetch_weather(city_name)
    if weather_data:
        weather_message = format_weather_message(weather_data)
        bot.reply_to(message, weather_message)
    else:
        bot.reply_to(message, "Kechirasiz, Bu shaharning ob havosi haqida malumot topolmadim!")
