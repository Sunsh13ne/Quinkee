from aiogram.fsm.state import StatesGroup, State

# Состояния для обработки поиска игры
class GameSearch(StatesGroup):
    waiting_for_game_name = State()
    waiting_for_game_choice = State()
    game_found = State()