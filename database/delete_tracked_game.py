from aiogram.types import CallbackQuery
from database.models import User, TrackedGame, UserTrackedGame

# Функция удаления отслеживаемой игры из БД
async def delete_tracked_game(callback: CallbackQuery, user_id: int, steam_appid: int):

    user = User.get_or_none(user_id=user_id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден.")
        return

    tracked_game = TrackedGame.get_or_none(appid=steam_appid)
    if not tracked_game:
        await callback.answer("Ошибка: игра не найдена.")
        return

    # Удаляем запись из промежуточной таблицы, если она существует
    user_tracked_game = UserTrackedGame.get_or_none(user=user, tracked_game=tracked_game)
    if user_tracked_game:
        user_tracked_game.delete_instance()
        await callback.answer("Игра удалена из отслеживаемых!")
    else:
        await callback.answer("Игра не была добавлена в отслеживаемые.")
