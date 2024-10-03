from datetime import datetime, timedelta
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from loader import dp
from aiogram import F
from database.models import SearchHistory
from utils.send_paginated_games import send_paginated_games
from aiogram.fsm.context import FSMContext
from keyboards.inline.back_to_menu_button import back_to_menu_button


# Обработчик команды /history
@dp.message(Command('history'))
async def handle_history_command(message: Message, state: FSMContext):
    await send_history(message, state)

# Обработчик нажатия на кнопку "История поиска"
@dp.callback_query(F.data == 'history')
async def handle_history_callback(callback_query: CallbackQuery, state: FSMContext):
    await send_history(callback_query, state)

# Обработчик команды /history и нажатия на кнопку "История поиска"
async def send_history(message_or_callback: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    calendar = await SimpleCalendar(locale=await get_user_locale(
        message_or_callback.from_user)).start_calendar()
    back_button = await back_to_menu_button()
    keyboard = InlineKeyboardMarkup(inline_keyboard=calendar.inline_keyboard + [[back_button]])

    message = "Пожалуйста, выберите дату для просмотра истории запросов:"
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text=message,
            reply_markup=keyboard
        )
    elif isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(
            text=message,
            reply_markup=keyboard
        )

# Обработка выбора даты
@dp.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery,
                                  callback_data: SimpleCalendarCallback,
                                  state: FSMContext):
    selected, date = await SimpleCalendar(locale=await get_user_locale(callback_query.from_user))\
        .process_selection(callback_query, callback_data)
    
    if selected:
        user_id = callback_query.from_user.id
        
        # Получение записей из SearchHistory за выбранную дату для конкретного пользователя
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = start_of_day + timedelta(days=1)

        # Запрос к базе данных с фильтрацией по пользователю
        search_history_records = SearchHistory.select().where(
            (SearchHistory.user == user_id) &
            (SearchHistory.searched_at >= start_of_day) &
            (SearchHistory.searched_at < end_of_day)
        )

        history = []
        for record in search_history_records:
            history_entry = {
                'appid': record.game.appid,
                'name': record.game.title,
                'time': record.searched_at.strftime('(%H:%M:%S)')
            }
            history.append(history_entry)

        if history:
            description = f'На <b>{date.strftime("%d/%m/%Y")}</b> найдено записей: <b>{len(history)}</b>.'\
                '\nНажмите на название игры, чтобы получить подробную информацию.'
            await send_paginated_games(message_or_callback=callback_query,
                                       state=state,
                                       user_id=user_id,
                                       games=history,
                                       description=description,
                                       page=1)
        else:
            back_button = await back_to_menu_button()
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
            await callback_query.message.edit_text("Нет записей за эту дату.",
                                                reply_markup=keyboard)
