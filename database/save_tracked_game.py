from aiogram.types import CallbackQuery
from database.models import User, TrackedGame, UserTrackedGame
from api.api_requests import fetch_game_details
from aiogram.fsm.context import FSMContext
from config_data.config import cached_games

# Функция сохранения отслеживаемой игры в БД
async def save_tracked_game(callback: CallbackQuery,
                            state: FSMContext,
                            user_id: int,
                            steam_appid: int):
    user, created = User.get_or_create(user_id=user_id, defaults={'username': callback.from_user.username})
    data = await state.get_data()
    chosen_game_data = data.get('chosen_game_data', None)
    if chosen_game_data is not None and chosen_game_data.get('appid') == steam_appid:
        title = chosen_game_data.get('name')
        price = chosen_game_data.get('price')
    else:
        game_details = await fetch_game_details(steam_appid)
        if game_details is None:
            shortened_data = next((game for game in cached_games if game['appid'] == steam_appid), None)
            if shortened_data is not None:
                title = shortened_data.get('name')
                price = 'Неизвестно'
            return None
        else:
            title = game_details.get('name')
            is_free = game_details.get("is_free",  False)
            price = (game_details.get("price_overview", {})
                     .get("final_formatted", None) if not is_free else 'Бесплатная')

    tracked_game, game_created = TrackedGame.get_or_create(
        appid=steam_appid,
        defaults={
            'title': title,
            'price': price
        }
    )
    UserTrackedGame.get_or_create(user=user, tracked_game=tracked_game)