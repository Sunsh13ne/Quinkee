from aiogram import Bot
from aiogram.types import BotCommand
from config_data import config

DEFAULT_COMMANDS = config.DEFAULT_COMMANDS

# Функция для установки команд в меню бота
async def set_commands(bot: Bot):
    commands = [BotCommand(command=command, description=description)
                for command, description in DEFAULT_COMMANDS]
    await bot.set_my_commands(commands)