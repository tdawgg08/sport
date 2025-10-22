import os
import sys
import logging
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from misc.set_kcal_in_db import import_products
from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.calculator.output_calories import router as output_calculator_router
from handlers.calculator.paste_calories import router as paste_calculator_router
from handlers.calculator.set_product import router as set_product_router
from handlers.quiz import router as quiz_router
from handlers.todo import router as todo_router
from handlers.gpt import router as gpt_router
from handlers.analize_vs_questions import router as analize_router
from handlers.gpt_for_analize_lead import router as gpt_for_analize_router
from misc.scheduler import schedule_daily_messages

from database.database import DataBaseInit

import asyncio

load_dotenv()

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
    TOKEN_API_BOT = os.getenv('TOKEN_API_BOT')
    bot = Bot(TOKEN_API_BOT)
    dp = Dispatcher()
    await DataBaseInit()
    await import_products()
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(output_calculator_router)
    dp.include_router(quiz_router)
    dp.include_router(paste_calculator_router)
    dp.include_router(set_product_router)
    dp.include_router(todo_router)
    dp.include_router(gpt_router)
    dp.include_router(analize_router)
    dp.include_router(gpt_for_analize_router)
    asyncio.create_task(schedule_daily_messages(bot))
    
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