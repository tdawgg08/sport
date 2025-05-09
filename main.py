from aiogram import Dispatcher, Bot, F, types
from handlers.start import router
from handlers.quiz import router as quiz_router
from callbacks import num_router
import logging

from config import TOKEN_API_BOT

import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler("bot.log")  # Запись в файл
    ]
)


async def main():
    bot = Bot(TOKEN_API_BOT)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(quiz_router)
    dp.include_router(num_router)
    logging.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при работе бота: {e}")
    finally:
        logging.info("Бот остановлен")
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())