from aiogram import Router, F 
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

from database.database import AsyncSessionLocal

from database.models import User

from keyboards.quiz import (
    question_1,
    question_2,
    question_3,
    question_4,
    question_5,
    question_6,
    question_7
)

QUESTION_TEXTS = {
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
}

router = Router()

class QuizStats(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()

async def edit_quiz_question(
    callback: CallbackQuery,
    question_num: int,
    question_text: str,
    keyboard_func,
    state: FSMContext,
    answer_key: str
):
    
    state_data = await state.get_data()
    answered = state_data.get(answer_key)
    
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            f"Вопрос {question_num}/7\n{question_text}",
            reply_markup=keyboard_func(answered)
        )
        await state.set_state(getattr(QuizStats, f"question_{question_num}"))
        await callback.answer()
async def handle_quiz_answer(
    callback: CallbackQuery,
    question_num: int,
    keyboard_func,
    state: FSMContext,
    answer_key: str
):
    
    answer_num = int(callback.data.split("-")[-1])
    
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            f"Вопрос {question_num}/7\nКакие у вас цели в спорте?",
            reply_markup=keyboard_func(answer_num)
        )
        await state.update_data({answer_key: answer_num})
        await callback.answer()

# Вопрос 1
@router.callback_query(F.data == 'quiz-1')
async def start_quiz_1(callback: CallbackQuery, state: FSMContext):
    await edit_quiz_question(
        callback, 1, "Какие у вас цели в спорте?", 
        question_1, state, 'answered_1'
    )

@router.callback_query(QuizStats.question_1, F.data.startswith("quiz-1-"))
async def handle_q1_answer(callback: CallbackQuery, state: FSMContext):
    await handle_quiz_answer(
        callback, 1, question_1, state, 'answered_1'
    )

# Вопрос 2
@router.callback_query(F.data == 'quiz-2')
async def start_quiz_2(callback: CallbackQuery, state: FSMContext):
    await edit_quiz_question(
        callback, 2, "Какие виды тренировок вы предпочитаете ?", 
        question_2, state, 'answered_2'
    )

@router.callback_query(QuizStats.question_2, F.data.startswith("quiz-2-"))
async def handle_q2_answer(callback: CallbackQuery, state: FSMContext):
    await handle_quiz_answer(
        callback, 2, question_2, state, 'answered_2'
    )

# Вопрос 3
@router.callback_query(F.data == 'quiz-3')
async def start_quiz_3(callback: CallbackQuery, state: FSMContext):
    await edit_quiz_question(
        callback, 3, "Что вы хотите получить от занятий?", 
        question_3, state, 'answered_3'
    )

@router.callback_query(QuizStats.question_3, F.data.startswith("quiz-3-"))
async def handle_q3_answer(callback: CallbackQuery, state: FSMContext):
    await handle_quiz_answer(
        callback, 3, question_3, state, 'answered_3'
    )

# Вопрос 4
@router.callback_query(F.data == 'quiz-4')
async def start_quiz_4(callback: CallbackQuery, state: FSMContext):
    await edit_quiz_question(
        callback, 4, "Сколько часов в неделю готовы выделить?", 
        question_4, state, 'answered_4'
    )

@router.callback_query(QuizStats.question_4, F.data.startswith("quiz-4-"))
async def handle_q4_answer(callback: CallbackQuery, state: FSMContext):
    await handle_quiz_answer(
        callback, 4, question_4, state, 'answered_4'
    )

# Вопрос 5
@router.callback_query(F.data == 'quiz-5')
async def start_quiz_5(callback: CallbackQuery, state: FSMContext):
    await edit_quiz_question(
        callback, 5, "Будете заниматься сами или с тренером?", 
        question_5, state, 'answered_5'
    )

@router.callback_query(QuizStats.question_5, F.data.startswith("quiz-5-"))
async def handle_q5_answer(callback: CallbackQuery, state: FSMContext):
    await handle_quiz_answer(
        callback, 5, question_5, state, 'answered_5'
    )

# Вопрос 6
@router.callback_query(F.data == 'quiz-6')
async def start_quiz_6(callback: CallbackQuery, state: FSMContext):
    await edit_quiz_question(
        callback, 6, "Важно ли иметь единомышленников?", 
        question_6, state, 'answered_6'
    )

@router.callback_query(QuizStats.question_6, F.data.startswith("quiz-6-"))
async def handle_q6_answer(callback: CallbackQuery, state: FSMContext):
    await handle_quiz_answer(
        callback, 6, question_6, state, 'answered_6'
    )

# Вопрос 7
@router.callback_query(F.data == 'quiz-7')
async def start_quiz_7(callback: CallbackQuery, state: FSMContext):
    await edit_quiz_question(
        callback, 7, "Какой ваш возраст?", 
        question_7, state, 'answered_7'
    )

@router.callback_query(QuizStats.question_7, F.data.startswith("quiz-7-"))
async def handle_q7_answer(callback: CallbackQuery, state: FSMContext):
    await handle_quiz_answer(
        callback, 7, question_7, state, 'answered_7'
    )

