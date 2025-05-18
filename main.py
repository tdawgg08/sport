import os
import sys
from aiogram import Dispatcher, Bot, F, types
from handlers.start import router as start_router
from handlers.quiz import router as quiz_router
from handlers.menu import router as menu_router
from callbacks import num_router
import logging

from database.orm import Manage_ORM
from config import TOKEN_API_BOT

import asyncio

import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)

sys.path.insert(1, os.path.join(sys.path[0], '..'))

async def main():
    bot = Bot(TOKEN_API_BOT)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(quiz_router)
    dp.include_router(menu_router)
    dp.include_router(num_router)
    await Manage_ORM.drop_tables()
    await Manage_ORM.create_table_anketa()
    logging.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при работе бота: {e}")
    finally:
        logging.info("Бот остановлен")
        await bot.session.close()

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())