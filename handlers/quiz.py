from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.quiz import (
    question_1,
    question_2,
    question_3,
    question_4,
    question_5,
    question_6,
    question_7
)

router = Router()

class QuizStats(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()


@router.callback_query(F.data == 'quiz-1')
async def question_1_handler(callback: CallbackQuery, state: FSMContext):
    answered = None
    if await state.get_state():
        state_data = await state.get_data()
        answered = state_data.get('answered_1')
    await callback.message.delete()    
    await callback.message.answer(text="Вопрос 1/7\nКакие у вас цели в спорте?", reply_markup=question_1(answered))
    await state.set_state(QuizStats.question_1)

