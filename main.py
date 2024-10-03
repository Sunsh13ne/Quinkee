from utils.set_bot_commands import set_commands
from loader import bot, dp
from handlers.default_handlers import start, help, searchgame, trackedgames, top, history, echo
from database.models import create_models
import asyncio
from utils.task_manager import update_game_list, check_game_changes, update_top_list

# Функция запуска фоновых задач при старте
async def on_startup():
    asyncio.create_task(update_game_list())
    asyncio.create_task(update_top_list())
    asyncio.create_task(check_game_changes())

# Запуск бота
async def main():
    create_models()
    await set_commands(bot)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())