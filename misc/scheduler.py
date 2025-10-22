from aiogram import Bot
from datetime import datetime, time, timedelta
import asyncio
from database.models import User 

async def send_daily_message(bot: Bot):
    try:
        users = await User.all()
        
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text="🌞 Доброе утро! Не забудьте внести свои сегодняшние данные:\n\n"
                         "• 🍎 Питание\n"
                         "• 🏋️ Тренировки\n"
                         "• 📊 Замеры (если нужно)\n\n"
                         "Хорошего дня! 💪"
                )
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")
                continue
                
    except Exception as e:
        print(f"Ошибка в daily_message: {e}")

async def schedule_daily_messages(bot: Bot):
    while True:
        now = datetime.now()
        target_time = time(4, 0)  
        
        target_datetime = datetime.combine(now.date(), target_time)
        if now > target_datetime:
            target_datetime = datetime.combine(now.date() + timedelta(days=1), target_time)
        
        wait_seconds = (target_datetime - now).total_seconds()
        
        print(f"Следующее ежедневное сообщение через {wait_seconds} секунд")
        await asyncio.sleep(wait_seconds)
        
        await send_daily_message(bot)