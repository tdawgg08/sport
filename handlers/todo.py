from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.models import todo
from keyboards.todo import get_todolist_inline_keyboard
from misc.scheduler_update_date import update_time

router = Router()

class DeleteMessage(StatesGroup):
    del_message = State()

class AddTask(StatesGroup):
    adder = State()

@router.callback_query(F.data == 'todo')
async def todo_day(callback: CallbackQuery):
    tasks = await todo.filter(
        telegram_id=callback.from_user.id,
        date=update_time()
    )
    
    if tasks:
        task_list = ""
        for item in tasks:
            task_list += f'{item.id}) {item.todo_task}\n'
        
        await callback.message.answer(
            f'📝 Ваши задачи на сегодня:\n\n{task_list}', 
            reply_markup=get_todolist_inline_keyboard()
        )
    else:
        await callback.message.answer(
            '📝 На сегодня задач нет', 
            reply_markup=get_todolist_inline_keyboard()
        )
    
    await callback.answer()        

@router.callback_query(F.data == 'delete_task')
async def delete_task_todo(callback : CallbackQuery, state : FSMContext):
    await callback.message.answer('Введите ID таски, которую хотите удалить') 
    await state.set_state(DeleteMessage.del_message)
    await callback.answer()

@router.message(DeleteMessage.del_message)
async def id_to_delete_message(message : Message, state : FSMContext):
        message_id = message.text

        test = await todo.get_or_none(
                telegram_id = message.from_user.id,
                id = message_id
            )
        if test:
            await test.delete()
            await message.answer('Данные успешно удалены!', reply_markup=get_todolist_inline_keyboard())    
        else:           
            await message.answer('Сообщения не найдено', reply_markup=get_todolist_inline_keyboard())
        await state.clear()        


@router.callback_query(F.data == 'add_task')
async def adder_task(callback : CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите вашу таску')
    await state.set_state(AddTask.adder)
    await callback.answer()


@router.message(AddTask.adder)
async def update_message(message : Message, state : FSMContext):
    task = message.text

    await todo.create(
        telegram_id = message.from_user.id,
        username = message.from_user.username,
        todo_task = task,
        date = update_time()
    )    
    await state.clear()