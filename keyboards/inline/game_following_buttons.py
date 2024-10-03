from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.delete_tracked_game import delete_tracked_game
from database.save_tracked_game import save_tracked_game
from keyboards.inline.back_to_menu_button import back_to_menu_button
from loader import router
from aiogram.fsm.context import FSMContext
from utils.check_if_tracked_game import check_if_tracked_game

# Функция создания кнопок для отслеживания игры и перехода на страницу игры в Steam
def game_following_buttons(steam_link: str, is_tracked: bool, steam_appid: int) -> InlineKeyboardMarkup:
    steam_button = InlineKeyboardButton(text="🚀 Перейти в Steam", url=steam_link)
    if is_tracked:
        track_button = InlineKeyboardButton(text="💔 Перестать\nотслеживать",
                                            callback_data=f"untrack_game:{steam_appid}")
    else:
        track_button = InlineKeyboardButton(text="❤️ Отслеживать",
                                            callback_data=f"track_game:{steam_appid}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[steam_button, track_button]])
    return keyboard

# Обработчик колбэка для кнопки "Отслеживать"
@router.callback_query(F.data.startswith("track_game:"))
async def track_game(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    steam_appid = int(callback.data.split(":")[1])
    steam_link = f"https://store.steampowered.com/app/{steam_appid}/"
    if steam_appid:
        await save_tracked_game(callback, state=state, user_id=user_id, steam_appid=steam_appid)
        # Проверка, отслеживается ли игра
        is_tracked = await check_if_tracked_game(user_id, steam_appid)
        # Обновление кнопок
        following_buttons = game_following_buttons(steam_link, is_tracked, steam_appid)
        back_button = await back_to_menu_button()
        keyboard = InlineKeyboardMarkup(inline_keyboard=following_buttons.inline_keyboard + [[back_button]])

        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer("Игра добавлена в отслеживаемые игры!")
    else:
        await callback.answer("Ошибка: не удалось найти информацию об игре.")

# Обработчик колбэка для кнопки "Перестать отслеживать"
@router.callback_query(F.data.startswith("untrack_game:"))
async def untrack_game(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    steam_appid = callback.data.split(":")[1]
    steam_link = f"https://store.steampowered.com/app/{steam_appid}/"
    if steam_appid:
        await delete_tracked_game(callback, user_id=user_id, steam_appid=steam_appid)
        # Проверка, отслеживается ли игра
        is_tracked = await check_if_tracked_game(user_id, steam_appid)
        # Обновление кнопок
        following_buttons = game_following_buttons(steam_link, is_tracked, steam_appid)
        back_button = await back_to_menu_button()
        keyboard = InlineKeyboardMarkup(inline_keyboard=following_buttons.inline_keyboard + [[back_button]])

        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer("Игра больше не отслеживается!")
    else:
        await callback.answer("Ошибка: не удалось найти информацию об игре.")