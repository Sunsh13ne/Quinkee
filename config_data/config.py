import os
from dotenv import find_dotenv, load_dotenv
from typing import Any, List, Dict

if not find_dotenv():
  exit('Переменные окружения не загружены, так как отсутствует файл .env')
else:
  load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_PATH = os.path.join(os.getcwd(), 'database', 'database.db')

# api для получения данных об играх
STEAM_APP_LIST_API = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
STEAM_APP_UPDATES_API = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
STEAM_APP_DETAILS_API = "https://store.steampowered.com/api/appdetails"
STEAM_TOP_APPS_API = "https://steamspy.com/api.php"

# Глобальный список словарей игр, загружается и обновляется фоново
cached_games: List[Dict] = []
# Глобальный список топа игр, загружается и обновляется фоново
cached_top: Dict[str, Dict[str, Any]] = {}

DEFAULT_COMMANDS = [
    ("start", "Запуск бота"),
    # ("searchgame", "Поиск игр"),
    # ("trackedgames", "Отслеживаемые игры"),
    # ("top", "Топ игр"),
    # ("help", "Справка"),
    # ("history", "История поиска")
]
