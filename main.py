import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6413915263:AAFmQ3uLMCk2oUDPE5bycvh9ZxUL06DujEY",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    years = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Давай знакомиться!"  # Можно менять текст
text_button_1 = "Мой кабинет Умскул"  # Можно менять текст
text_button_2 = "Поднять настроение"  # Можно менять текст
text_button_3 = "А что это?"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Что будем делать?',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! Ваше _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Принял! Сколько _лет_ ты с [Умскул](https://t.me/umschool_official)?')
    bot.set_state(message.from_user.id, PollState.years, message.chat.id)


@bot.message_handler(state=PollState.years)
def years(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['years'] = message.text
    bot.send_message(message.chat.id, '*Спасибо за регистрацию!*', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Супер! Лови [ссылку](https://nd.umschool.net/auth/login/)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Вау, какой *милый ฅ^•ﻌ•^ฅ* котик!",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "*А это лучший* [телеграм канал](https://t.me/+jjHK7mxBpMthZWFi) *для начинающего python разработчика*",
                     reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()