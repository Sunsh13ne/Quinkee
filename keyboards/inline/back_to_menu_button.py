from aiogram.types import InlineKeyboardButton, CallbackQuery
from loader import dp
from aiogram import F
from aiogram.fsm.context import FSMContext

# Функция создания кнопки возврата к главному меню
async def back_to_menu_button():
    back_button = InlineKeyboardButton(text='⬅️ Назад к меню', callback_data='back_to_menu')
    return back_button

# Обработчик нажатия на кнопку 'Назад к меню'
@dp.callback_query(F.data == 'back_to_menu')
async def process_callback_back_to_menu(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    from keyboards.inline.menu_buttons import menu_buttons
    if callback_query.message.text:
        await callback_query.message.edit_text("\nㅤ\n ──────   *Главное меню*   ────── \nㅤ",
                                               reply_markup=await menu_buttons(),
                                               parse_mode="Markdown")
    else:
        await callback_query.message.answer("\nㅤ\n ──────   *Главное меню*   ────── \nㅤ",
                                            reply_markup=await menu_buttons(),
                                            parse_mode="Markdown")
        await callback_query.message.delete()
    await callback_query.answer()