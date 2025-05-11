import logging
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import URL, create_engine, select, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.exc import IntegrityError  # Добавлен импорт

from hui import settings
from config import TOKEN_API_BOT

# Настройка бота
bot = Bot(token=TOKEN_API_BOT)
dp = Dispatcher()

# Настройка базы данных
engine = create_engine(url=settings.DATABASE_URL_PSYCOPG, echo=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str]
    age: Mapped[int]

# Создаем таблицы и удаляем таблицу 
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Стейты (состояния) для FSM
class Form(StatesGroup):
    name = State()
    age = State()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

# Обработчик ввода имени
@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

# Обработчик ввода возраста
@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите число!")
        return

    data = await state.get_data()
    
    # Сохраняем в базу данных
    with Session(engine) as session:
        try:
            # Пытаемся добавить нового пользователя
            user = User(
                user_id=message.from_user.id,
                name=data['name'],
                age=age
            )
            session.add(user)
            session.commit()
            await message.answer("Данные сохранены!")
            
        except IntegrityError:
            # Если пользователь уже существует - обновляем его данные
            session.rollback()
            existing_user = session.execute(
                select(User).where(User.user_id == message.from_user.id)
            ).scalar_one()
            
            existing_user.name = data['name']
            existing_user.age = age
            session.commit()
            await message.answer("Данные обновлены!")
    
    # Отправляем все данные пользователю
    await send_all_data(message)
    await state.clear()

# Функция отправки всех данных
async def send_all_data(message: Message):
    with Session(engine) as session:
        users = session.execute(select(User)).scalars().all()
        
        if not users:
            await message.answer("В базе пока нет данных.")
            return

        response = "📊 Все данные из базы:\n\n"
        for user in users:
            response += (
                f"👤 ID: {user.user_id}\n"
                f"📛 Имя: {user.name}\n"
                f"🔢 Возраст: {user.age}\n"
                f"————————————\n"
            )
        
        # Разбиваем длинные сообщения
        max_length = 4000
        if len(response) > max_length:
            for i in range(0, len(response), max_length):
                await message.answer(response[i:i+max_length])
        else:
            await message.answer(response)

# Обработчик команды /data
@dp.message(Command("data"))
async def cmd_data(message: Message):
    await send_all_data(message)

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())