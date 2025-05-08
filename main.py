from aiogram import Dispatcher, Bot, F, types
from handlers.start import router
from handlers.quiz import router as quiz_router
from callbacks import num_router

from config import TOKEN_API_BOT

import asyncio


async def main():
    bot = Bot(TOKEN_API_BOT)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(quiz_router)
    dp.include_router(num_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    
    asyncio.run(main())