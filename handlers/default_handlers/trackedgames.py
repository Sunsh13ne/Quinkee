from database.models import User, TrackedGame, UserTrackedGame, db
from keyboards.inline.back_to_menu_button import back_to_menu_button
from loader import dp
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from utils.send_paginated_games import send_paginated_games

# Обработчик команды /trackedgames
@dp.message(Command('trackedgames'))
async def handle_trackedgames_command(message: Message, state: FSMContext):
    await show_tracked_games(message, state)

# Обработчик нажатия на кнопку "Отслеживаемые игры"
@dp.callback_query(F.data == 'trackedgames')
async def handle_trackedgames_callback(callback_query: CallbackQuery, state: FSMContext):
    await show_tracked_games(callback_query, state)

# Обработчик команды /trackedgames и нажатия на кнопку "Отслеживаемые игры"
async def show_tracked_games(message_or_callback: Message | CallbackQuery, state: FSMContext):
    back_button = await back_to_menu_button()
    trackedgames_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
    await state.clear()
    user_id = message_or_callback.from_user.id
    with db:
        try:
            user = User.get_or_none(User.user_id == user_id)
            if not user:
                if isinstance(message_or_callback, Message):
                    await message_or_callback.answer("Вы не зарегистрированы в системе."
                                        "\nВыполните команду /start для регистрации.",
                                        reply_markup=trackedgames_keyboard)
                if isinstance(message_or_callback, CallbackQuery):
                    await message_or_callback.message.edit_text("Вы не зарегистрированы в системе."
                                                             "\nВыполните команду /start для регистрации.",
                                                             reply_markup=trackedgames_keyboard)
                return
            
            tracked_games = (TrackedGame
                             .select(TrackedGame.title, TrackedGame.appid, TrackedGame.price)
                             .join(UserTrackedGame)
                             .where(UserTrackedGame.user == user))
            
            if tracked_games:
                games_list = [
                    {'appid': game.appid, 'name': game.title, 'price': f'({game.price})'}
                    for game in tracked_games
                ]

                description = "Список ваших отслеживаемых игр.\nВы получите уведомление "\
                    "в случае выхода обновлений или изменения цен на эти игры."
                await send_paginated_games(message_or_callback=message_or_callback,
                                            state=state,
                                            user_id=user_id,
                                            games=games_list,
                                            description=description,
                                            page=1)
                if isinstance(message_or_callback, CallbackQuery):
                    await message_or_callback.answer()

            else:
                message = 'Вы пока не отслеживаете ни одной игры.\nНажмите '\
                    'на кнопку *"Отслеживать"* на странице нужной игры, '\
                        'если хотите получать уведомления в случае выхода '\
                            'обновлений или изменения цены на эту игру.'
                if isinstance(message_or_callback, Message):
                    await message_or_callback.answer(message,
                                                     reply_markup=trackedgames_keyboard,
                                                     parse_mode="Markdown")
                elif isinstance(message_or_callback, CallbackQuery):
                    await message_or_callback.message.edit_text(message,
                                                                reply_markup=trackedgames_keyboard,
                                                                parse_mode="Markdown")
                    await message_or_callback.answer()

        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(f"Произошла ошибка: {e}",
                                                 reply_markup=trackedgames_keyboard)
            elif isinstance(message_or_callback, CallbackQuery):
                    await message_or_callback.message.edit_text(f"Произошла ошибка: {e}",
                                                                reply_markup=trackedgames_keyboard)
                    await message_or_callback.answer()