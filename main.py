import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from sqlite.sqlite import db_start


async def main():
    await db_start()
    bot = Bot(token='6706240861:AAFIFHd1dOzdmUySZ-miKAtbwrpRVRUcCvw')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

