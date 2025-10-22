from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from database.models import User, todo, Food
from misc.scheduler_update_date import update_time
from keyboards.back import back_kb
from keyboards.gpt import gpt_kb

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

router = Router()

class Form(StatesGroup):
    gpt_question = State()

API_KEY = os.getenv('API_KEY_GPT')
MODEL = 'deepseek/deepseek-r1'

def proces_content(content):
    return content.replace('<think>', '').replace('</think>', '')

async def analize_chat_stream(user_question, message: types.Message):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = await User.filter(telegram_id=message.from_user.id)
    values = {
        '1-1': data[0].first_answer,
        '1-2': data[0].second_answer,
        '1-3': data[0].third_answer,
        '1-4': data[0].fourth_answer,
        '2-1': data[0].fifth_answer,
        '2-2': data[0].sixth_answer,
        '2-3': data[0].seventh_answer,
    }
    data_food = await Food.filter(telegram_id = message, date = update_time())
    data_todo = await todo.filter(telegram_id = message.from_user.id, date = update_time())
    prompt = '''Ты — «Виталий», персональный AI-тренер...

...всё ваш промт...

ЖЕЛАНИЕ ПОЛЬЗОВАТЕЛЯ:
{QUESTION}

❗️**ВАЖНАЯ ИНСТРУКЦИЯ**: ОБЯЗАТЕЛЬНО ИСПОЛЬЗУЙ ВСЕ ВЫШЕПЕРЕЧИСЛЕННЫЕ ДАННЫЕ для ответа на вопрос пользователя. 
Не игнорируй данные анкеты, питания и тренировок - анализируй их и на их основе давай персонализированный ответ.

1. Сначала проанализируй данные анкеты
2. Затем учти сегодняшнее питание и тренировки  
3. И только потом отвечай на вопрос пользователя, используя весь этот контекст

Вопросы для клиента:
1: {
        1: "Похудение и снижение веса",
        2: "Набор мышечной массы",
        3: "Улучшение выносливости",
        4: "Реабилитация после травм"
    },
    2: {
        1: "Силовые тренировки с железом",
        2: "Кардио-тренировки",
        3: "Функциональный тренинг",
        4: "Йога и растяжка"
    },
    3: {
        1: "Улучшение физической формы",
        2: "Снижение стресса",
        3: "Социализация",
        4: "Подготовка к соревнованиям"
    },
    4: {
        1: "1-2 часа в неделю",
        2: "3-4 часа в неделю",
        3: "5-6 часов в неделю",
        4: "Более 6 часов"
    },
    5: {
        1: "Самостоятельные тренировки",
        2: "С персональным тренером",
        3: "Групповые занятия"
    },
    6: {
        1: "Очень важно",
        2: "Скорее важно",
        3: "Не имеет значения"
    },
    7: {
        1: "До 18 лет",
        2: "18-25 лет",
        3: "26-35 лет",
        4: "36-45 лет",
        5: "Старше 45 лет"
    }

Его ответы:
ДАННЫЕ ИЗ АНКЕТЫ КЛИЕНТА:
{data}

СЕГОДНЯ ПОЛЬЗОВАТЕЛЬ СЪЕЛ:
{FOOD}

СЕГОДНЯ ПОЛЬЗОВАТЕЛЬ СДЕЛАЛ:
{TODO}

ИНСТРУКЦИЯ ДЛЯ АНАЛИЗА:
1. Анализируй цифровые ответы как уровни/баллы (1-низкий, 3-средний, 5-высокий)
2. Будь внимательным, конструктивным и ориентированным на данные
3. Всегда начинай с положительного, подкрепляя сильные стороны
4. Затем переходи к "зонам роста", предлагая конкретные решения
5. Показывай взаимосвязь между различными аспектами тренировок и питания

ФОРМАТ ОТВЕТА:

🏋️ АНАЛИЗ ТВОЕГО ПОТЕНЦИАЛА

✅ Сильные стороны: [выяви плюсы на основе ответов]
⚠️ Зоны роста: [определи минусы и риски]

📊 ПЕРСОНАЛИЗИРОВАННЫЙ ПЛАН

🎯 Рекомендуемая программа:
• Частота тренировок: [конкретные рекомендации]
• Акценты: [на что делать упор]
• Интенсивность: [уровень нагрузки]

🥗 ПИТАНИЕ И РЕЖИМ:
• Основные рекомендации: [конкретные советы по питанию]
• Режим дня: [расписание]
• Гидратация: [рекомендации по воде]

🔄 ВОССТАНОВЛЕНИЕ:
• Сон: [рекомендации]
• Контроль прогресса: [как отслеживать]

🎯 КЛЮЧЕВЫЕ РЕКОМЕНДАЦИИ НА СТАРТЕ:
• [3-4 самых важных конкретных пункта]

Ты на правильном пути! Давай настроим твой план для максимальных результатов! 💪

Не используй общие фразы, давай только конкретные рекомендации основанные на цифрах из анкеты.'''

    data_str = ""
    for key, value in values.items():
        question_number, answer_number = key.split('-')
        data_str += f'Раздел {question_number}, вопрос {answer_number}: {value}\n'
    food_list = [food.name for food in data_food] if data_food else ["Нет данных о питании"]
    todo_list = [task.todo_task for task in data_todo] if data_todo else ["Нет данных о тренировках"]

    formatted_prompt = prompt.format(
        data=data_str,
        FOOD=", ".join(food_list),
        TODO=", ".join(todo_list),
        QUESTION = user_question
    )
    data = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': formatted_prompt}],
        'stream': True
    }

    bot_message = await message.answer("🔍 Нейросеть генерирует ответ...")
    full_response = []

    try:
        with requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            stream=True
        ) as response:
            if response.status_code != 200:
                await bot_message.edit_text("⚠️ Ошибка при обращении к нейросети")
                return
            
            for chunk in response.iter_lines():
                if chunk:
                    chunk_str = chunk.decode('utf-8').replace('data:', '')
                    try:
                        chunk_json = json.loads(chunk_str)
                        if 'choices' in chunk_json:
                            content = chunk_json['choices'][0]['delta'].get('content', '')
                            if content:
                                cleaned = proces_content(content)
                                full_response.append(cleaned)
                                if len(full_response) % 5 == 0: 
                                    await bot_message.edit_text(
                                        f"🤖 Ответ:\n\n{''.join(full_response)}",
                                        parse_mode=ParseMode.MARKDOWN
                                    )
                    except:
                        pass
            
            if full_response:
                await bot_message.edit_text(
                    f"🤖 Ответ:\n\n{''.join(full_response)}",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=gpt_kb()
                )
            else:
                await bot_message.edit_text("❌ Нейросеть не вернула ответ")
                
    except Exception as e:
        await bot_message.edit_text(f"⚠️ Произошла ошибка: {str(e)}")

@router.callback_query(F.data == 'deepseek_analize')
async def question_answer1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Задайте вопрос нейросети:', reply_markup=back_kb())
    await state.set_state(Form.gpt_question)
    await callback.answer()
@router.message(StateFilter(Form.gpt_question))
async def handle_user_question1(message: types.Message, state: FSMContext):
    if message.text:
        await analize_chat_stream(message.text, message)
        await state.clear()