from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import User
from keyboards.gpt import gpt_kb

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

router = Router()

API_KEY = os.getenv('API_KEY_GPT')
MODEL = 'deepseek/deepseek-r1'


async def send_recomendation(user_id, message : types.Message):
    data = await User.filter(telegram_id=user_id)
    values = {
        '1-1': data[0].first_answer,
        '1-2': data[0].second_answer,
        '1-3': data[0].third_answer,
        '1-4': data[0].fourth_answer,
        '2-1': data[0].fifth_answer,
        '2-2': data[0].sixth_answer,
        '2-3': data[0].seventh_answer,
    }

    prompt = '''Ты - опытный персональный тренер и диетолог. Проанализируй ответы клиента из анкеты и составь ПЕРСОНАЛИЗИРОВАННЫЙ план рекомендаций.

ДАННЫЕ ИЗ АНКЕТЫ КЛИЕНТА:
{data}

ИНСТРУКЦИЯ ДЛЯ ТЕБЯ:
1. Анализируй цифровые ответы как уровни/баллы (1-низкий, 3-средний, 5-высокий)
2. Дай КОНКРЕТНЫЕ рекомендации без общих фраз
3. Структурируй ответ четко по разделам
4. Предлагай реально выполнимые действия
5. Учитывай взаимосвязь между ответами

ФОРМАТ ОТВЕТА (соблюдай точно):

🏋️ ПЕРСОНАЛИЗИРОВАННЫЙ ПЛАН ТРЕНИРОВОК

📅 Рекомендуемая частота: [укажи конкретно]
💪 Основные акценты: [на что делать упор]
⚡ Интенсивность: [уровень нагрузки]

Тренировочные дни:
• День 1: [конкретные упражнения, подходы, повторения]
• День 2: [конкретные упражнения, подходы, повторения]
• День 3: [конкретные упражнения, подходы, повторения]

🥗 ПЛАН ПИТАНИЯ И РЕЖИМ

🍽️ Режим питания: [рекомендации по питанию]
📊 Калорийность: [ориентиры]
🥛 Гидратация: [рекомендации по воде]
⏰ Режим дня: [расписание]

🔄 ВОССТАНОВЛЕНИЕ И ПРОГРЕСС

💤 Сон: [рекомендации]
📈 Контроль прогресса: [как отслеживать]
⚡ Корректировки: [когда вносить изменения]

🎯 КЛЮЧЕВЫЕ РЕКОМЕНДАЦИИ
• [3-4 самых важных пункта]

Не используй общие фразы, давай только конкретные рекомендации основанные на цифрах из анкеты.'''

    data_str = ""
    for key, value in values.items():
        question_number, answer_number = key.split('-')
        data_str += f'Раздел {question_number}, вопрос {answer_number}: {value}\n'

    prompt = prompt.format(data=data_str)
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
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
                                cleaned = process_content(content)
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


def process_content(content):
    return content.replace('<think>', '').replace('</think>', '')

