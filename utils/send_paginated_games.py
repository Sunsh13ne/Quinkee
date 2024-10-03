from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline.back_to_menu_button import back_to_menu_button
from loader import dp
from aiogram import F
from keyboards.inline.pagination_buttons import get_pagination_buttons
from utils.send_game_details import send_game_details

GAMES_PER_PAGE = 5  # Количество игр на странице

# Функция для отправки игр с пагинацией
async def send_paginated_games(message_or_callback: Message | CallbackQuery,
                               state: FSMContext,
                               user_id: int,
                               games: list,
                               description: str,
                               page: int = 1):
    total_pages = (len(games) - 1) // GAMES_PER_PAGE + 1
    start_index = (page - 1) * GAMES_PER_PAGE
    end_index = start_index + GAMES_PER_PAGE
    games_on_page = games[start_index:end_index]

    # Создание кнопок для каждой игры
    pagination_games = [
        [InlineKeyboardButton(text=f"•{GAMES_PER_PAGE*(page-1)+i+1}• "\
                              f"{game.get('time','')} "\
                              f"{game['name']} "\
                              f"{game.get('price','')}"\
                              f"{game.get('ccu','')}",
                              callback_data=f"game_{game['appid']}_{user_id}")]
        for i, game in enumerate(games_on_page)
    ]

    pagination_buttons = get_pagination_buttons(page, total_pages)
    back_button = await back_to_menu_button()
    keyboard = InlineKeyboardMarkup(inline_keyboard=pagination_games +
                                    pagination_buttons.inline_keyboard + 
                                    [[back_button]])

    data = await state.get_data()
    response_message_id = data.get('response_message_id')

    if page == 1:
        # Если это первая страница и сообщение еще не создано
        if response_message_id is None:
            if isinstance(message_or_callback, Message): 
                response_message = await message_or_callback.answer(
                    text=description,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
            elif isinstance(message_or_callback, CallbackQuery):
                response_message = await message_or_callback.message.edit_text(
                    text=description,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )

            await state.update_data(response_message_id=response_message.message_id)
        else:
            # Редактируем существующее сообщение
            if isinstance(message_or_callback, Message): 
                response_message = await message_or_callback.bot.edit_message_text(
                    chat_id=message_or_callback.chat.id,
                    message_id=response_message_id,
                    text=description,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
            elif isinstance(message_or_callback, CallbackQuery):
                response_message = await message_or_callback.message.edit_text(
                    chat_id=message_or_callback.chat.id,
                    message_id=response_message_id,
                    text=description,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
    else:
        # Если это не первая страница, редактируем существующее сообщение
        if response_message_id is not None:
            if isinstance(message_or_callback, Message):
                response_message = await message_or_callback.bot.edit_message_text(
                    chat_id=message_or_callback.chat.id,
                    message_id=response_message_id,
                    text=description,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
            elif isinstance(message_or_callback, CallbackQuery):
                response_message = await message_or_callback.message.edit_text(
                    chat_id=message_or_callback.chat.id,
                    message_id=response_message_id,
                    text=description,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )

        else:
            # Создаем новое сообщение, если по какой-то причине ID сообщения не найден
            if isinstance(message_or_callback, Message):
                response_message = await message_or_callback.answer(
                    text=description,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
            elif isinstance(message_or_callback, CallbackQuery):
                response_message = await message_or_callback.message.answer(
                    text=description,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )

            await state.update_data(response_message_id=response_message.message_id)

    await state.update_data(user_id=user_id,
                            found_games=games,
                            current_page=page,
                            total_pages=total_pages,
                            description=description)

    return response_message


# Обработчик выбора игры по кнопке
@dp.callback_query(F.data.startswith('game_'))
async def handle_game_selection(callback_query, state: FSMContext):
    game_appid = callback_query.data.split('_')[1]
    user_id = callback_query.data.split('_')[2]
    found_games = (await state.get_data()).get('found_games', [])

    chosen_game_data = next((game for game in found_games if str(game['appid']) == game_appid), None)
    if chosen_game_data:
        previous_message = callback_query.message.reply_to_message
        await send_game_details(message=callback_query.message,
                                state=state,
                                user_id=user_id,
                                game=chosen_game_data,
                                previous_message=callback_query.message)
    else:
        await callback_query.answer("Не удалось найти игру. Попробуйте еще раз.")


# Обработчик выбора страницы
@dp.callback_query(F.data.startswith('page_'))
async def process_pagination(callback_query, state: FSMContext):
    data = await state.get_data()
    found_games = data.get('found_games', [])
    page = int(callback_query.data.split('_')[1])
    user_id = data.get('user_id')
    description = data.get('description', 'Описание не найдено')
    await send_paginated_games(callback_query.message, state, user_id, found_games, description, page)
    await callback_query.answer()