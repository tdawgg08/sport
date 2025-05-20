from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from database.models import UserTodo, Tasks
from database.database import AsyncSessionLocal
from keyboards.todo import get_todolist_inline_keyboard

from sqlalchemy import select, delete

router = Router()

class TodoStates(StatesGroup):
    GET_task_title = State()
    GET_task_description = State()
    CHANGE_task_status = State()
    DELETE_task_by_id = State()

async def get_or_create_user(user_id: int, username: str) -> UserTodo:
    """Получение или создание пользователя"""
    async with AsyncSessionLocal() as session:
        user = await session.scalar(
            select(UserTodo).where(UserTodo.user_id == user_id)
        )
        if not user:
            user = UserTodo(user_id=user_id, username=username)
            session.add(user)
            await session.commit()
            
        return user

async def get_user_tasks(user_id: int) -> list[Tasks]:
    """Получение задач пользователя"""
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(Tasks)
            .where(Tasks.owner_id == user_id)
            .order_by(Tasks.created_at)
        )
        return result.all()

async def create_task(title: str, description: str, owner_id: int) -> None:
    """Создание новой задачи"""
    async with AsyncSessionLocal() as session:
        task = Tasks(
            title=title,
            description=description,
            owner_id=owner_id
        )
        session.add(task)
        await session.commit()

async def toggle_task_status(task_id: int, user_id: int) -> bool:
    """Переключение статуса задачи"""
    async with AsyncSessionLocal() as session:
        task = await session.scalar(
            select(Tasks)
            .where(Tasks.id == task_id)
            .where(Tasks.owner_id == user_id)
        )
        
        if task:
            task.is_completed = not task.is_completed
            await session.commit()
            return True
        return False

async def remove_task(task_id: int, user_id: int) -> bool:
    """Удаление задачи"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            delete(Tasks)
            .where(Tasks.id == task_id)
            .where(Tasks.owner_id == user_id)
        )
        await session.commit()
        return result.rowcount > 0
#endregion

#region Handlers
@router.callback_query(F.data == "list_all_task")
async def list_tasks_handler(callback: types.CallbackQuery):
    """Показать список задач"""
    tasks = await get_user_tasks(callback.from_user.id)
    
    if not tasks:
        await callback.message.answer("📭 У вас пока нет задач")
        return
    
    response = ["📋 Ваши задачи:\n"]
    for task in tasks:
        status = "✅" if task.is_completed else "❌"
        response.append(
            f"{status} *{task.title}*\n"
            f"🆔 ID: `{task.id}`\n"
            f"📝 Описание: {task.description or 'нет описания'}\n"
            f"📅 Создано: {task.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        )
    
    await callback.message.answer(
        "\n".join(response),
        parse_mode="Markdown",
        reply_markup=get_todolist_inline_keyboard()
    )

@router.callback_query(F.data == "add_task")
async def add_task_start(callback: types.CallbackQuery, state: FSMContext):
    """Начало добавления задачи"""
    await callback.message.answer("📝 Введите название задачи:")
    await state.set_state(TodoStates.GET_task_title)

@router.message(StateFilter(TodoStates.GET_task_title))
async def process_task_title(message: types.Message, state: FSMContext):
    """Обработка названия задачи"""
    await state.update_data(title=message.text)
    await message.delete()
    await message.answer("📄 Теперь введите описание задачи:")
    await state.set_state(TodoStates.GET_task_description)

@router.message(StateFilter(TodoStates.GET_task_description))
async def process_task_description(message: types.Message, state: FSMContext):
    """Обработка описания задачи"""
    data = await state.get_data()
    await create_task(
        title=data["title"],
        description=message.text,
        owner_id=message.from_user.id
    )
    
    await message.answer(
        "🎉 Задача успешно добавлена!",
        reply_markup=get_todolist_inline_keyboard()
    )
    await state.clear()

@router.callback_query(F.data == "done_task")
async def complete_task_start(callback: types.CallbackQuery, state: FSMContext):
    """Начало завершения задачи"""
    await callback.message.answer("🔢 Введите ID задачи для изменения статуса:")
    await state.set_state(TodoStates.CHANGE_task_status)

@router.message(StateFilter(TodoStates.CHANGE_task_status))
async def process_complete_task(message: types.Message, state: FSMContext):
    """Обработка завершения задачи"""
    try:
        task_id = int(message.text)
        success = await toggle_task_status(task_id, message.from_user.id)
        
        if success:
            await message.answer("🔄 Статус задачи обновлен!", reply_markup=get_todolist_inline_keyboard())
        else:
            await message.answer("⚠️ Задача не найдена!")
            
    except ValueError:
        await message.answer("❌ Некорректный ID задачи")
    
    await state.clear()

@router.callback_query(F.data == "delete_task")
async def delete_task_start(callback: types.CallbackQuery, state: FSMContext):
    """Начало удаления задачи"""
    await callback.message.answer("🔢 Введите ID задачи для удаления:")
    await state.set_state(TodoStates.DELETE_task_by_id)

@router.message(StateFilter(TodoStates.DELETE_task_by_id))
async def process_delete_task(message: types.Message, state: FSMContext):
    """Обработка удаления задачи"""
    try:
        task_id = int(message.text)
        success = await remove_task(task_id, message.from_user.id)
        
        if success:
            await message.answer("🗑 Задача удалена!", reply_markup=get_todolist_inline_keyboard())
        else:
            await message.answer("⚠️ Задача не найдена!")
            
    except ValueError:
        await message.answer("❌ Некорректный ID задачи")
    
    await state.clear()

@router.callback_query(F.data == "todo")
async def show_todo_menu(callback: types.CallbackQuery):
    """Показать меню задач"""
    await get_or_create_user(callback.from_user.id, callback.from_user.username)
    await callback.message.answer(
        "📌 Менеджер задач",
        reply_markup=get_todolist_inline_keyboard()
    )
    await callback.answer()
