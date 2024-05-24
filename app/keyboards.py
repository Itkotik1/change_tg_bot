from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='О нас')],
                                     [KeyboardButton(text='Меню'),
                                     KeyboardButton(text='Контакты'),
                                     KeyboardButton(text='Бонусы')],
                                     [KeyboardButton(text='Сайт')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пунк меню...')

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кофе', callback_data='coffee')],
    [InlineKeyboardButton(text='Не кофе', callback_data='not coffee')],
    [InlineKeyboardButton(text='Выпечка', callback_data='bakery')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправь номер',
                                                        request_contact=True)]],
                               resize_keyboard=True)