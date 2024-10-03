from keyboards.inline.back_to_menu_button import back_to_menu_button
from loader import bot
from typing import Dict, Optional
from aiogram.types import InlineKeyboardMarkup
from database.models import TrackedGame

# Функция формирования списка пользователей и отправки уведомлений об обновлении игры
async def send_update_notification(game: TrackedGame, update: Dict):
    users = game.users
    game_name= game.title
    update_url = update['url']
    back_button = await back_to_menu_button()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id,
                                   text=f"Новое событие в *{game_name}*!\n[Посмотреть новость]({update_url})",
                                   parse_mode="Markdown",
                                   reply_markup=keyboard,
                                   disable_web_page_preview=False)
        except Exception as e:
            print(f"Ошибка при отправке уведомления пользователю {user.username}: {e}")

# Функция формирования списка пользователей и отправки уведомлений об обновлении цены на игру
async def send_price_change_notification(game: TrackedGame,
                                         new_price: Optional[str],
                                         old_price: Optional[str]):
    users = game.users
    game_name= game.title
    back_button = await back_to_menu_button()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id,
                                   text=f"Цена на *{game_name}* изменилась!"
                                   f"\nТекущая цена: *{new_price if new_price is not None else 'не указана.'}*"
                                   f"\nСтарая цена: *{old_price if old_price is not None else 'не указана.'}*",
                                   reply_markup=keyboard,
                                   parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка при отправке уведомления пользователю {user.username}: {e}")
        
    