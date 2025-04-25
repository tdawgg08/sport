from aiogram import Router, F 
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.start import start_keyboard

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

#1
@router.callback_query(F.data == 'quiz-1')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    answered = state_data.get('answered_1') 
    
    await callback.message.edit_text(
        "Вопрос 1/7\nКакие у вас цели в спорте?",
        reply_markup=question_1(answered) 
    )
    await state.set_state(QuizStats.question_1)
    await callback.answer()

@router.callback_query(QuizStats.question_1, F.data.startswith("quiz-1-"))
async def handle_q1_answer(callback: CallbackQuery, state: FSMContext):
    answer_num = int(callback.data.split("-")[-1])
       
    await callback.message.edit_text(
            "Вопрос 1/7\nКакие у вас цели в спорте?",
            reply_markup=question_1(answer_num)
        )
    await callback.message.edit_reply_markup(
            reply_markup=question_1(answer_num)
        )
    
    await state.update_data(answered_1=answer_num)
    await callback.answer()

#2
@router.callback_query(F.data == 'quiz-2')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    answered = state_data.get('answered_2') 
    
    await callback.message.edit_text(
        "Вопрос 2/7\nКакие у вас цели в спорте?",
        reply_markup=question_2(answered) 
    )
    await state.set_state(QuizStats.question_2)
    await callback.answer()
@router.callback_query(QuizStats.question_2, F.data.startswith("quiz-2-"))
async def handle_q1_answer(callback: CallbackQuery, state: FSMContext):
    answer_num = int(callback.data.split("-")[-1])
       
    await callback.message.edit_text(
            "Вопрос 1/7\nКакие у вас цели в спорте?",
            reply_markup=question_1(answer_num)
        )
    await callback.message.edit_reply_markup(
            reply_markup=question_1(answer_num)
        )
    
    await state.update_data(answered_1=answer_num)
    await callback.answer()

#3
@router.callback_query(F.data == 'quiz-3')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    answered = state_data.get('answered_3') 
    
    await callback.message.edit_text(
        "Вопрос 1/7\nКакие у вас цели в спорте?",
        reply_markup=question_3(answered) 
    )
    await state.set_state(QuizStats.question_3)
    await callback.answer()
@router.callback_query(QuizStats.question_1, F.data.startswith("quiz-3-"))
async def handle_q1_answer(callback: CallbackQuery, state: FSMContext):
    answer_num = int(callback.data.split("-")[-1])
       
    await callback.message.edit_text(
            "Вопрос 3/7\nКакие у вас цели в спорте?",
            reply_markup=question_3(answer_num)
        )
    await callback.message.edit_reply_markup(
            reply_markup=question_3(answer_num)
        )
    
    await state.update_data(answered_1=answer_num)
    await callback.answer()

#4
@router.callback_query(F.data == 'quiz-4')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    answered = state_data.get('answered_4') 
    
    await callback.message.edit_text(
        "Вопрос 1/7\nКакие у вас цели в спорте?",
        reply_markup=question_4(answered) 
    )
    await state.set_state(QuizStats.question_4)
    await callback.answer()
@router.callback_query(QuizStats.question_4, F.data.startswith("quiz-4-"))
async def handle_q1_answer(callback: CallbackQuery, state: FSMContext):
    answer_num = int(callback.data.split("-")[-1])
       
    await callback.message.edit_text(
            "Вопрос 1/7\nКакие у вас цели в спорте?",
            reply_markup=question_4(answer_num)
        )
    await callback.message.edit_reply_markup(
            reply_markup=question_4(answer_num)
        )
    
    await state.update_data(answered_4=answer_num)
    await callback.answer()

#5
@router.callback_query(F.data == 'quiz-5')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    answered = state_data.get('answered_5') 
    
    await callback.message.edit_text(
        "Вопрос 1/7\nКакие у вас цели в спорте?",
        reply_markup=question_1(answered) 
    )
    await state.set_state(QuizStats.question_1)
    await callback.answer()
@router.callback_query(QuizStats.question_1, F.data.startswith("quiz-5-"))
async def handle_q1_answer(callback: CallbackQuery, state: FSMContext):
    answer_num = int(callback.data.split("-")[-1])
       
    await callback.message.edit_text(
            "Вопрос 1/7\nКакие у вас цели в спорте?",
            reply_markup=question_1(answer_num)
        )
    await callback.message.edit_reply_markup(
            reply_markup=question_1(answer_num)
        )
    
    await state.update_data(answered_1=answer_num)
    await callback.answer()

#6
@router.callback_query(F.data == 'quiz-6')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    answered = state_data.get('answered_6') 
    
    await callback.message.edit_text(
        "Вопрос 1/7\nКакие у вас цели в спорте?",
        reply_markup=question_1(answered) 
    )
    await state.set_state(QuizStats.question_1)
    await callback.answer()
@router.callback_query(QuizStats.question_1, F.data.startswith("quiz-6-"))
async def handle_q1_answer(callback: CallbackQuery, state: FSMContext):
    answer_num = int(callback.data.split("-")[-1])
       
    await callback.message.edit_text(
            "Вопрос 1/7\nКакие у вас цели в спорте?",
            reply_markup=question_1(answer_num)
        )
    await callback.message.edit_reply_markup(
            reply_markup=question_1(answer_num)
        )
    
    await state.update_data(answered_1=answer_num)
    await callback.answer()

#7
@router.callback_query(F.data == 'quiz-7')
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    answered = state_data.get('answered_7') 
    
    await callback.message.edit_text(
        "Вопрос 1/7\nКакие у вас цели в спорте?",
        reply_markup=question_1(answered) 
    )
    await state.set_state(QuizStats.question_1)
    await callback.answer()
@router.callback_query(QuizStats.question_1, F.data.startswith("quiz-7-"))
async def handle_q1_answer(callback: CallbackQuery, state: FSMContext):
    answer_num = int(callback.data.split("-")[-1])
       
    await callback.message.edit_text(
            "Вопрос 1/7\nКакие у вас цели в спорте?",
            reply_markup=question_1(answer_num)
        )
    await callback.message.edit_reply_markup(
            reply_markup=question_1(answer_num)
        )
    
    await state.update_data(answered_1=answer_num)
    await callback.answer()