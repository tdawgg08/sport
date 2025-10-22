from aiogram import Router, F 
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types
from keyboards.menu import menu_kb
from database.models import User
from handlers.gpt_after_start import send_recomendation

router = Router()


@router.callback_query(F.data == 'menu')
async def menu_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    if not all(f'answered_{i}' in data for i in range(1, 8)):
        await callback.answer('❌ Ответьте на все вопросы!', show_alert=True)
        return
    
    else:
        try:
            await User.create(
                telegram_id = callback.from_user.id,
                username = callback.from_user.username,
                first_answer=data['answered_1'],
                second_answer=data['answered_2'],
                third_answer=data['answered_3'],
                fourth_answer=data['answered_4'],
                fifth_answer=data['answered_5'],
                sixth_answer=data['answered_6'],
                seventh_answer=data['answered_7'] 
            )
    
            await callback.answer("✅ Данные сохранены!")
            await send_recomendation(callback.from_user.id, callback.message)
        
        except Exception as e:
            print(e)
            error_msg = f"Ошибка: {str(e)[:100]}"
            await callback.answer(error_msg, show_alert=True)

        finally:
            await state.clear()
            
            chat_id = callback.message.chat.id
            user_id = callback.from_user.id
            
            last_msg_id = callback.message.message_id
            
            for msg_id in range(last_msg_id, max(0, last_msg_id-100), -1):
                try:
                    await callback.bot.delete_message(chat_id, msg_id)
                except:
                    pass

        await callback.message.answer('Меню', reply_markup=menu_kb())
@router.callback_query(F.data == 'back')        
async def back_command(callback: CallbackQuery):
    await callback.message.answer('Меню', reply_markup=menu_kb())
    await callback.answer()