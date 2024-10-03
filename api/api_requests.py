import logging
import aiohttp
from typing import List
from config_data.config import (STEAM_APP_DETAILS_API,
                                STEAM_APP_LIST_API,
                                STEAM_APP_UPDATES_API,
                                STEAM_TOP_APPS_API,
                                cached_games,
                                cached_top)

# Функция получения и сохранения списка игр
async def fetch_and_cache_game_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(STEAM_APP_LIST_API) as response:
            if response.status == 200:
                global cached_games
                games_data_json = await response.json()
                new_cached_games = games_data_json.get('applist', {}).get('apps', [])
                cached_games.clear()
                cached_games.extend(new_cached_games)
                logging.info(f'Список игр обновлен.')
                return True
            else:
                logging.error(f'Ошибка при получении списка игр: {response.status}')
                return False
            
# Функция получения и сохранения топа игр           
async def fetch_top100_games():
    params = {'request': 'top100in2weeks'}
    async with aiohttp.ClientSession() as session:
        async with session.get(STEAM_TOP_APPS_API, params=params) as response:
            if response.status == 200:
                data_json = await response.json()
                cached_top.clear()
                cached_top.update(data_json)
                logging.info(f'Топ игр обновлен.')
                return True
            else:
                logging.error(f'Ошибка обновления топа игр: {response.status}')
                return False

# Функция для поиска игр по названию (возвращает список игр)
async def fetch_games_by_name(game_name: str, quantity: int) -> List:
    async with aiohttp.ClientSession() as session:
        async with session.get(STEAM_APP_LIST_API) as response:
            if response.status == 200:
                games = await response.json()
                found_games = list({game['name']: game for game in games['applist']['apps']
                                    if game_name.lower() in game['name'].lower()}.values())
                return found_games[:quantity]
            return []

# Функция для поиска игры по AppID
async def fetch_game_by_appid(appid: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(STEAM_APP_LIST_API) as response:
            if response.status == 200:
                games = await response.json()
                found_game = next((game for game in games['applist']['apps'] if game['appid'] == appid), None)
                return found_game if found_game else None
            return None

# Функция получения информации о последнем обновлении игры по AppID
async def fetch_game_updates(appid: int, quantity: int = 1):
    params = {'appid': appid, 'count': quantity}
    async with aiohttp.ClientSession() as session:
        async with session.get(STEAM_APP_UPDATES_API, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data['appnews']['newsitems']
            return None

# Функция для получения подробной информации об игре по AppID
async def fetch_game_details(appid: int):
    params = {'appids': appid, 'cc': 'ru', 'l': 'russian'}
    async with aiohttp.ClientSession() as session:
        async with session.get(STEAM_APP_DETAILS_API, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data[str(appid)]['success']:
                    return data[str(appid)].get('data')
            return None

# Функция получения цены игры по AppID
async def fetch_game_price(appid: int):
    data = await fetch_game_details(appid)
    if data is not None:
        is_free = data.get("is_free", False)
        price = ('Бесплатная' if is_free else data.get("price_overview", {})
                 .get("final_formatted", 'Неизвестно'))
        return price
    return None