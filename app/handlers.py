from aiogram import F, Router, Dispatcher, types
from aiogram.enums import ChatAction
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

COFFEE_PHOTO_PATH = "./prices/list1.jpg"

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f'Добро пожаловать, {message.from_user.first_name}.\n'
                         f'Вас приветствует телеграмм-бот кофейни-пекарни "Перемена".\n'
                         f'Давайте познакомимся? Ведь приятно, когда обращаются по имени!\n'
                         f'Нажмите на /register')

@router.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(f'Вы нажали на кнопку помощи  Вот команды для выбора действий: '
                         "/register - регистрация\n"
                         "/help - список команд для выполнения действий\n"
                         "/catalog - раздел с информацией")

@router.message(Command('catalog'))
async def cmd_catalog(message: types.Message):
    await message.answer(f'Выберите интересующий вас раздел 👇', reply_markup=kb.main)

@router.message(F.text == 'О нас')
async def about(message: types.Message):
    await message.answer('Кофейня-пекарня "Перемена')

@router.message(F.text == 'Контакты')
async def about(message: types.Message):
    await message.answer('Наши контакты!!!')

@router.message(F.text == 'Бонусы')
async def bonus(message: types.Message):
    await message.answer('Здесь мы будем показывать ваши бонусы!')

@router.message(F.text == 'Сайт')
async def site(message: types.Message):
    await message.answer('Здесь будет ссылка на наш сайт!')
@router.message(F.text == 'Меню')
async def menu(message: types.Message):
    await message.answer('Сделайте выбор: ', reply_markup=kb.menu)

@router.callback_query(F.data == 'coffee')
async def coffee_callback(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await coffee_command(callback.message)
async def coffee_command(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    file_path = "./prices/menu.jpg"
    await message.reply_photo(
        photo=types.FSInputFile(path=file_path),
        caption="Кофейные напитки",
    )



@router.callback_query(F.data == 'not coffee')
async def not_coffee_callback(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await not_coffee_command(callback.message)


async def not_coffee_command(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    file_path = "./prices/menu.jpg"
    # await message.bot.send_photo()
    await message.reply_photo(
        photo=types.FSInputFile(path=file_path),
        caption="Напитки",
    )
@router.callback_query(F.data == 'bakery')
async def bakery_callback(callback: types.CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await bakery_command(callback.message)


async def bakery_command(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    file_path = "./prices/menu.jpg"
    # await message.bot.send_photo()
    await message.reply_photo(
        photo=types.FSInputFile(path=file_path),
        caption="Выпечка",
    )

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

@router.message(Command("pic"))
async def handle_command_pic(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_PHOTO,
    )
    file_path = "./prices/list1.png"
    # await message.bot.send_photo()
    await message.reply_photo(
        photo=types.FSInputFile(path=file_path),
        caption="Кофейные напитки",
    )