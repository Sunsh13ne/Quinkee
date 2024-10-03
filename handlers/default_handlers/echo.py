from loader import dp
from aiogram.types import Message, InlineKeyboardMarkup
from keyboards.inline.back_to_menu_button import back_to_menu_button

# Функция фильтрации неизвестных команд, сообщений
@dp.message()
async def echo_message_handler(message: Message):
    back_button = await back_to_menu_button()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
    await message.reply("К сожалению, я не знаю такой команды. "
                        "Можете ввести /help, чтобы ознакомиться с функционалом бота.",
                        reply_markup=keyboard)
