from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


BROADCAST_BUTTON = KeyboardButton('Посмотреть прогноз')
CURRENT_CITY_BUTTON = KeyboardButton('Текущий город', request_contact=False)
CHANGE_CITY_BUTTON = KeyboardButton('Изменить город')
CANCEL_BUTTON = KeyboardButton('Отмена')
MAILING_BUTTON = KeyboardButton('Рассылка')
SUBSCRIBE_BUTTON = KeyboardButton('Подписаться')
UNSUBSCRIBE_BUTTON = KeyboardButton('Отписаться')

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_kb.row(CHANGE_CITY_BUTTON)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(CURRENT_CITY_BUTTON, CHANGE_CITY_BUTTON, MAILING_BUTTON)
kb.add(BROADCAST_BUTTON)

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_kb.row(CANCEL_BUTTON)

mailing_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mailing_kb.row(SUBSCRIBE_BUTTON, UNSUBSCRIBE_BUTTON)
mailing_kb.add(CANCEL_BUTTON)
