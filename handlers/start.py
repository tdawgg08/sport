from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command
from keyboards.start import start_keyboard
from aiogram.fsm.context import FSMContext
from keyboards.quiz import SportQuiz, QuizStates


router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Ты попал в бота \"Интеллектуальный помощник по спортивному планированию\"\n"
        "Нажми кнопку ниже, чтобы начать тест 👇",
        reply_markup=start_keyboard()
    )





@router.message(F.text == "Начать")
async def start_quiz_handler(message: Message, state: FSMContext):
    # Создаем новый экземпляр квиза
    quiz = SportQuiz()
    
    # Сохраняем квиз в хранилище состояний
    await state.update_data(quiz=quiz)
    
    # Устанавливаем состояние квиза
    await state.set_state(QuizStates.in_quiz)
    
    # Отправляем первый вопрос
    await message.answer(
        text=f"Вопрос 1/{len(quiz.questions)}\n{quiz.questions[0]}",
        reply_markup=quiz.get_answer_keyboard(),
        parse_mode="Markdown"
    )    