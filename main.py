from aiogram import Dispatcher, Bot, F
from handlers.start import router

from config import TOKEN_API_BOT

import asyncio


async def main():
    bot = Bot(TOKEN_API_BOT)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())