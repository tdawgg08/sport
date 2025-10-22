from aiogram.types import CallbackQuery
from aiogram import Router, F
from keyboards.gpt import gpt_kb

router = Router()

@router.callback_query(F.data == 'question')
async def vs(callback : CallbackQuery):
    await callback.message.answer('Узнать мнение нейросети о вашем питании / Задать вопрос', reply_markup=gpt_kb())
    await callback.answer()