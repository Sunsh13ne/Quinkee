from loader import dp
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from utils.send_paginated_games import send_paginated_games
from config_data.config import cached_top
from keyboards.inline.back_to_menu_button import back_to_menu_button

# Обработчик команды /top
@dp.message(Command('top'))
async def handle_top_command(message: Message, state: FSMContext):
    await send_top(message, state)

# Обработчик нажатия на кнопку "Топ игр"
@dp.callback_query(F.data == 'top')
async def handle_top_callback(callback_query: CallbackQuery, state: FSMContext):
    await send_top(callback_query, state)

# Обработчик команды /top и нажатия на кнопку "Топ игр"
async def send_top(message_or_callback: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    top_list = cached_top.copy()
    if top_list:
        sorted_top_list = sorted(
            [{'appid': game['appid'], 'name': game['name'], 'ccu': game['ccu']}
            for game in top_list.values()],
            key=lambda x: x['ccu'],
            reverse=True
            )
        formated_top_list = [
            {'appid': game['appid'], 'name': game['name'], 'ccu': format_ccu(game['ccu'])}
            for game in sorted_top_list
        ]
        user_id = message_or_callback.from_user.id
        description = "Топ 100 игр Steam по количеству одновременно играющих пользователей за 2 недели.\n"\
            "Может и вам стоит попробовать? 😎"
        await send_paginated_games(message_or_callback=message_or_callback,
                             state=state,
                             user_id=user_id,
                             games=formated_top_list,
                             description=description,
                             page=1)
    else:
        back_button = await back_to_menu_button()
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
        error_text = "Не удалось загрузить список топа игр 😭. Попробуйте позже."
        if isinstance(message_or_callback, Message): 
            await message_or_callback.answer(
                text=error_text,
                reply_markup=keyboard
            )
        elif isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                text=error_text,
                reply_markup=keyboard
            )

def format_ccu(value):
    if value >= 1_000_000:
        return f"({value / 1_000_000:.1f} млн.)"
    elif value >= 1_000:
        return f"({value / 1_000:.1f} тыс.)"
    return f"({value})"