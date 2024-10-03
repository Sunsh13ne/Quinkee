from keyboards.inline.back_to_menu_button import back_to_menu_button
from loader import dp
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.states import GameSearch
from utils.send_paginated_games import send_paginated_games
from utils.send_game_details import send_game_details
from handlers.default_handlers import trackedgames
from config_data.config import cached_games

# Обработчик команды /searchgame
@dp.message(Command('searchgame'))
async def handle_searchgame_command(message: Message, state: FSMContext):
    await search_game(message, state)

# Обработчик нажатия на кнопку "Поиск игр"
@dp.callback_query(F.data == 'searchgame')
async def handle_searchgame_callback(callback_query: CallbackQuery, state: FSMContext):
    await search_game(callback_query, state)

# Обработчик команды /searchgame и нажатия на кнопку "Поиск игр"
async def search_game(message_or_callback: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer("Введите название игры, которую хотите найти:")
    elif isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.answer("Введите название игры, которую хотите найти:")
        await message_or_callback.answer()
    await state.set_state(GameSearch.waiting_for_game_name)

# Обработчик текстовых сообщений, если бот в состоянии ожидания названия игры
@dp.message(GameSearch.waiting_for_game_name)
async def handle_search(message: Message, state: FSMContext):
    app_list = cached_games[:]
    game_name = message.text
    found_games = []
    back_button = await back_to_menu_button()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])

    if len(app_list) != 0:
        found_games = list({game['name']: game for game in app_list
                            if game_name.lower() in game['name'].lower()}.values())
    else:
        await state.clear()
        await message.answer(f"Возникла ошибка при получении данных. "
                             "Попробуйте повторить запрос позже.",
                             reply_markup=keyboard)
        return

    if found_games:
        await state.clear()
        if len(found_games) == 1:
            await send_game_details(message=message,
                                    state=state,
                                    user_id=message.from_user.id,
                                    game=found_games[0],
                                    previous_message=None)
        else:
            description = f"По вашему запросу найдено игр: <b>{len(found_games)}</b>.\n" \
                "Нажмите на название игры, чтобы получить подробную информацию."
            await send_paginated_games(message_or_callback=message,
                                       state=state,
                                       user_id=message.from_user.id,
                                       games=found_games,
                                       description = description,
                                       page=1)
    else:
        await message.answer("Игры с таким названием не найдены.\nПопробуйте снова:")