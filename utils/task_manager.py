import asyncio
import logging
from api.api_requests import (fetch_and_cache_game_list,
                              fetch_game_updates,
                              fetch_game_price,
                              fetch_top100_games)
from database.models import TrackedGame
from utils.notify_users import send_update_notification, send_price_change_notification

# Функция загрузки списка игр Steam, обновляется раз в час по таймеру.
async def update_game_list():
    while True:
        if await fetch_and_cache_game_list():
            await asyncio.sleep(3600)
        else:
            await asyncio.sleep(60)

# Функция загрузки топа игр Steam, обновляется раз в сутки по таймеру.
async def update_top_list():
    while True:
        if await fetch_top100_games():
            await asyncio.sleep(86400)
        else:
            await asyncio.sleep(60)

# Функция проверки обновлений и цен, выполняется раз в час.
async def check_game_changes():
    while True:
        tracked_games = TrackedGame.select()
        for game in tracked_games:
            updates = await fetch_game_updates(game.appid)
            if updates:
                latest_update = updates[0]
                update_time = latest_update['date']
                if update_time > game.last_updated_at:
                    game.last_updated_at = update_time
                    game.save()
                    await send_update_notification(game=game,
                                                   update=latest_update)
            price = await fetch_game_price(game.appid)
            old_price = game.price
            if price and old_price != price:
                game.price = price
                game.save()
                await send_price_change_notification(game=game,
                                                     new_price=price,
                                                     old_price=old_price)
        logging.info(f'Произведена проверка обновлений и цен.')
        await asyncio.sleep(3600)