from aiogram import Router, F 
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F, types
from keyboards.menu import menu_kb
from database.database import AsyncSessionLocal
from database.models import User

router = Router()


@router.callback_query(F.data == 'menu')
async def menu_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    if not all(f'answered_{i}' in data for i in range(1, 8)):
        await callback.answer('❌ Ответьте на все вопросы!', show_alert=True)
        return
    
    # message_text = "📊 Ваши ответы:\n\n" + "\n".join(
    #     f"Вопрос {i}: {data[f'answered_{i}']}" 
    #     for i in range(1, 8)
    # )
    
    # if len(message_text) > 4096:
    #     message_text = message_text[:4000] + "\n... [сообщение обрезано]"
    
    else:
        try:
            
            # await callback.message.edit_text(message_text)
            
            async with AsyncSessionLocal() as session:
                user = User(
                    user_id=callback.from_user.id,
                    first_username=callback.from_user.first_name or "",
                    last_username=callback.from_user.last_name or "",
                    first_answer=data['answered_1'],
                    second_answer=data['answered_2'],
                    third_answer=data['answered_3'],
                    fourth_answer=data['answered_4'],
                    fifth_answer=data['answered_5'],
                    sixth_answer=data['answered_6'],
                    seventh_answer=data['answered_7']
                )
                session.add(user)
                await session.commit()
                
            await callback.answer("✅ Данные сохранены!")
        
        except Exception as e:
            print(e)
            error_msg = f"Ошибка: {str(e)[:100]}"
            await callback.answer(error_msg, show_alert=True)

        finally:
            await state.clear()
            await callback.message.delete()

        await callback.message.answer('Меню', reply_markup=menu_kb())
    