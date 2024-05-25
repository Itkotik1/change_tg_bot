from aiogram import F, Router, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from sqlite.database import db_start, register_or_update_user

router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    phone_number = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f'Добро пожаловать, {message.from_user.first_name}.\n'
                         f'Вас приветствует телеграмм-бот кофейни-пекарни "Перемена".')

@router.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(f'Вы нажали на кнопку помощи  Вот команды для выбора действий: '
                         "/register - регистрация\n"
                         "/help - список команд для выполнения действий\n"
                         "/catalog - раздел с информацией")

@router.message(Command('catalog'))
async def cmd_catalog(message: types.Message):
    await message.answer(f'Выберите интересующий вас раздел 👇', reply_markup=kb.main)

@router.message(F.text == 'Меню')
async def menu(message: types.Message):
    await message.answer('Сделайте выбор: ', reply_markup=kb.menu)

@router.callback_query(F.data == 'coffee')
async def coffee_callback(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Вы выбрали категорию кофе')

@router.callback_query(F.data == 'not coffee')
async def not_coffee_callback(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Вы выбрали категорию не кофе')

@router.callback_query(F.data == 'bakery')
async def bakery_callback(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Вы выбрали категорию выпечка')

@router.message(Command('register'))
async def register(message: types.Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')

@router.message(Register.age)
async def register_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await state.set_state(Register.phone_number)
    await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)

@router.message(Register.phone_number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nВаш номер телефона: {data["phone_number"]}\n')
    await register_or_update_user(user_id=message.from_user.id, name=data['name'], age=data['age'], phone_number=data['phone_number'])
    await message.reply('Вы успешно зарегистрировались!')
    await state.clear()