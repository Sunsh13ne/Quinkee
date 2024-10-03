from database.models import SearchHistory, TrackedGame, User
from aiogram.types import CallbackQuery

# Функция сохранения записи в истории поиска
async def save_search_result(callback: CallbackQuery,
                             user_id: int,
                             game_appid: int,
                             name: str,
                             price: str):
    user = User.get(User.user_id == user_id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден.")
        return
    game, game_created = TrackedGame.get_or_create(
        appid=game_appid,
        defaults={
            'title': name,
            'price': price
        }
    )
    SearchHistory.create(user=user, game=game)
