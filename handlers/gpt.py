from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

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

def process_content(content):
    return content.replace('<think>', '').replace('</think>', '')

async def chat_stream(prompt, message: types.Message):
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

@router.callback_query(F.data == 'question')
async def question_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Задайте вопрос нейросети:', reply_markup=gpt_kb())
    await state.set_state(Form.gpt_question)

@router.message(StateFilter(Form.gpt_question))
async def handle_user_question(message: types.Message, state: FSMContext):
    if message.text:
        await chat_stream(message.text, message)
        await state.clear()