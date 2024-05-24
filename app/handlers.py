from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    number = State()
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f'Добро пожаловать, {message.from_user.first_name} !'
                         f' Вас приветствует телеграмм-бот кофейни-пекарни "Перемена".')


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

@router.callback_query(F.data == 'not coffee')
async def coffee(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Вы выбрали категорию не кофе')

@router.callback_query(F.data == 'bakery')
async def coffee(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Вы выбрали категорию выпечка')

@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')

@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)

@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data=await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nВаше номер телефона: {data["number"]}\n')
    await state.clear()

