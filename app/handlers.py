from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Добро пожаловать,{message.from_user.first_name} !')

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи!')

@router.message(Command('catalog'))
async def cmd_help(message: Message):
    await message.answer(f'Выберите интересующий вас раздел 👇', reply_markup=kb.main)

@router.message(F.text == 'Меню')
async def menu(message: Message):
    await message.answer('Сделайте выбор: ', reply_markup=kb.menu)

@router.callback_query(F.data == 'coffee')
async def coffee(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Вы выбрали категорию кофе')
